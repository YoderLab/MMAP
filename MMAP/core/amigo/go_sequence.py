"""
Created on Jan 8, 2015

@author: Steven Wu
"""
import sys
import time
import warnings

from core import re_patterns
from core.amigo import web_page_utils
from core.utils import string_utils


MATCH_HREF = "<a href=\""
MATCH_HREF_HASH = "<a href=\"#"
MATCH_HREF_HASH_LEN = len(MATCH_HREF_HASH)
MATCH_END_HREF = "\">"
MATCH_END_HREF_LEN = len(MATCH_END_HREF)

MATCH_BLAST_WAIT = "<a href=\"blast.cgi?action=get_blast_results&amp;session_id="
MATCH_BLAST_WAIT_LEN = len(MATCH_BLAST_WAIT)
MATCH_BLAST_END = "\" title=\"Retrieve your BLAST job\">"

# # check these later
# ## waiting time
# <h1>BLAST Query Submission</h1>
# <div class="block">
# <h2>Success!</h2>
# <p>Your job has been successfully submitted to the BLAST queue.</p>
# seq.web_page.find("Your job has been successfully submitted to the BLAST queue")
# <a href="blast.cgi?action=get_blast_results&amp;session_id=3873amigo1320966804" title="Retrieve your BLAST job">
# "blast.cgi?action=get_blast_results&amp;session_id=3873amigo1320966804"
# http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi?action=get_blast_results&amp;session_id=



MATCH_BLAST_NOT_COMPLETE = web_page_utils.MATCH_BLAST_NOT_COMPLETE
AMIGO_BLAST_URL = web_page_utils.AMIGO_BLAST_URL



class GoSequence(object):
    """store all blast results from 1 seq
    class __doc__
    """
    DEFAULT_DELIM = "$"

    def __init__(self, seq_id, webpage):
        self.seq_id = seq_id
        self.web_page = webpage

        self.each_term = dict()  # {str: set()}
        self.combined_terms = set()
        self.is_match = False

        self.len = 0
        self.acc_ID, self.match_ID, self.e_value = [], [], []


    def add(self, key, term):
        '''append term, term must be a list (str doesnt work)'''
        self.each_term[key] = set(term)
        self.combined_terms.update(term)
        self.len += 1

    def __len__(self):
        ''' "Emulating" method, should override len()'''
        return self.len

    def get_one_term(self, key):
        return self.each_term[key]

    def get_combinations(self):
        '''
        return tuple (index_in_dist_matrix, set1, set2)
        index_in_dist_matrix in "tuple", with (row_index, col_index) for lower triangle
        '''

        keyList = self.each_term.keys()
        len_set = len(keyList)
#        dist = numpy.zeros(shape=(len_set, len_set), dtype=numpy.float32)
        combList = []
        for i, u in enumerate(self.each_term.values()):
            for j in range(i + 1, len_set):
                v = self.each_term.get(keyList[j])
#                print "i:%d \t j:%d \t %d and %s and %s" % (i ,j,len(u&v), str(u), str(v))
                combList.append(((j, i), u, v))

        return combList


    def __str__(self, *args, **kwargs):

        out = "GoSequence_Seq_ID: %s\n\tall_terms:%s\n" % (self.seq_id,
                                                          self.combined_terms)
        return out


#     def outputResult(self, *args, **kwargs):
    def outputResult(self, delim=DEFAULT_DELIM):
#         delim = kwargs["delim"]
#         print kwargs, delim
        out = "SeqID%s%s%s%s\n" % (delim, self.seq_id, delim, self.combined_terms)
        return out


    def extract_ID(self):
        """
        extract all ID and evalues
        """

        if self.web_page.find("*** NONE ***") == -1:
            key = "Sequences producing High-scoring Segment Pairs"
            end_key = "<span id="
            blast_matches = string_utils.substring(self.web_page, key, end_key)
            lines = blast_matches.splitlines()

            acc_ID, match_ID, e_value = [], [], []

            # for i,l in enumerate(lines):
            for l in lines:
#                 print l
                if l.find(MATCH_HREF_HASH) != -1:
#                     print l
                    token = re_patterns.multi_space_split(l)
#                     print token
                    if len(token) < 4:
                        warnings.warn("Error: incorrecting parsing", token, len(token), l, "(lazy regular expression was used)")
                        print "====NEVER REACH HERE??=====", token, len(token)
                        """
                          File "/home/steven/Postdoc/Project_Lemur/MMAP/src/core/amigo/web_session.py", line 213, in parse_seq
    seq.extract_ID()
  File "/home/steven/Postdoc/Project_Lemur/MMAP/src/core/amigo/go_sequence.py", line 126, in extract_ID
    raise UserWarning("Error: incorrecting parsing", token, len(token))
UserWarning: ('Error: incorrecting parsing', ['<a href="#UniProtKB:P37643">UNIPROTKB|P37643</a> - symbol:yhjE "YhjE', 'MFS transporter" sp...', '624', '9.4e-57', '2'], 5)

                        """
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
                        raise ValueError("ValueError: %s \t %s \t %s \t %s (lazy regular expression was used)" %
                                         {e, sys.exc_info()[0], sys.exc_info()[1]}, l)

            self.acc_ID = acc_ID
            self.match_ID = match_ID
            self.e_value = e_value
            self.is_match = True

        else:
            self.is_match = False
#         return seq


    def parse_go_term(self, e_value_cut_off, debug=False):
        """1 seq -> blast -> n hits -> m GO terms
        """

        if debug:
            print "=====DEBUG: parse_go_term, seq_id:", self.seq_id
        if self.is_match:
            result_Full, result_Summary, list_GO_term = dict(), dict(), set()

            for i, m in enumerate(self.acc_ID):
                if self.e_value[i] < e_value_cut_off:
    #                 if debug:
    #                     print("======PASS e-cutoff:%e\t%e\t%s\n" % (seq.e_value[i], e_threshold, e_threshold))
                    search_Key = "<span id=\"" + m + "\">"
                    match_index = self.web_page.find(search_Key)
                    end_match_index = self.web_page.find("Length", match_index)
                    raw_list = self.web_page[match_index:end_match_index]
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
                    self.add(m, term_summary_list)
    #             else:
    #                 if debug:
    #                     print("======Fail e-cutoff:%e\t%e\n" % (seq.e_value[i] , e_threshold))
#         return seq


    def blast_AmiGO(self, raw_sequence):
        """ blast Amigo with data \
        no customise blast parameters yet"""

        query_blast = [
            ('action', 'blast'),
            ('seq', raw_sequence),
            # ('seq_id','FB:FBgn0015946'),
            ('CMD', 'Put')]

        self.web_page = web_page_utils.get_web_page(query_blast, AMIGO_BLAST_URL)

        is_complete = self.web_page.find(MATCH_BLAST_NOT_COMPLETE)
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
            session_id_index = self.web_page.find(MATCH_BLAST_WAIT, is_complete) + MATCH_BLAST_WAIT_LEN
            session_id_index_end = self.web_page.find(MATCH_BLAST_END, is_complete)
            session_id = self.web_page[session_id_index:session_id_index_end]
            query_wait = [
                ('action', 'get_blast_results'),
                ('session_id', session_id),
                ('CMD', 'Put')]
    #        http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi?action=get_blast_results&session_id=1284amigo1359406324&CMD=Put
            self.web_page = web_page_utils.get_web_page(query_wait, AMIGO_BLAST_URL)
            is_complete = self.web_page.find(MATCH_BLAST_NOT_COMPLETE)

