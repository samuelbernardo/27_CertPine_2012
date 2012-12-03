#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This is a script to test the connecting capabilities of the psycopg2 library
'''


import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(host='db.ist.utl.pt', user='ist153890', password='thlt7466') 
    cur = con.cursor()
    cur.execute('SELECT * FROM inquerito')          
    ver = cur.fetchall()
    print ver    
    

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
