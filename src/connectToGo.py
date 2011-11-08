
import urllib, urllib2
import time
import sys
try:
    from cStringIO import StringIO ;
except ImportError:
    from StringIO import StringIO ;
    
from Bio._py3k import _as_string ;


# Format the "Put" command, which sends search requests to qblast.
# Parameters taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node5.html on 9 July 2007
# Additional parameters are taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node9.html on 8 Oct 2010
# To perform a PSI-BLAST or PHI-BLAST search the service ("Put" and "Get" commands) must be specified
# (e.g. psi_blast = NCBIWWW.qblast("blastp", "refseq_protein", input_sequence, service="psi"))
#program = 'blastn';
#database = "nt";
#sequence = "8332116";

        

## test GO
sequence = "8332116";
sequence = "GO:0006468";
sequence = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALK";
sequence = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALKRKQRLRLPEWVKTDVPAGKNFARIKGNLRDLKLHTVCEEARCPNIGECWGGAEGTATATIMLMGDECTRGCRFCSIKTNKAPAPLDVDEPAHTAAAVAAWGLDYVVLTSVDRDDLPDGGSNHFASTVIELKKRKPEILVECLTPDFSGVYEDIARVAVSGLDVFAHNMETVESLTPSVRD";
#"P55269";

parameters = [
    ('action','blast'),
    ('seq',sequence),
    #('seq_id','FB:FBgn0015946'),
    ('CMD', 'Put'),
];

## query = [x for x in parameters ];
query = parameters;
message = urllib.urlencode(query);

GOBlast = "http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi";
request = urllib2.Request(GOBlast, message, {"User-Agent":"BiopythonClient"});
# http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi?action=blast&seq_id=FB:FBgn0015946&session_id=9173amigo1320696173
handle = urllib2.urlopen(request);

#handle = urllib2.urlopen("http://amigo.geneontology.org/cgi-bin/amigo/term_details?term=GO:0022008")

s = _as_string(handle.read())
save_file = open("testMulti.html", "w")
save_file.write(s)  
save_file.close()

key = "Sequences producing High-scoring Segment Pairs"
keyIndex = s.index(key)
endIndex = s.index("<span id=", keyIndex)
s2 = s[keyIndex:endIndex].strip()
#<a href="#UniProtKB:Q5BIP7">UNIPROTKB|Q5BIP7</a> - symbol:LIAS "Lipoyl synthase, mitochon...   723  1.4e-71   1
lines = s2.splitlines()

#lines2 = s2.split("\n<a href=")
import re;  ## reuglar expression

accID, matchID, eValue = [], [], [];
MATCH_HREF = "<a href=\"#";
MATCH_HREF_LEN = len(MATCH_HREF);
MATCH_END_HREF = "\">";
MATCH_END_HREF_LEN = len(MATCH_END_HREF); 
## can remove i
for i,l in enumerate(lines):
    if l.find(MATCH_HREF) != -1:
        #l.split(" ")
        print l;
        token = re.split("\s{2,}",l)
        if len(token) != 4:
            print len(token), 
            break;
        start = token[0].find(MATCH_HREF)+MATCH_HREF_LEN;
        mid = token[0].find(MATCH_END_HREF);
        end = token[0].find("</a>");
        accID.append(token[0][start:mid]);
        matchID.append(token[0][mid+MATCH_END_HREF_LEN:end]);
        eValue.append(token.pop(len(token)-2)); ## or call pop() twice


for m in matchID:
    i = s.find(m);
    print q, m, s[i:i+50];
    q=q+1;





#### get actual GO terms
for i, eachID in enumerate(accID):

parameters2 = [
    ('gp',eachID),
    ('CMD', 'Put')];
message = urllib.urlencode(parameters2);
#http://amigo.geneontology.org/cgi-bin/amigo/gp-assoc.cgi?gp=UniProtKB:Q5BIP7&session_id=1671amigo1320698330
GOAssoc = "http://amigo.geneontology.org/cgi-bin/amigo/gp-assoc.cgi";
request = urllib2.Request(GOAssoc, message, {"User-Agent":"BiopythonClient"});

handle = urllib2.urlopen(request);
goID = _as_string(handle.read())

save_file = open("testGetID.html", "w")
save_file.write(goID)  
save_file.close()





## from gp-assoc.cgi
GO:0006954 : inflammatory response   biological process     
GO:0001843 : neural tube closure     biological process     
GO:0032496 : response to lipopolysaccharide  biological process     
GO:0006979 : response to oxidative stress    biological process     
GO:0005739 : mitochondrion   cellular component     
GO:0051539 : 4 iron, 4 sulfur cluster binding    molecular function     
GO:0016992 : lipoate synthase activity   molecular function     
GO:0046872 : metal ion binding   molecular function     
GO:0016740 : transferase activity

## from blast result, this should have everything, parse this
symbol:LIAS "Lipoyl synthase, mitochondrial" species:9913
"Bos taurus" 
[GO:0001843 "neural tube closure" evidence=IEA]
[GO:0005739 "mitochondrion" evidence=IEA] 
[GO:0006954 "inflammatory response" evidence=IEA] 
[GO:0006979 "response to oxidative stress" evidence=IEA] 
[GO:0016740 "transferase activity" evidence=IEA]
[GO:0016992 "lipoate synthase activity" evidence=IEA] 
[GO:0032496 "response to lipopolysaccharide" evidence=IEA] 
[GO:0046872 "metal ion binding" evidence=IEA] 
[GO:0051539 "4 iron, 4 sulfur clusterbinding" evidence=IEA] 
InterPro:IPR003698
InterPro:IPR006638
InterPro:IPR007197 
InterPro:IPR013785 
Pfam:PF04055
PIRSF:PIRSF005963 SMART:SM00729 PANTHER:PTHR10949 GO:GO:0005739
Gene3D:G3DSA:3.20.20.70 GO:GO:0046872 GO:GO:0051539 GO:GO:0016992
TIGRFAMs:TIGR00510 EMBL:BT021177 IPI:IPI00718348
RefSeq:NP_001017944.1 UniGene:Bt.9756 ProteinModelPortal:Q5BIP7
STRING:Q5BIP7 PRIDE:Q5BIP7 Ensembl:ENSBTAT00000019299 GeneID:530865
KEGG:bta:530865 CTD:11019 GeneTree:ENSGT00390000006234
HOVERGEN:HBG023328 InParanoid:Q5BIP7 OMA:SWGLDYI PhylomeDB:Q5BIP7
Uniprot:Q5BIP7
Length = 372

## header)
CTD:11019
EMBL:BT021177
Ensembl:ENSBTAT00000019299
Gene3D:G3DSA:3.20.20.70
GeneID:530865
GeneTree:ENSGT00390000006234
HOVERGEN:HBG023328
InParanoid:Q5BIP7
InterPro:IPR003698
InterPro:IPR006638
InterPro:IPR007197
InterPro:IPR013785
IPI:IPI00718348
KEGG:bta:530865
OMA:SWGLDYI
PANTHER:PTHR10949
Pfam:PF04055
PhylomeDB:Q5BIP7
PIRSF:PIRSF005963
PRIDE:Q5BIP7
ProteinModelPortal:Q5BIP7
RefSeq:NP_001017944.1
SMART:SM00729
STRING:Q5BIP7
TIGRFAMs:TIGR00510
UniGene:Bt.9756
Uniprot:Q5BIP7



####
## alternative way to go throught lines
#for l in lines:
#if l.find("<a href=\"#") != -1:
#l.split(" ")
#print l;

#for i in range(len(lines)):
    #print i, lines[i]

##################### others functions
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


















##### Functions from other places
#####

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



