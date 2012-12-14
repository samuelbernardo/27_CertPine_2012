import ssl, socket, pprint
import httplib, urllib
import datetime
import OpenSSL
from sys import argv

'''
Just launch it and it will go thorugh the domain_list and get the certificate from every domain
and send a post request to DatabaseServer.py
python Crawler.py [host] [port]
'''

host = "127.0.0.1"
port = 8000

domain_list = ['www.bpinet.pt', 
               'www.google.com', 
               'www.ist.utl.pt',
               'www.viaforensics.com']

'''
Converts the date from the stupid format that OpenSSL returns
into a datetime object
'''
def convertX509Date(date):
    return datetime.datetime.strptime(date, "%Y%m%d%H%M%SZ")

'''
Converts the datetime to a ISO format string
'''
def convertDate(date):
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

'''
given an argument in the form of a domain this method will get 
it's certificate
'''
def getServerCertificate(domainName):
    print "Get Certificate from: %s" % domainName
    cert = ssl.get_server_certificate((domainName,443))
    return cert

'''
This method will print relevant info and send it to the server
'''
def parseCert(cert):
    #print cert
    #print "length: ", cert.__len__()
    X509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    #issuer
    '''print "\tIssuer: \t\t",
    print X509.get_issuer().commonName
    print "Organization Name: \t\t",
    print X509.get_issuer().organizationName
    print "Organizational Unit Name: \t",
    print X509.get_issuer().organizationalUnitName
    print "Email Adress: \t\t\t",
    print X509.get_issuer().emailAddress
    print "Country Name: \t\t\t",
    print X509.get_issuer().countryName
    print "State Name: \t\t\t",
    print X509.get_issuer().stateOrProvinceName
    print "Locality Name: \t\t\t",
    print X509.get_issuer().localityName
    print ""
    print "\tPubkey: ",
    print X509.get_pubkey().bits()
    #print ""
    #print "Signature Algorithm: ",
    #print X509.get_signature_algorithm()
    #print ""
    #subject
    print "\tSubject: \t\t",
    print X509.get_subject().commonName
    print "Organization Name: \t\t",
    print X509.get_subject().organizationName
    print "Organizational Unit Name: \t",
    print X509.get_subject().organizationalUnitName
    print "Email Adress: \t\t\t",
    print X509.get_subject().emailAddress
    print "Country Name: \t\t\t",
    print X509.get_subject().countryName
    print "State Name: \t\t\t",
    print X509.get_subject().stateOrProvinceName
    print "Locality Name: \t\t\t",
    print X509.get_subject().localityName
    print ""
    print "\tSerial Number: \t\t",
    print X509.get_serial_number()
    #print ""
    print "\tCertificate Version: \t",
    print X509.get_version()
    #print ""
    print "\tNot Before Date: \t",
    print convertX509Date(X509.get_notBefore())
    #print ""
    print "\tNot After Date: \t",
    print convertX509Date(X509.get_notAfter())
    print ""'''
    
    pack = dict()
    
    pack['issuerName'] = X509.get_issuer().commonName
    pack['subjectName'] = X509.get_subject().commonName
    pack['serialNumber'] = X509.get_serial_number()
    pack['version'] =X509.get_version()
    pack['beforeDate'] = convertX509Date(X509.get_notBefore()).isoformat()
    pack['afterDate'] = convertX509Date(X509.get_notAfter()).isoformat()
    
    pprint.pprint(pack, indent=2)
    
    return pack

def updateDB(pack):
    params = urllib.urlencode(pack)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection(host,port)
    
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    data = response.read()
    print "Server Response: %s %s %s" %(response.status, response.reason, data)
    conn.close()
    return

if __name__ == '__main__':
	
	
	
	if sys.argv[1:]:
        host = int(sys.argv[1])
    else:
        host = '127.0.0.1'
    
    if sys.argv[2:]:
        port = int(sys.argv[2])
    else:
        port = 8000
	
    for item in domain_list:
        cert = getServerCertificate(item)
        pack = parseCert(cert)
        updateDB(pack)
        print ""







