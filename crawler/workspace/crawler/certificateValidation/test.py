import os
import glob
from OpenSSL.SSL import Context, TLSv1_METHOD, VERIFY_PEER, VERIFY_FAIL_IF_NO_PEER_CERT, OP_NO_SSLv2
from OpenSSL.crypto import load_certificate, FILETYPE_PEM
from twisted.python.urlpath import URLPath
from twisted.internet.ssl import ContextFactory
from twisted.internet import reactor
from twisted.web.client import getPage

'''
don't believe it actually works it's just here for the libraries and as an example
'''

certificateAuthorityMap = {}
for certFileName in glob.glob("/etc/ssl/certs/*.pem"):
    # There might be some dead symlinks in there, so let's make sure it's real.
    if os.path.exists(certFileName):
        data = open(certFileName).read()
        x509 = load_certificate(FILETYPE_PEM, data)
        digest = x509.digest('sha1')
        # Now, de-duplicate in case the same cert has multiple names.
        certificateAuthorityMap[digest] = x509
class HTTPSVerifyingContextFactory(ContextFactory):
    def __init__(self, hostname):
        self.hostname = hostname
    isClient = True
    def getContext(self):
        ctx = Context(TLSv1_METHOD)
        store = ctx.get_cert_store()
        for value in certificateAuthorityMap.values():
            store.add_cert(value)
        ctx.set_verify(VERIFY_PEER | VERIFY_FAIL_IF_NO_PEER_CERT, self.verifyHostname)
        ctx.set_options(OP_NO_SSLv2)
        return ctx
    def verifyHostname(self, connection, x509, errno, depth, preverifyOK):
        if preverifyOK:
            if self.hostname != x509.get_subject().commonName:
                return False
        return preverifyOK
def secureGet(url):
    return getPage(url, HTTPSVerifyingContextFactory(URLPath.fromString(url).netloc))
#def done(result):
    #print 'Done!', len(result)
secureGet("https://google.pt/")#.addCallback(done)
