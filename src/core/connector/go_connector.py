'''

@author: Steven Wu

connect it AmiGoS
Setup on at Dec 2011, if URL/webpage changes then need update it accordingly
'''


from core import re_patterns
from core.sequence import Sequence2
from core.utils import string_utils
from urllib2 import URLError
import re
import socket
import sys

import time
import urllib
import urllib2
import warnings


# # check these later

# ## waiting time
# <h1>BLAST Query Submission</h1>

# <div class="block">
# <h2>Success!</h2>
# <p>Your job has been successfully submitted to the BLAST queue.</p>
# seq.web_page.find("Your job has been successfully submitted to the BLAST queue")

# <a href="blast.cgi?action=get_blast_results&amp;session_id=3873amigo1320966804" title="Retrieve your BLAST job">
# "blast.cgi?action=get_blast_results&amp;session_id=3873amigo1320966804"

MATCH_HREF = "<a href=\""
MATCH_HREF_HASH = "<a href=\"#"
MATCH_HREF_HASH_LEN = len(MATCH_HREF_HASH)
MATCH_END_HREF = "\">"
MATCH_END_HREF_LEN = len(MATCH_END_HREF)

MATCH_BLAST_WAIT = "<a href=\"blast.cgi?action=get_blast_results&amp;session_id="
MATCH_BLAST_WAIT_LEN = len(MATCH_BLAST_WAIT)
MATCH_BLAST_END = "\" title=\"Retrieve your BLAST job\">"

MATCH_BLAST_NOT_COMPLETE = ("Please be patient as your job may take several minutes to complete. This page will automatically refresh with the BLAST results when the job is done.")

AMIGO_BLAST_URL = "http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi"
DELAY = 5.0

MAX_QUERY_SEQ_LENGTH = 3e6

RE_NO_SEQ_COUNTER = re.compile("Your job contains (\d+) sequence")
RE_GET_SESSION_ID = re.compile("\!--\s+session_id\s+=\s+(\d+amigo\d+)\s+--")
# RE_GET_SESSION_ID = re.compile  ("\s+session_id\s+=\s+(\d+amigo\d+)")
# <!-- session_id         = 634amigo1360013506 -->
DEFAULT_BATCH_SIZE = 50
DEFAULT_E_VALUE_CUT_OFF = 1e-15


class GOConnector(object):
    """
        seq_record in SeqRecord format,
        created from SeqIO.index
        self.record_index = SeqIO.index(infile, "fasta")

    """
    socket.setdefaulttimeout(30)
    warnings.simplefilter("always")

    def __init__(self, seq_record, max_query_size=DEFAULT_BATCH_SIZE, e_value_cut_off=DEFAULT_E_VALUE_CUT_OFF):


        self.max_query_size = max_query_size
        self.seq_record = seq_record
        self.e_value_cut_off = e_value_cut_off
        self.web_session_list = []
        self.all_seqs = []


    def parse_seq_record(self):
#        datas = []
        max_query_size_1 = self.max_query_size - 1
        WebSession.e_value_cut_off = self.e_value_cut_off
        keys = []
        data = ""
        for i, key in enumerate(self.seq_record):
#            print i, key, type(self.seq_record[key]), type(self.seq_record[key].seq), type(self.seq_record[key].format("fasta"))
            data = data + ">" + key + "\n" + str(self.seq_record[key].seq) + "\n"
            keys.append(key)
            if i % self.max_query_size is max_query_size_1:
                if len(data) > MAX_QUERY_SEQ_LENGTH:
                    warnings.warn("TODO: Implement auto scale down blast batch size. Total query length %d > %d"\
                                  % (len(data), MAX_QUERY_SEQ_LENGTH))
                self.web_session_list.append(WebSession(data, keys))
                data = ""
                keys = []
        if data != "":
            self.web_session_list.append(WebSession(data, keys))
#        datas.append(data)
#        print "DATA:\n", data
#        print datas
#        return datas

    def amigo_batch_mode(self):
        self.parse_seq_record()

        for wb in self.web_session_list:
            query_blast = [
                ('action', 'blast'),
                ('seq', wb.query_data),
                ('CMD', 'Put')]

            wb.query_page = _get_web_page(query_blast, AMIGO_BLAST_URL)


        for wb in self.web_session_list:
            seq_result = wb.parse_querypage()
            self.all_seqs.extend(seq_result)



    def get_GO_terms(self, seq):
        """
            seq: sequence format
            core.sequence.py
        """
        self.seq = seq
        self.seq = blast_AmiGO(self.seq)
        self.seq = extract_ID(self.seq)
        self.seq = parse_go_term(self.seq, self.e_value_cut_off)




def get_session_id(webpage):
    match = RE_GET_SESSION_ID.search(webpage)
    session_id = match.group(1)
    return session_id


def blast_AmiGO(seq):
    """ blast Amigo with data \
    no customise blast parameters yet"""

    query_blast = [
        ('action', 'blast'),
        ('seq', seq.data),
        # ('seq_id','FB:FBgn0015946'),
        ('CMD', 'Put')]

    seq.web_page = _get_web_page(query_blast, AMIGO_BLAST_URL)

    is_complete = seq.web_page.find(MATCH_BLAST_NOT_COMPLETE)
    previous = time.time()

    while is_complete != -1:
        current = time.time()
        wait = previous + DELAY - current
        if wait > 0:
            time.sleep(wait)
            print("wait %d s" % DELAY)
            previous = current + wait
        else:
            previous = current
        session_id_index = seq.web_page.find(MATCH_BLAST_WAIT, is_complete) + MATCH_BLAST_WAIT_LEN
        session_id_index_end = seq.web_page.find(MATCH_BLAST_END, is_complete)
        session_id = seq.web_page[session_id_index:session_id_index_end]
        query_wait = [
            ('action', 'get_blast_results'),
            ('session_id', session_id),
            ('CMD', 'Put')]
#        http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi?action=get_blast_results&session_id=1284amigo1359406324&CMD=Put
        seq.web_page = _get_web_page(query_wait, AMIGO_BLAST_URL)
        is_complete = seq.web_page.find(MATCH_BLAST_NOT_COMPLETE)

    return seq



def extract_ID(seq):
    """
    extract all ID and evalues
    """

    if seq.web_page.find("*** NONE ***") == -1:
        key = "Sequences producing High-scoring Segment Pairs"
        end_key = "<span id="
        blast_matches = string_utils.substring(seq.web_page, key, end_key)
        lines = blast_matches.splitlines()

        acc_ID, match_ID, e_value = [], [], []
        # TODO: change data structure later
        # for i,l in enumerate(lines):
        for l in lines:
            if l.find(MATCH_HREF_HASH) != -1:
                token = re_patterns.multi_space_split(l)
                if len(token) != 4:
                    raise UserWarning("Error: incorrecting parsing", token, len(token))
                    print "====NEVER REACH HERE??=====", token, len(token)
                    break
                start = token[0].find(MATCH_HREF_HASH) + MATCH_HREF_HASH_LEN
                mid = token[0].find(MATCH_END_HREF)
                end = token[0].find("</a>")
                acc_ID.append(token[0][start:mid])  # search webpage
                match_ID.append(token[0][mid + MATCH_END_HREF_LEN:end])
                try:
                    v = float(token.pop(len(token) - 2))
                    e_value.append(v)  # or call pop() twice
                except ValueError as e:
#                    print 'ValueError: %s' % e;
                    raise ValueError("ValueError: %s \t %s \t %s" %
                                     {e, sys.exc_info()[0], sys.exc_info()[1]})

        seq.acc_ID = acc_ID
        seq.match_ID = match_ID
        seq.e_value = e_value
        seq.is_match = True

    else:
        seq.is_match = False

    return seq


def parse_go_term(seq, e_value_cut_off):
    """1 seq -> blast -> n hits -> m GO terms
    """
    if seq.is_match:
        result_Full, result_Summary, list_GO_term = dict(), dict(), set()
    #    e_value_cut_off = 1e-25
        for i, m in enumerate(seq.acc_ID):
            if seq.e_value[i] < e_value_cut_off:
                search_Key = "<span id=\"" + m + "\">"
                match_index = seq.web_page.find(search_Key)
                end_match_index = seq.web_page.find("Length", match_index)
                raw_list = seq.web_page[match_index:end_match_index]
                raw_list = re_patterns.multi_space_sub(" ", raw_list)
                term_full_list = re_patterns.go_term_full_findall(raw_list)
                term_summary_list = re_patterns.go_term_exact_findall("".join(term_full_list))
                result_Full[m] = term_full_list
                result_Summary[m] = term_summary_list
                list_GO_term.update(term_summary_list)
                seq.add(m, term_summary_list)

    return seq



# @retry(urllib2.URLError, tries=4, delay=3, backoff=2)
def _get_web_page(query, URL):

    s = None
    for _ in range(10):
        try:

            message = urllib.urlencode(query)
            request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient"})
            handle = urllib2.urlopen(request)
#    s = _as_string(handle.read())
            s = str(handle.read())
            break
        except URLError as e:
            warnings.warn("retry %s\n%s" % (query, e))
#            continue
        except socket.timeout:
            warnings.warn("timouout! retry")
#            continue
#    print s
#    sys.exit()
    return s


def wait_for_query_result(query_wait):
    query_page = _get_web_page(query_wait, AMIGO_BLAST_URL)
    is_complete = query_page.find(MATCH_BLAST_NOT_COMPLETE)
#        previous, current = [time.time()] * 2
    previous = time.time()
    while is_complete != -1:
        current = time.time()
        wait = previous + DELAY - current
        if wait > 0:
            time.sleep(wait)
            print("wait %d s" % DELAY)
            previous = current + wait
        else:
            previous = current

        query_page = _get_web_page(query_wait, AMIGO_BLAST_URL)
        is_complete = query_page.find(MATCH_BLAST_NOT_COMPLETE)
    return query_page


def find_seq_id(web_pages):
    index = web_pages.find("<p class=\"sequence\">>")
    index_end = web_pages.find("<br>", index)
    gid = web_pages[index + len("<p class=\"sequence\">>"):index_end].strip()
    return gid


def parse_get_get_blast_results_query(session_id, page):
    query = [('action', 'get_blast_results'),
            ('session_id', session_id),
            ("page", page),
            ('CMD', 'Put')]
    return query


class WebSession(object):
    e_value_cut_off = DEFAULT_E_VALUE_CUT_OFF

    def __init__(self, query_data, key_list):
        self.query_data = query_data
        self.key_list = key_list

        self.session_id = None
        self._query_page = None
        self.seq_counter = 0
        self.go_results = []



#        print query_data
#        print key_list




    def parse_seq(self, web_page):

        seq_id = find_seq_id(web_page)
        if seq_id not in self.key_list:
            warnings.warn("ID doesn't match %s" % seq_id)

        seq = Sequence2(seq_id, web_page)
        seq = extract_ID(seq)
        seq = parse_go_term(seq, self.e_value_cut_off)
        return seq



    def parse_querypage(self):

        query_wait = parse_get_get_blast_results_query(self.session_id, 1)
        self.query_page = wait_for_query_result(query_wait)
        self._get_seq_counter()
#        web_pages = [None] * self.seq_counter
        for page in range(self.seq_counter):

            query = parse_get_get_blast_results_query(self.session_id, page + 1)
            web_page = _get_web_page(query, AMIGO_BLAST_URL)

            seq = self.parse_seq(web_page)
            self.go_results.append(seq)
        return self.go_results
#        return web_pages



    def _get_seq_counter(self):

        match = RE_NO_SEQ_COUNTER.search(self.query_page)
#        if match:
        self.seq_counter = int(match.group(1))
#        print "seq_counter:%d\tlist_length:%d" % (seq_counter, len(self.key_list))
#        print seq_counter == len(self.key_list), seq_counter is len(self.key_list)
        if self.seq_counter != len(self.key_list):
            warnings.warn("Mismatch numebr of sequencs=%d, and number of key=%d keys" % (self.seq_counter, len(self.key_list)))


    def _get_query_page(self):
        return self._query_page

    def _set_query_page(self, query_page):
        self._query_page = query_page
        self.session_id = get_session_id(self._query_page)

    query_page = property(_get_query_page, _set_query_page)
