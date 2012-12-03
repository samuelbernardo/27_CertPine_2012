import datetime
import simplejson as json

'''
Testing the constructin of a structure to be sent in TCP/json that includes the information about the certificate checked
'''

t = dict()
t['serialNumber'] = 144082741558875710455667109925152810750
t['subjectName'] = 'www.bpinet.pt'
t['beforeDate'] = datetime.datetime(2012, 1, 6, 0, 0, 0).isoformat()
t['afterDate'] = datetime.datetime(2013, 4 , 6, 23, 59, 59).isoformat()


test = json.dumps(t, indent = 4)

print test

result = json.loads(test)

print result

result['beforeDate'] = datetime.datetime.strptime(result['beforeDate'], "%Y-%m-%dT%H:%M:%S")

result['afterDate'] = datetime.datetime.strptime(result['afterDate'], "%Y-%m-%dT%H:%M:%S")

for i,j in result.items():
    print "key: ",i,"\tvalue: ", j