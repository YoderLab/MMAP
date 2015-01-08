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
def get_web_page_handle(query, URL):
    # TODO faster? with httplib?
    handle = None
    message = urllib.urlencode(query)
    request = urllib2.Request(URL, message, {"User-Agent": "BiopythonClient"})
#     print message
#     print request
    while True:
        handle = urllib2.urlopen(request)
        if handle.code > 0:
            break
    return handle
