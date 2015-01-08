"""
Created on Dec 18, 2014

@author: Steven Wu
"""


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
# from core.connector import go_connector



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


RE_NO_SEQ_COUNTER = re.compile("Your job contains (\d+) sequence")
RE_GET_SESSION_ID = re.compile("\!--\s+session_id\s+=\s+(\d+amigo\d+)\s+--")
# RE_GET_SESSION_ID = re.compile  ("\s+session_id\s+=\s+(\d+amigo\d+)")
# <!-- session_id         = 634amigo1360013506 -->
DEFAULT_BATCH_SIZE = 20
DEFAULT_E_VALUE_CUT_OFF = 1e-15


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
        print "parse_go_term" , seq.seq_id
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
        self.handle = None
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
#             print web_pages
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






