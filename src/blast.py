from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIStandalone
from Bio.Blast import NCBIXML

result_handle = NCBIWWW.qblast("blastn", "nr", "8332116")



#save_file = open("my_blast.xml", "w")
#save_file.write(result_handle.read())
#save_file.close()
#result_handle.close()
#result_handle2 = open("my_blast.xml")

#aa = result_handle
#aa.next()
#result_handle.next()
#data = aa.read()

http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?QUERY=AGGTTGGTTGGGAGGATTG&DATABASE=nr&FORMAT_TYPE=HTML&PROGRAM=blastn&CLIENT=web&SERVICE=plain&PAGE=Nucleotides&CMD=Put

http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?RID=954517013-7639-11119&CMD=Get

blast_records = NCBIXML.parse(result_handle)
blast_record = blast_records.next()
blast_record2 = blast_records.next()
print blast_record


blast_record_all = list(blast_records)

i=1
for blast_record in blast_records:
    print "a: ", i



##

E_VALUE_THRESH = 0.05

for alignment in blast_record.alignments:
    for hsp in alignment.hsps:
        if hsp.expect < E_VALUE_THRESH:
            print '****Alignment****'
            print 'sequence:', alignment.title
            print 'length:', alignment.length
            print 'e value:', hsp.expect
            print hsp.query[0:75] + '...'
            print hsp.match[0:75] + '...'
            print hsp.sbjct[0:75] + '...'


alignment.accession
alignment.hit_def
alignment.hit_id ## XM_002866936


hsp.align_length
hsp.bits
hsp.expect
hsp.frame
hsp.gaps
hsp.identities
hsp.match
hsp.num_alignments
hsp.positives
hsp.query
hsp.query_end
hsp.query_start
hsp.sbjct
hsp.sbjct_end
hsp.sbjct_start
hsp.score
hsp.strand



from Bio import Entrez
Entrez.email = "A.N.Other@example.com"
handle = Entrez.einfo()
record = Entrez.read(handle)

record.keys()
[u'DbList']
The values stored in this key is the list of database names shown in the XML above:

handle = Entrez.einfo(db="gene")
record = Entrez.read(handle)
record["DbInfo"]["Description"]
record["DbInfo"]["Count"]
record["DbInfo"]["LastUpdate"]
record["DbInfo"].keys()



Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
handle = Entrez.esearch(db="gene", term="XM_002866936")
record = Entrez.read(handle)
record["IdList"]
['9303054']
#handle = Entrez.esearch(db="nucleotide", term="XM_002866936")

handle = Entrez.efetch(db="gene", id="9303054", retmode="asn1")
data = handle.read()
print


data.find("UniProtKB/TrEMBL")
data.strip(data.find("UniProtKB/TrEMBL"), data.find("UniProtKB/TrEMBL")+100)
data[data.find("UniProtKB/TrEMBL"):data.find("UniProtKB/TrEMBL")+100]
#save_file = open("testOut.txt", "w")
#save_file.write(data)
#save_file.close()

You can also use ESearch to search GenBank. Here we’ll do a quick search for the matK gene in Cypripedioideae orchids (see Section 8.2 about EInfo for one way to find out which fields you can search in each Entrez database):

>>> handle = Entrez.esearch(db="nucleotide",term="Cypripedioideae[Orgn] AND matK[Gene]")
>>> record = Entrez.read(handle)
>>> record["Count"]
'25'
>>> record["IdList"]





Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
handle = Entrez.einfo()
result = handle.read()




from Bio import ExPASy
handle = ExPASy.get_sprot_raw("XM_002866936")



##############
def qblast2(program, database, sequence,
       auto_format=None,composition_based_statistics=None,
       db_genetic_code=None,endpoints=None,entrez_query='(none)',
       expect=10.0,filter=None,gapcosts=None,genetic_code=None,
       hitlist_size=50,i_thresh=None,layout=None,lcase_mask=None,
       matrix_name=None,nucl_penalty=None,nucl_reward=None,
       other_advanced=None,perc_ident=None,phi_pattern=None,
       query_file=None,query_believe_defline=None,query_from=None,
       query_to=None,searchsp_eff=None,service=None,threshold=None,
       ungapped_alignment=None,word_size=None,
       alignments=500,alignment_view=None,descriptions=500,
       entrez_links_new_window=None,expect_low=None,expect_high=None,
       format_entrez_query=None,format_object=None,format_type='XML',
       ncbi_gi=None,results_file=None,show_overview=None, megablast=None,
       ):

entrez_query='(none)'
expect=10.0
hitlist_size=50
alignments=500
descriptions=500
format_type='XML'




import urllib, urllib2
import time
import sys
try:
    from cStringIO import StringIO ;
except ImportError:
    from StringIO import StringIO ;

from Bio._py3k import _as_string ;


assert program in ['blastn', 'blastp', 'blastx', 'tblastn', 'tblastx']

# Format the "Put" command, which sends search requests to qblast.
# Parameters taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node5.html on 9 July 2007
# Additional parameters are taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node9.html on 8 Oct 2010
# To perform a PSI-BLAST or PHI-BLAST search the service ("Put" and "Get" commands) must be specified
# (e.g. psi_blast = NCBIWWW.qblast("blastp", "refseq_protein", input_sequence, service="psi"))
program = 'blastn';
database = "nt";
sequence = "8332116";



 #("blastn", "nr", "8332116")
parameters = [  ('DATABASE',database),
    ('PROGRAM',program),
    ('QUERY',sequence),
    ('CMD', 'Put'),
]

query = [x for x in parameters if x[1] is not None]
message = urllib.urlencode(query)

## test GO
sequence = "8332116";
sequence = "GO:0006468";
sequence = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALK";
#"P55269";

 #("blastn", "nr", "8332116")
parameters = [
	('action','blast'),
    ('seq',sequence),
    #('seq_id','FB:FBgn0015946'),
    ('CMD', 'Put'),
]

query = [x for x in parameters if x[1] is not None]
message = urllib.urlencode(query)

GOUrl = "http://amigo.geneontology.org/cgi-bin/amigo/search.cgi"
GOBlast = "http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi"
request = urllib2.Request(GOBlast, message, {"User-Agent":"BiopythonClient"})

# http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi?action=blast&seq_id=FB:FBgn0015946&session_id=9173amigo1320696173

#~ request = urllib2.Request(GOUrl, message, {"User-Agent":"BiopythonClient"})
handle = urllib2.urlopen(request)


#handle = urllib2.urlopen("http://amigo.geneontology.org/cgi-bin/amigo/term_details?term=GO:0022008")


s = _as_string(handle.read())
save_file = open("testOut.html", "w")
save_file.write(s)
save_file.close()




# Send off the initial query to qblast.
# Note the NCBI do not currently impose a rate limit here, other
# than the request not to make say 50 queries at once using multiple
# threads.
request = urllib2.Request("http://blast.ncbi.nlm.nih.gov/Blast.cgi",
message,
{"User-Agent":"BiopythonClient"})
handle = urllib2.urlopen(request)

# Format the "Get" command, which gets the formatted results from qblast
# Parameters taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node6.html on 9 July 2007
rid, rtoe = _parse_qblast_ref_page(handle)
parameters = [
    ('ALIGNMENTS',alignments),
    ('FORMAT_TYPE',format_type),
    ('RID',rid),
    ('CMD', 'Get'),
    ]
query = [x for x in parameters if x[1] is not None]
message = urllib.urlencode(query)

# Poll NCBI until the results are ready.  Use a 3 second wait
delay = 3.0
previous = time.time()
while True:
    current = time.time()
    wait = previous + delay - current
    if wait > 0:
        #~ time.sleep(wait)
        previous = current + wait
    else:
        previous = current

    request = urllib2.Request("http://blast.ncbi.nlm.nih.gov/Blast.cgi",
                              message,
                              {"User-Agent":"BiopythonClient"})
    handle = urllib2.urlopen(request)
    results = _as_string(handle.read())
    # Can see an "\n\n" page while results are in progress,
    # if so just wait a bit longer...
    if results=="\n\n":
        continue
    # XML results don't have the Status tag when finished
    if results.find("Status=") < 0:
        break
    i = results.index("Status=")
    j = results.index("\n", i)
    status = results[i+len("Status="):j].strip()
    if status.upper() == "READY":
        break


return StringIO(results)




def _parse_qblast_ref_page(handle):
    """Extract a tuple of RID, RTOE from the 'please wait' page (PRIVATE).
    The NCBI FAQ pages use TOE for 'Time of Execution', so RTOE is proably
    'Request Time of Execution' and RID would be 'Request Identifier'.
    """
    s = _as_string(handle.read())
    i = s.find("RID =")
    if i == -1:
        rid = None
    else:
        j = s.find("\n", i)
        rid = s[i+len("RID ="):j].strip()

    i = s.find("RTOE =")
    if i == -1:
        rtoe = None
    else:
        j = s.find("\n", i)
        rtoe = s[i+len("RTOE ="):j].strip()

    if not rid and not rtoe:
        #Can we reliably extract the error message from the HTML page?
        #e.g.  "Message ID#24 Error: Failed to read the Blast query:
        #       Nucleotide FASTA provided for protein sequence"
        #or    "Message ID#32 Error: Query contains no data: Query
        #       contains no sequence data"
        #
        #This used to occur inside a <div class="error msInf"> entry:
        i = s.find('<div class="error msInf">')
        if i != -1:
            msg = s[i+len('<div class="error msInf">'):].strip()
            msg = msg.split("</div>",1)[0].split("\n",1)[0].strip()
            if msg:
                raise ValueError("Error message from NCBI: %s" % msg)
        #In spring 2010 the markup was like this:
        i = s.find('<p class="error">')
        if i != -1:
            msg = s[i+len('<p class="error">'):].strip()
            msg = msg.split("</p>",1)[0].split("\n",1)[0].strip()
            if msg:
                raise ValueError("Error message from NCBI: %s" % msg)
        #Generic search based on the way the error messages start:
        i = s.find('Message ID#')
        if i != -1:
            #Break the message at the first HTML tag
            msg = s[i:].split("<",1)[0].split("\n",1)[0].strip()
            raise ValueError("Error message from NCBI: %s" % msg)
        #We didn't recognise the error layout :(
        #print s
        raise ValueError("No RID and no RTOE found in the 'please wait' page, "
                         "there was probably an error in your request but we "
                         "could not extract a helpful error message.")
    elif not rid:
        #Can this happen?
        raise ValueError("No RID found in the 'please wait' page."
                           " (although RTOE = %s)" % repr(rtoe))
    elif not rtoe:
        #Can this happen?
        raise ValueError("No RTOE found in the 'please wait' page."    +                  " (although RID = %s)" % repr(rid))

    try:
        return rid, int(rtoe)
    except ValueError:
        raise ValueError("A non-integer RTOE found in "  +"the 'please wait' page, %s" % repr(rtoe))






a=10
if a>15:
    if a>20:
        print "A";
    else:
        print("B");



