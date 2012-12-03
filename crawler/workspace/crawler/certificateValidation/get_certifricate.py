import ssl, socket, pprint
import OpenSSL
from sys import argv

script, host = argv

'''
given an argument in the form of a domain this script will get 
it's certificate and print all the information available
'''

cert = ssl.get_server_certificate((host,443))

print cert

X509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

#issuer
print "\nIssuer: "
print "Common Name: \t\t\t",
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
print "Pubkey: ",
print X509.get_pubkey().bits()
print ""
print "Serial Number: ",
print X509.get_serial_number()
print ""
#print "Signature Algorithm: ",
#print X509.get_signature_algorithm()
#print ""
#subject
print "Subject: "
print "Common Name: \t\t\t",
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
print "Certificate Version: ",
print X509.get_version()
print ""
print "Not Before Date: ",
print X509.get_notBefore()
print ""
print "Not After Date: ",
print X509.get_notAfter()
print ""


