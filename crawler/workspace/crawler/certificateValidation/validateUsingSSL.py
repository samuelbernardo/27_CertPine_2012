import socket
import ssl

HOST = "www.bpinet.pt"
PORT = 443

# replace HOST name with IP, this should fail connection attempt
#HOST = socket.getaddrinfo(HOST, PORT)[0][4][0]
print(HOST)

# create socket and connect to server
# server address is specified later in connect() method
sock = socket.socket()
sock.connect((HOST, PORT))

# wrap socket to add SSL support
sock = ssl.wrap_socket(sock,
  # flag that certificate from the other side of connection is required
  # and should be validated when wrapping 
  cert_reqs=ssl.CERT_REQUIRED,
  # file with root certificates
  ca_certs="cacert.pem"
)

# security hole here - there should be an error about mismatched host name
# manual check of hostname
cert = sock.getpeercert()
for field in cert['subject']:
  if field[0][0] == 'commonName':
    certhost = field[0][1]
    if certhost != HOST:
      raise ssl.SSLError("Host name '%s' doesn't match certificate host '%s'"
                         % (HOST, certhost))
    else:
        print 'Success'