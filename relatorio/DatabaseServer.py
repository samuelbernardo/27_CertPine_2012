import sys
import BaseHTTPServer
import SimpleHTTPServer
import cgi
import pprint
import psycopg2


from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler

'''
This script launches a server that expects http POST requests
Crawler.py will connect to it and send a POST Request for every certificate e finds
to launch: python DatabaseServer.py [port]
it will print the SQL querries
it will make these querries vefore sendind '200 OK' to the Crawler.py
'''


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        print "GET Path: ", self.path
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print "Serving a crawler..."
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        #for item in form.list:
        #    print item
        pack = dict()
    
        pack['issuerName'] = form.getvalue('issuerName')
        pack['subjectName'] = form.getvalue('subjectName')
        pack['serialNumber'] = form.getvalue('serialNumber')
        pack['version'] =form.getvalue('version')
        pack['beforeDate'] = form.getvalue('beforeDate')
        pack['afterDate'] = form.getvalue('afterDate')
        
        updateSQL(pack)
        
        self.send_response( 200 )
        body = "%s was updated!" % form.getvalue('subjectName')
        self.send_header( "Content-type", type )
        self.send_header( "Content-length", str(len(body)) )
        self.end_headers()
        self.wfile.write( body )
        
        
def updateSQL(pack):
    con = None
    try:
        con = psycopg2.connect(host='db.ist.utl.pt', user='ist153890', password='thlt7466') 
        cur = con.cursor()
        
        querry = "INSERT INTO certs values('%s', '%s', '%s', '%s', '%s', %d, %d);" % (pack['serialNumber'], 
                           pack['issuerName'],
                           pack['subjectName'], 
                           pack['beforeDate'], 
                           pack['afterDate'],
                           1,
                           1)
                        
        print querry
        
        cur.execute(querry)    
        con.commit()      
        #ver = cur.fetchall()
        #print ver   
    except psycopg2.DatabaseError as e:
        print 'Error %s' % e    
        sys.exit(1)   
    finally:
        if con:
            con.close()
    return

if __name__ == '__main__':
    #HandlerClass = SimpleHTTPRequestHandler
    HandlerClass = ServerHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    #ServerClass = MyLoggingHTTPRequestHandler
    Protocol     = "HTTP/1.1"
    
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8000
    server_address = ('', port)
    
    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)
    
    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."   
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
