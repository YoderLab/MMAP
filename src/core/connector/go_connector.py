'''

@author: Steven Wu

connect it AmiGoS
Setup on at Dec 2011, if URL/webpage changes then need update it accordingly
'''

from httplib import IncompleteRead
import httplib
import os
import re
import socket
import sys
import time
import urllib
from urllib2 import URLError, HTTPError
import urllib2
import warnings

from core import re_patterns
from core.sequence import Sequence2
from core.utils import string_utils
from numpy.f2py.auxfuncs import throw_error
from urlparse import ParseResult


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

AMIGO_BLAST_URL = "http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi"
# http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi

DELAY = 5.0

MAX_QUERY_SEQ_LENGTH = 3e6

RE_NO_SEQ_COUNTER = re.compile("Your job contains (\d+) sequence")
RE_GET_SESSION_ID = re.compile("\!--\s+session_id\s+=\s+(\d+amigo\d+)\s+--")
# RE_GET_SESSION_ID = re.compile  ("\s+session_id\s+=\s+(\d+amigo\d+)")
# <!-- session_id         = 634amigo1360013506 -->
DEFAULT_BATCH_SIZE = 20
DEFAULT_E_VALUE_CUT_OFF = 1e-15


# #TODO: read http://bcbio.wordpress.com/2009/10/18/gene-ontology-analysis-with-python-and-bioconductor/

class GOConnector(object):
    """
        seq_record in SeqRecord format,
        created from SeqIO.index
        self.record_index = SeqIO.index(infile, "fasta")

    """
    socket.setdefaulttimeout(180)
    warnings.simplefilter("always")
    DELIM = Sequence2.DEFAULT_DELIM

    def __init__(self, seq_record, max_query_size=DEFAULT_BATCH_SIZE,
                 e_value_cut_off=DEFAULT_E_VALUE_CUT_OFF, tempfile=None, debug=False):

#         self.conn = httplib.HTTPConnection("amigo.geneontology.org:80")
        self.max_query_size = max_query_size
        self.seq_record = seq_record
        self.e_threshold = e_value_cut_off
        self.web_session_list = []
        self.all_seqs = []
        self.debug = debug
        if tempfile:
            self.tempfile = tempfile
        else:
            self.tempfile = None


    def create_WebSessions_batches(self):

        max_query_size_1 = self.max_query_size - 1
#         datas = []
#         WebSession.e_threshold = self.e_threshold
        self.web_session_list = []
        keys = []
        data = ""

        for i, key in enumerate(self.seq_record):
            # print i, key, type(self.seq_record[key]), type(self.seq_record[key].seq), type(self.seq_record[key].format("fasta"))
            data = data + ">" + key + "\n" + str(self.seq_record[key].seq) + "\n"
            keys.append(key)
            if i % self.max_query_size is max_query_size_1:
                if len(data) > MAX_QUERY_SEQ_LENGTH:
                    warnings.warn("TODO: Implement auto scale down blast batch size. Total query length %d > %d"\
                                  % (len(data), MAX_QUERY_SEQ_LENGTH))
                wb = WebSession(data, keys, self.e_threshold, debug=self.debug)
                self.web_session_list.append(wb)
                data = ""
                keys = []
        if data != "":
            wb = WebSession(data, keys, self.e_threshold, debug=self.debug)
            self.web_session_list.append(wb)
#        datas.append(data)
#        print "DATA:\n", data
#        print datas
#        return datas


    def amigo_batch_mode(self):
#         self.debug = True

        print "AmiGo BatchMode, dose tempfile exist? %s\t%s" % (os.path.exists(self.tempfile), self.tempfile)
#         if self.tempfile and not os.path.exists(self.tempfile):
        if not os.path.exists(self.tempfile):
            return self.amigo_batch_mode_new()
        else:
            return self.amigo_batch_resume()

#         else:
#             version = 1
#             while os.path.exists(self.filename + ".%s.fna" % version):
#                 version = version + 1
#             self.filename = self.filename + ".%s.fna" % version

    def amigo_batch_mode_new(self):

        if self.tempfile:
            tempout = open(self.tempfile, "w+")
            print "creat tempFile:\t%s" % self.tempfile

        self.create_WebSessions_batches()
#         self.web_session_list = self.web_session_list[0:3]
        total_BLAST = len(self.web_session_list)

        print "Total number of BLAST Sessions:", total_BLAST
        session_id_list = [None] * total_BLAST
        for i, wb in enumerate(self.web_session_list):
            print "BLAST: ", (i + 1), "/", total_BLAST

#            wb.query_page = _get_web_page(query_blast, AMIGO_BLAST_URL)
#            session_id_list[i] = wb.session_id
#            print session_id_list[i] , wb.session_id, wb.query_page
            wb.handle = _get_web_page_handle(wb.query_blast, AMIGO_BLAST_URL)
#            if i == 2:
#                break
        print "Submitted all BLAST queries"

#         self.debug = True
#         print session_id_list
#         print self.web_session_list
        if self.tempfile:
            tempout.write("BeginSavingSessionID\n")
        while not all(session_id_list):
            for ii, wb in enumerate(self.web_session_list):
                if self.debug:
                    print "=In loop %d with session_id: %s" % (ii, wb.session_id)
                if not wb.session_id:

                    if self.debug:
                        print "==No session_id", ii, wb.session_id
                    try:
                        if not wb.handle:
                            wb.handle = _get_web_page_handle(wb.query_blast, AMIGO_BLAST_URL)
                        wb.query_page = str(wb.handle.read())
                        wb.handle = None

                        session_id_list[ii] = wb.get_session_id()
                        if session_id_list[ii]:
                            if self.debug:
                                print "===Got the id:\t%s", session_id_list[ii]
                            if self.tempfile:
                                tempout.write("StoreSessionID%s%s\n" % (self.DELIM, session_id_list[ii]))
                        if self.debug:
                            print "====Done reading:", len(wb.query_page), session_id_list[ii]  # , wb.query_page

#                            break
                    except HTTPError, e:
                        print 'The server couldn\'t fulfill the request.'
                        print 'Error code: ', e.code
                        print wb.handle.code
                        wb.handle = None
#                        wb.handle = _get_web_page_handle(wb.query_blast, AMIGO_BLAST_URL)
#                        print "done recreated handle ", wb.handle.code
                    except URLError, e:
                        print 'We failed to reach a server.'
                        print 'Reason: ', e.reason
                        print wb.handle.code
                        wb.handle = None
#                        wb.handle = _get_web_page_handle(wb.query_blast, AMIGO_BLAST_URL)
#                        print "done recreated handle ", wb.handle.code
            #            continue
                    except IncompleteRead as e:
                        print "IncompleteRead:", e  # , e.partial
                        wb.handle = None

                    except socket.timeout as e:
                        print "timeout ", wb.handle.code, ii
                        wb.handle = None

#                        wb.handle = _get_web_page_handle(wb.query_blast, AMIGO_BLAST_URL)
#                        print "done recreated handle ", wb.handle.code
                        warnings.warn("timouout! retry\n%s%s" % (e, ii))
                    except socket.error as e:
                        print wb.handle.code
                        wb.handle = None
#                        wb.handle = _get_web_page_handle(wb.query_blast, AMIGO_BLAST_URL)
#                        print "done recreated handle ", wb.handle.code
                        warnings.warn("socket error\n%s%s%s" % (e, type(e), ii))
                        # TODO: this happen quite a few times

        if self.tempfile:
            tempout.write("ENDSession\n")

        # TODO: Maybe use Pickles??
        for ii, wb in enumerate(self.web_session_list):

            wb.parse_querypage()
            self.all_seqs.extend(wb.go_results)
            out = self.generate_output_result(wb)
            if self.tempfile:
                if self.debug:
                    print "Store in tempfile: %s" % wb.session_id
                tempout.write(out)


        if self.tempfile:
            tempout.close()
        print "End amigo_batch_mode_new\n"
        return len(self.web_session_list)




    def amigo_batch_resume(self):

        print "RESUME!!! Tempfile exist: %s!" % self.tempfile
        tempout = open(self.tempfile, "a+")

        self.stored_session_id = []
        line = ""
        end_session_string = "ENDSession"
        StoreSessionID = "StoreSessionID"
        StoreResult = "StoreResult"
        end_storeResult = "ENDResult"
        is_parse_result = False
        is_saving_completed = False
        for line in tempout.readlines():
            line = line.strip()

            if line.startswith(StoreSessionID):
                index = line.split(self.DELIM)
                sid = index[1]
                self.web_session_list.append(sid)
            if line.startswith(end_session_string):
                is_saving_completed = True
            if line.startswith(end_storeResult):
                is_parse_result = False

            if is_parse_result and line.startswith("SeqID"):
                index = line.split(self.DELIM)  # Use $ becasue GO:000251 terms got : already
                seqid = index[1]
                seqSet = index[2]
#                 print seqid, seqSet
#                 sset = Ste
                seq = Sequence2(seqid, seqSet)
                seq.combined_terms = eval(seqSet)
#                 print seq
                self.all_seqs.append(seq)

            if line.startswith(StoreResult):
                index = line.split(self.DELIM)
                sid = index[1]
                self.stored_session_id.append(sid)
                is_parse_result = True

        if not is_saving_completed:
            print "===Warning!! Not all session_ids are stored, recreate batch mode"
            return self.amigo_batch_mode_new()

        if self.debug:
            print "Full   session_list:", self.web_session_list
            print "Stored sessios_list:", self.stored_session_id

        missiing_session = set(self.web_session_list) - set(self.stored_session_id)

        print "Missing _%d_ session(s): %s" % (len(missiing_session), missiing_session)

        for session_id in missiing_session:
            print "Retrieving session: %s" % session_id
            wb = WebSession.create_with_session_id_only(session_id)
            wb.parse_querypage()
            self.all_seqs.extend(wb.go_results)
            out = self.generate_output_result(wb)

            if self.debug:
                print "Store in tempfile:%s" % wb.session_id
            tempout.write(out)



        if self.debug:
            for seq in self.all_seqs:
                print seq.outputResult(),

        tempout.close()
        print "End amigo_batch_resume", len(missiing_session)
        return len(missiing_session)

    def generate_output_result(self, wb):
        out = "StoreResult%s%s\n" % (self.DELIM, wb.session_id)
        for seq in wb.go_results:
            out += seq.outputResult()
        out += "ENDResult\n"
        return out

    def get_GO_terms(self, seq):
        """
            seq: sequence format
            core.sequence.py
        """
        self.seq = seq
        self.seq = blast_AmiGO(self.seq)
        self.seq = extract_ID(self.seq)
        self.seq = parse_go_term(self.seq, self.e_threshold)


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
#             print l
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


def parse_go_term(seq, e_value_cut_off, debug=False):
    """1 seq -> blast -> n hits -> m GO terms
    """

    if(debug):
        print(seq.seq_id)
    if seq.is_match:
        result_Full, result_Summary, list_GO_term = dict(), dict(), set()
    #    e_threshold = 1e-25

        for i, m in enumerate(seq.acc_ID):
            if seq.e_value[i] < e_value_cut_off:
#                 if debug:
#                     print("======PASS e-cutoff:%e\t%e\t%s\n" % (seq.e_value[i], e_threshold, e_threshold))
                search_Key = "<span id=\"" + m + "\">"
                match_index = seq.web_page.find(search_Key)
                end_match_index = seq.web_page.find("Length", match_index)
                raw_list = seq.web_page[match_index:end_match_index]
                raw_list = re_patterns.multi_space_sub(" ", raw_list)
                term_full_list = re_patterns.go_term_full_findall(raw_list)

                term_summary_list = re_patterns.go_term_exact_findall("".join(term_full_list))
#                 if debug:
# #                     print(i, m)
# #                     print(term_full_list)
#                     print(term_summary_list, "\n============\n")
                result_Full[m] = term_full_list
                result_Summary[m] = term_summary_list
                list_GO_term.update(term_summary_list)
                seq.add(m, term_summary_list)
#             else:
#                 if debug:
#                     print("======Fail e-cutoff:%e\t%e\n" % (seq.e_value[i] , e_threshold))
    return seq


def _get_web_page_httplib(connector, query):

    message = urllib.urlencode(query)
    header = {"User-Agent": "BiopythonClient"}
#            request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient"})
#
    connector.request("POST", "/cgi-bin/amigo/blast.cgi", message, header)
#    r1 = connector.getresponse()
#    print r1.status, r1.reason
#            print r1.
#    data = r1.read()
#    return connector
#    print data

# @retry(urllib2.URLError, tries=4, delay=3, backoff=2)


def _get_web_page(query, URL):

    s = None
    for _ in range(10):
        try:

            message = urllib.urlencode(query)

            request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient"})
#            print "URL:", URL, "\n", message, "\n", request, "\n"
#            print request.get_data()
#            print request.get_full_url()
            handle = urllib2.urlopen(request)

#            print handle
#            print type(handle)
#            print dir(handle)
#            print handle.getcode
#            print handle.geturl
#            print handle.headers
#            print handle.code
#            print handle.msg
#            print handle.url
#    s = _as_string(handle.read())
            s = str(handle.read())
            break
        except HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        except socket.timeout as e:
            warnings.warn("timouout! retry\n%s" % e)
        except socket.error as e:
            warnings.warn("[Errno 104] Connection reset by peer!!\n%s\n%s\t%s" % (e, query, URL))
#            continue
#    print s
#    sys.exit()
    return s


# @retry(urllib2.URLError, tries=4, delay=3, backoff=2)
def _get_web_page_handle(query, URL):
    # TODO faster? with httplib?
    handle = None
    message = urllib.urlencode(query)
    request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient"})
#     print message
#     print request
    while True:
        handle = urllib2.urlopen(request)
        if handle.code > 0:
#             print handle.code
            break
#         print len(handle)
#         print len(handle)
    return handle


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




def parse_get_blast_results_query(session_id, page):
    query = [('action', 'get_blast_results'),
             ('session_id', session_id),
             ("page", page),
             ('CMD', 'Put')]
    return query


class WebSession(object):

    def __init__(self, query_data, key_list, e_threshold, max_hits=1000, debug=False):
#         max_hits = 101
        self.query_data = query_data
        self.key_list = key_list
        if e_threshold:
            self.e_threshold = e_threshold
        else:
            self.e_threshold = DEFAULT_E_VALUE_CUT_OFF
        self.max_hits = max_hits
        self.session_id = None
        self.query_page = None
        self.seq_counter = 0
        self.go_results = []

        self.debug = debug
        self.query_blast = [('action', 'blast'),
                            ('seq', self.query_data),
                            ('maxhits', self.max_hits),
                            ('threshold', self.e_threshold),
                            ('CMD', 'Put')]
#        print query_data
#        print key_list

    def parse_querypage(self):

        query_wait = parse_get_blast_results_query(self.session_id, 1)
        self.query_page = wait_for_query_result(query_wait)
        self._get_seq_counter()

        if self.debug:
            print "======parsing %d sequences" % self.seq_counter
        for page in range(self.seq_counter):
#            print "parse sequences %d/%d" % (page, self.seq_counter)
            seq = None
            while seq is None:
                query = parse_get_blast_results_query(self.session_id, page + 1)
                web_page = _get_web_page(query, AMIGO_BLAST_URL)
                if web_page is not None:
                    seq = self.parse_seq(web_page)
#                    print "---in ", page, "with ", seq
            self.go_results.append(seq)
#        return self.go_results
#        return web_pages

    def _get_seq_counter(self):

        match = RE_NO_SEQ_COUNTER.search(self.query_page)
        if match:
            self.seq_counter = int(match.group(1))
            if self.key_list and self.seq_counter != len(self.key_list):
                warnings.warn("Mismatch numebr of sequencs=%d, and number of key=%d keys" % (self.seq_counter, len(self.key_list)))
        else:
            print "no matches!!!", self.seq_counter


    def parse_seq(self, web_page):

        seq_id = self._find_seq_id(web_page)
        seq = Sequence2(seq_id, web_page)
        seq = extract_ID(seq)
        seq = parse_go_term(seq, self.e_threshold, self.debug)

        if seq_id and self.key_list and seq_id not in self.key_list:
            warnings.warn("Seq_ID %s doesn't exist in the list %s" % (seq_id, self.key_list))

        return seq



    def _find_seq_id(self, web_pages):
        index = web_pages.find("<p class=\"sequence\">>")
        index_end = web_pages.find("<br>", index)
        if index == -1 and index_end == -1:
            return None
        else:
            gid = web_pages[index + len("<p class=\"sequence\">>"):index_end].strip()
            return gid

#    def _get_query_page(self):
#        return self._query_page
#
#    def _set_query_page(self, query_page):
#        self._query_page = query_page
#
#    query_page = property(_get_query_page, _set_query_page)


    def get_session_id(self):
#         self.session_id = None
        if self.session_id:
            return self.session_id
        match = RE_GET_SESSION_ID.search(self.query_page)
        if match:
            self.session_id = match.group(1)
            if self.debug:
                print "Assign session_id=", self.session_id
    #    try:
    #
    #    except AttributeError as e:
    #        raise AttributeError("AttributeError: %s \n webpage: %s" % (e, webpage))
        return self.session_id

    @classmethod
    def create_with_session_id_only(cls, session_id):  # @NoSelf
        wb = cls(None, None, None)
        wb.session_id = session_id
        return wb


#    wb.session_id = wb.get_session_id(wb.query_page)


###########

class MyHandler(urllib2.HTTPHandler):
    def http_response(self, req, response):
        print "url: %s" % (response.geturl(),)
        print "info: %s" % (response.info(),)
        for l in response:
            print l
        return response

# o = urllib2.build_opener(MyHandler())
# t = threading.Thread(target=o.open, args=('http://www.google.com/',))
# t.start()
# print "I'm asynchronous!"
#
# t.join()
#
# print "I've ended!"










