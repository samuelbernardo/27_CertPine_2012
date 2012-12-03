import simplejson as json

data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
print 'DATA:', repr(data)
print 'repr(data)             :', repr(data)
print 'dumps(data)            :', json.dumps(data)
print 'dumps(data, indent=2)  :', json.dumps(data, indent=2)
print 'dumps(data, separators):', json.dumps(data, separators=(',',':'))

