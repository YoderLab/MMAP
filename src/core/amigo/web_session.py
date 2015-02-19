"""
Created on Dec 18, 2014

@author: Steven Wu
"""


import re
import time
import urllib2
import warnings
import socket
from urllib2 import URLError, HTTPError
from httplib import IncompleteRead


from core.amigo import web_page_utils
from core.amigo.go_sequence import GoSequence


MATCH_BLAST_NOT_COMPLETE = web_page_utils.MATCH_BLAST_NOT_COMPLETE
AMIGO_BLAST_URL = web_page_utils.AMIGO_BLAST_URL




RE_NO_SEQ_COUNTER = re.compile("Your job contains (\d+) sequence")
RE_GET_SESSION_ID = re.compile("\!--\s+session_id\s+=\s+(\d+amigo\d+)\s+--")
# RE_GET_SESSION_ID = re.compile  ("\s+session_id\s+=\s+(\d+amigo\d+)")
# <!-- session_id         = 634amigo1360013506 -->
# http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi?action=get_blast_results&amp;session_id=

DEFAULT_TIMEOUT = 180  # Should be long enough for most cases, most of them finish < 90s with 50k query_limits


def warning_on_one_line(message, category, filename, lineno, _):
    return '%s:%s: %s:%s\n' % (filename, lineno, category.__name__, message)
# warnings.formatwarning = warning_on_one_line


def wait_for_query_result(query_wait):
    query_page = web_page_utils.get_web_page(query_wait, AMIGO_BLAST_URL)
    is_complete = query_page.find(MATCH_BLAST_NOT_COMPLETE)
#        previous, current = [time.time()] * 2
    previous = time.time()
    while is_complete != -1:
        current = time.time()
        wait = previous + web_page_utils.DELAY - current
        if wait > 0:
            time.sleep(wait)
            print("wait %d s" % web_page_utils.DELAY)
            previous = current + wait
        else:
            previous = current

        query_page = web_page_utils.get_web_page(query_wait, AMIGO_BLAST_URL)
        is_complete = query_page.find(MATCH_BLAST_NOT_COMPLETE)
    return query_page


def parse_get_blast_results_query(session_id, page):
    query = [('action', 'get_blast_results'),
             ('session_id', session_id),
             ("page", page),
             ('CMD', 'Put')]
    return query


class WebSession(object):

    def __init__(self, query_data, key_list, e_threshold, max_hits=1000, timeout=DEFAULT_TIMEOUT, debug=False):

        self.query_data = query_data
        self.key_list = key_list
        self.e_threshold = e_threshold
        self.max_hits = max_hits
        self.timeout = timeout
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

    @classmethod
    def create_with_session_id_only(cls, session_id):  # @NoSelf
        wb = cls(None, None, None)
        wb.session_id = session_id
        return wb


    def create_session_id(self):

        try:
            if not self.handle:
                self.handle = web_page_utils.get_web_page_handle(self.query_blast, AMIGO_BLAST_URL, self.timeout)
            self.query_page = str(self.handle.read())
            self.handle = None

            self.get_session_id()
            if self.session_id:
                if self.debug:
                    print "===DEBUG: Got the id:\t%s" % self.session_id
#                 if self.tempfile:
#                     tempout.write("%s%s%s%s%s\n" % (STORE_SESSION_ID_STRING, self.DELIM, ii, self.DELIM, session_id_list[ii]))
#                     tempout.flush()
#             if self.debug:
#                 print "====Done reading:", len(wb.query_page), session_id_list[ii]  # , wb.query_page

        except AttributeError, e:  # # for legacy code without self.timeout
            self.timeout = DEFAULT_TIMEOUT
            warnings.warn("AttributeError::%s. Legacy WebSession format without self.timeou, set to DEFAULT_TIMEOUT" % (e))
        except HTTPError, e:
            print 'The server could not fulfill the request.Error code: ', e
            self.handle = None
            warnings.warn("HTTPError::%s" % (e))

        except URLError, e:
            print 'We failed to reach a server. Reason: ', e
            self.handle = None
            warnings.warn("URLError::%s" % (e))

        except IncompleteRead as e:
            self.handle = None
            warnings.warn("IncompleteRead::%s" % (e))

        except socket.timeout as e:
            self.handle = None
            self.timeout *= 2
            warnings.warn("socket.timouout::%s. Retry with doubled default timeout:%ds" % (e, self.timeout))

        except socket.error as e:
            self.handle = None
            warnings.warn("socket.error::%s" % (e))

        except StandardError as e:
            self.handle = None
            warnings.warn("StandardError::%s" % (e))

        return self.session_id


    def get_session_id(self):
        if self.session_id:
            return self.session_id
        match = RE_GET_SESSION_ID.search(self.query_page)
        if match:
            self.session_id = match.group(1)
#             if self.debug:
#                 print "==Assign session_id=", self.session_id

        return self.session_id


    def parse_querypage(self):

        query_wait = parse_get_blast_results_query(self.session_id, 1)
        self.query_page = wait_for_query_result(query_wait)
        complete = False

#             isReRun = self._get_seq_counter()
#                 def _get_seq_counter(self):

        match = RE_NO_SEQ_COUNTER.search(self.query_page)
        if match:
            self.seq_counter = int(match.group(1))
            if self.key_list and self.seq_counter != len(self.key_list):
                warnings.warn("Mismatch numebr of sequencs=%d, and number of key=%d keys" % (self.seq_counter, len(self.key_list)))
            if self.debug:
                print "===DEBUG: Parsing %d sequences" % self.seq_counter
            for page in range(self.seq_counter):
    #            print "parse sequences %d/%d" % (page, self.seq_counter)

                query = parse_get_blast_results_query(self.session_id, page + 1)
                seq = None
                while seq is None:
                    web_page = web_page_utils.get_web_page(query, AMIGO_BLAST_URL)
                    if web_page is not None:
                        seq = self.parse_seq(web_page)
    #                    print "---in ", page, "with ", seq
                self.go_results.append(seq)
            complete = True
        else:
            """
            Error message from AmiGOs
            fatal message   There is an error in the configuration of AmiGO.
            Your cached BLAST results were lost. Please try again.
            """
            warnings.warn("No seq matched from id:%s!!! seq_counter=%d Recreate session_id!" % (self.session_id, self.seq_counter))
            complete = False
#             print self.session_id
            self.session_id = None
            while self.session_id is None:
                self.create_session_id()
#                 print self.session_id
        return complete


    def parse_seq(self, web_page):
        seq_id = self._find_seq_id(web_page)
        if seq_id is None:
            return None

        seq = GoSequence(seq_id, web_page)
        seq.extract_ID()
        seq.parse_go_term(self.e_threshold, self.debug)
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


###########################################################################

class WebSessionFile(WebSession):

    def __init__(self, query_data, key_list, e_threshold, query_file, max_hits=1000, debug=False):
        warnings.warn("Deprecated class: WebSessionFile. Don't think we need this in the future.", PendingDeprecationWarning)
        self.query_data = query_data
        self.key_list = key_list
        self.e_threshold = e_threshold
        self.max_hits = max_hits

        self.session_id = None
        self.query_page = None
        self.handle = None
        self.seq_counter = 0
        self.go_results = []

        self.debug = debug
        self.query_file = query_file
        self.query_blast = [('action', 'blast'),
                            ('maxhits', self.max_hits),
                            ('threshold', self.e_threshold),
                            ('CMD', 'Put')]

#     def create_session_id(self):
#         try:
#             if not self.handle:
#                 self.handle = web_page_utils.get_web_page_handle_file(self.query_blast, self.query_file, AMIGO_BLAST_URL)


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






