import socket
from whois import NICClient
from parser import WhoisEntry

def get_data_from_host(host):
    flags = 0
    nic_client = NICClient()
    
    data = nic_client.whois_lookup(None, host, flags)
    w = WhoisEntry.load(host, data)
    
    keys_to_test = ['domain_name', 'expiration_date', 'updated_date', 'creation_date', 'status']
    
    results = {}
    for key in keys_to_test:
        results[key] = w.__getattr__(key)
        
    print repr(get_ips_for_host(host))
    
    for key in keys_to_test:
        print "%s: %s" % (key, results[key])  

def get_ips_for_host(host):
    try:
        ips = socket.gethostbyname_ex(host)
    except socket.gaierror:
        ips=[]
    return ips

get_data_from_host('bpinet.pt')
    