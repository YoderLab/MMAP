'''

@author: Steven Wu

connect it AmiGoS
Setup at Dec 2011, if URL/webpage changes then need update it accordingly
'''

from httplib import IncompleteRead
import os
import pickle
import socket
from urllib2 import URLError, HTTPError
import warnings

from core.amigo import web_page_utils, go_sequence
from core.amigo.go_sequence import GoSequence
from core.amigo.web_session import WebSession


MAX_QUERY_SEQ_LENGTH = 3e6

DEFAULT_BATCH_SIZE = 20
DEFAULT_E_VALUE_CUT_OFF = 1e-15

AMIGO_BLAST_URL = go_sequence.AMIGO_BLAST_URL
# #TODO: read http://bcbio.wordpress.com/2009/10/18/gene-ontology-analysis-with-python-and-bioconductor/
# # maybe backup URL?? http://tools.bioso.org/cgi-bin/amigo/blast.cg
STORE_SESSION_ID_STRING = "StoreSessionID"
END_SESSION_ID_STRING = "ENDSession"

STORE_RESULT_STRING = "StoreResult"
END_STORE_RESULT_STRING = "ENDResult"
SEQ_ID_STRING = "SeqID"


class GOConnector(object):
    """
        seq_record in SeqRecord format,
        created from SeqIO.index
        self.record_index = SeqIO.index(infile, "fasta")

    """
    socket.setdefaulttimeout(120)
    warnings.simplefilter("always")
    DELIM = GoSequence.DEFAULT_DELIM

    def __init__(self, seq_record, max_query_size=DEFAULT_BATCH_SIZE,
                 e_value_cut_off=DEFAULT_E_VALUE_CUT_OFF, tempfile=None, debug=False):

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


    def amigo_batch_mode(self):
        print "AmiGo BatchMode, dose tempfile exist? %s\t%s" % (os.path.exists(self.tempfile), self.tempfile)
#         if self.tempfile and not os.path.exists(self.tempfile):

        if not os.path.exists(self.tempfile):
            return self.amigo_batch_mode_new()
        else:
            return self.amigo_batch_resume()




    def get_id_for_all_web_sessions(self, session_id_list, tempout):
        total_BLAST = len(session_id_list)
        while not all(session_id_list):
            for ii, wb in enumerate(self.web_session_list):

                if not wb.session_id:
                    if self.debug:
                        print "DEBUG:==In loop %d/%d, NO session_id: %s" % (ii, total_BLAST, wb.session_id)

                    session_id_list[ii] = wb.create_session_id()
                    if session_id_list[ii]:
                        tempout.write("%s%s%s%s%s\n" % (STORE_SESSION_ID_STRING, self.DELIM, ii, self.DELIM, session_id_list[ii]))
                        tempout.flush()

                else:
                    if self.debug:
                        print "DEBUG:==SKIP loop %d/%d, got session_id: %s" % (ii, total_BLAST, wb.session_id)
#                     print "BLAST: ", (i + 1), "/", total_BLAST


    def retrieving_all_session_results(self, complete_index_boolean, tempout):
        while not all(complete_index_boolean):
            for ii, is_complete in enumerate(complete_index_boolean):
                if not is_complete:
                    print "Retrieving session index=(%d) ID:%s" % (ii, self.web_session_list[ii].session_id)
                    complete_index_boolean[ii] = self.retrieving_session_result(self.web_session_list[ii], tempout)
                    if not complete_index_boolean[ii]:
                        print "Recreate session_id: %s" % self.web_session_list[ii].session_id
                        tempout.write("%s%s%s%s%s\n" % (STORE_SESSION_ID_STRING, self.DELIM, ii, self.DELIM, self.web_session_list[ii].session_id))
                        tempout.flush()



    def retrieving_session_result(self, wb, tempout):
        complete = wb.parse_querypage()
        if complete:
            self.all_seqs.extend(wb.go_results)
            out = self.generate_output_result(wb)
            if self.debug:
                print "DEBUG: Store in tempfile:%s" % wb.session_id
            tempout.write(out)
            tempout.flush()

        return complete


    def amigo_batch_mode_new(self):


        tempout = open(self.tempfile, "w+")
        print "Creat tempFile:\t%s" % self.tempfile

        self.create_WebSessions_batches()

        t2File = self.tempfile + "object"
        file = open(t2File, 'w')
        pickle.dump(self.web_session_list, file)
        file.close()

        total_BLAST = len(self.web_session_list)
        print "Total number of BLAST Sessions:", total_BLAST
        session_id_list = [None] * total_BLAST

        tempout.write("BeginSavingSessionID\n")
        self.get_id_for_all_web_sessions(session_id_list, tempout)
        tempout.write("%s\n" % END_SESSION_ID_STRING)
        tempout.flush()


        complete_index_boolean = [False] * total_BLAST
        self.retrieving_all_session_results(complete_index_boolean, tempout)
        tempout.close()
        print "End amigo_batch_mode_new\n"
        return len(self.web_session_list)


    def rebuild_web_session_list_from_tempobject(self):
#         t2File = self.tempfile + "object"
#         file = open(t2File, 'r')
#         self.web_session_list = pickle.load(file)
#         file.close()

        total_BLAST = len(self.web_session_list)
        session_id_list = [None] * total_BLAST
        for i in self.stored_web_session_info:
            if i != 0:
                index = int(i[0])
                sid = i[1]
                session_id_list[index] = sid
                self.web_session_list[index].session_id = sid

        return session_id_list

    def amigo_batch_mode_resume_partial(self):


        tempout = open(self.tempfile, "a")
        print "Append to tempFile:\t%s" % self.tempfile

        session_id_list = self.rebuild_web_session_list_from_tempobject()
        total_BLAST = len(self.web_session_list)
        print "RESUME_PARTIAL, get rest of the session_id\nTotal number of BLAST Sessions:%d" % total_BLAST

        self.get_id_for_all_web_sessions(session_id_list, tempout)
        tempout.write("%s\n" % END_SESSION_ID_STRING)
        tempout.flush()


        complete_index_boolean = [False] * total_BLAST
        self.retrieving_all_session_results(complete_index_boolean, tempout)

        tempout.close()
        print "End amigo_batch_mode_new\n"
        return len(self.web_session_list)




    def amigo_batch_resume(self):

        print "RESUME!!! Tempfile exist: %s!" % self.tempfile
        tempout = open(self.tempfile, "r+")

        t2File = self.tempfile + "object"
        file = open(t2File, 'r')
        self.web_session_list = pickle.load(file)
        file.close()

        total_BLAST = len(self.web_session_list)

        self.stored_session_id_result = []
        self.stored_web_session_info = [0] * total_BLAST
        line = ""


        is_parse_result = False
        is_saving_completed = False
        for line in tempout.readlines():
            line = line.strip()
#             print line
            if line.startswith(STORE_SESSION_ID_STRING):
                index = line.split(self.DELIM)
                sid = index[2]
#                 self.stored_web_session_info.append((index[1], sid))
                self.stored_web_session_info[int(index[1])] = (index[1], sid)

            if line.startswith(END_SESSION_ID_STRING):
                is_saving_completed = True
            if line.startswith(END_STORE_RESULT_STRING):
                is_parse_result = False

            if is_parse_result and line.startswith(SEQ_ID_STRING):
                index = line.split(self.DELIM)  # Use $ becasue GO:000251 terms got : already
                seqid = index[1]
                seqSet = index[2]
#                 print seqid, seqSet
#                 sset = Ste
                seq = GoSequence(seqid, seqSet)
                seq.combined_terms = eval(seqSet)
#                 print seq
                self.all_seqs.append(seq)

            if line.startswith(STORE_RESULT_STRING):
                index = line.split(self.DELIM)
                sid = index[1]
                self.stored_session_id_result.append(sid)
                is_parse_result = True


        if self.debug:
            print "DEBUG: Full saved session_list:", self.stored_web_session_info
            print "DEBUG: Stored  sessios_results:", self.stored_session_id_result

        if not is_saving_completed:
            print "===Warning!! Not all session_ids are stored, recreate using partial batch mode"
            print self.stored_web_session_info
            return self.amigo_batch_mode_resume_partial()



        stored_session_id_only = self.rebuild_web_session_list_from_tempobject()
        complete_index_boolean = [x in self.stored_session_id_result for x in stored_session_id_only]

#         stored_session_id_only = [ x[1] for x in self.stored_web_session_info]
#         missiing_session_id = set(stored_session_id_only) - set(self.stored_session_id_result)
#         missiing_session_id = list(missiing_session_id)
#         print "Missing %d session(s): %s" % (len(missiing_session_id), missiing_session_id)
        missing_length = total_BLAST - sum(complete_index_boolean)
        print "Missing %d session(s)." % missing_length
        if self.debug:
            missing_session_index = [i for i, is_comp in enumerate(complete_index_boolean) if not is_comp]
            print "DEBUG: Missing %d session(s): Index: %s" % (len(missing_session_index), missing_session_index)

        self.retrieving_all_session_results(complete_index_boolean, tempout)

        tempout.close()
        print "End amigo_batch_resume, number of missed session: %d" % missing_length
        return missing_length



    def generate_output_result(self, wb):
        out = "%s%s%s\n" % (STORE_RESULT_STRING, self.DELIM, wb.session_id)
        for seq in wb.go_results:
            out += seq.outputResult()
        out += END_STORE_RESULT_STRING + "\n"
        return out

