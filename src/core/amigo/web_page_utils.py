"""
Created on Jan 8, 2015

@author: Steven Wu
"""
import socket
import urllib
from urllib2 import URLError
import urllib2
import warnings

from cups import HTTPError
import os
import random
import time


DELAY = 5.0
MATCH_BLAST_NOT_COMPLETE = ("Please be patient as your job may take several minutes to complete. This page will automatically refresh with the BLAST results when the job is done.")
AMIGO_BLAST_URL = "http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi"
# http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi




def get_web_page(query, URL):
# #FIXME: Double check the result here
    for _ in range(10):
#     while s is None:
        try:

            message = urllib.urlencode(query)
            rand = random.random()
            request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient"})
#            print "URL:", URL, "\n", message, "\n", request, "\n"
#            print request.get_data()
#            print request.get_full_url()

            handle = urllib2.urlopen(request)
            s = str(handle.read())
            return s

        except URLError, e:
            warnings.warn("URLError::%s" % (e))
            time.sleep(1)

        except socket.timeout as e:
            warnings.warn("socket.timouout::%s" % (e))

        except socket.error as e:
            warnings.warn("socket.error::%s" % (e))
            time.sleep(1)

        except StandardError as e:
            warnings.warn("StandardError::%s" % (e))

        except Exception as e:
            warnings.warn("Exception::%s" % (e))

    return None


# @retry(urllib2.URLError, tries=4, delay=3, backoff=2)
def get_web_page_handle(query, URL, timeout=120):

    # TODO faster? with httplib?
    handle = None
#     print socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    message = urllib.urlencode(query)
#     print message
#     message = message.encode('utf-8')
    request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient Python-urllib2"})
#     print request
#     print request.get_data()
#     print request.get_method()

    while True:
        handle = urllib2.urlopen(request)
        if handle.code > 0:
            break
    return handle


####################################################################
def get_web_page_httplib(connector, query):

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



def get_web_page_handle_file(query, file_name, URL):

    # # This, again, only works on small files < 6**** bp
    handle = None
    a = open(file_name, "r")

    query.append(('seq_file_upload', open(file_name, "r")))
    print query, file_name
    q1 = {'action':'blast', 'CMD':"Put", "seq":">aoeuaoeu\nATGCGTGCATGC"}
    q2 = {'action':'blast', 'CMD':"Put", 'seq_file_upload': 'open(file_name, "r")'}
#     q3 = {'action':'blast', 'CMD':"Put", 'uniprot_id': 'P32246'} # working!
    print q2


    import poster.encode
    import poster.streaminghttp

    opener = poster.streaminghttp.register_openers()

    params = {'seq_file_upload': open(file_name + "A", 'rb'), 'description': 'upload test', 'action':'blast', 'CMD':"Put"}
    datagen, headers = poster.encode.multipart_encode(params)
    print "D", datagen, dir(datagen)
#     print datagen.boundary
#     print datagen.cb
#     print datagen.current
#     print datagen.i
#     print datagen.next
#     print datagen.p
#     print datagen.param_iter
#     print datagen.params
#     print datagen.total
#     print "H", headers
    response = opener.open(urllib2.Request(URL, datagen, headers))

    print response.read()
    message = urllib.urlencode(q2)
    print message
#     print query
#     message = message.encode('utf-8')
# data = urllib.urlencode({'filename': open(uploadfile, "rb"),
#                         'description': 'upload test'})
# post_req = urllib2.Request(upload_file_url, data)
#
# files = {'file': open('image.png', 'rb')}
# r = requests.post(url, files=files)


    request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient Python-urllib2"})
#     print message
#     print request
#     print request.get_data()
#     print request.get_method()
    while True:
        handle = urllib2.urlopen(request)
        if handle.code > 0:
            break
    return handle
