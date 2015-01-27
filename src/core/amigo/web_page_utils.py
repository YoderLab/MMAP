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


DELAY = 5.0


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

# @retry(urllib2.URLError, tries=4, delay=3, backoff=2)


def get_web_page(query, URL):

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
