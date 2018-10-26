#!/usr/bin/env python
# Mel 2018-10-26 - search employees in AD ldap

import ldap3
import sys

# be sure and change the next 2 lines from example.com and YourPasswordHere 
server=ldap3.Server('host.example.com',get_info=ldap3.ALL)
conn=ldap3.Connection(server,'cn=Authorized Search,CN=Users,dc=host,dc=example,dc=com','YourPasswordHere',auto_bind=True)
# also change search_base from example.com
searchParameters = { 'search_base': 'dc=host,dc=example,dc=com',
                     'search_filter': '(objectClass=Person)',
                     'attributes': ['cn', 'givenName', 'displayName', 'sn', 'name', 'sAMAccountName', 'userPrincipalName',
                     'mail', 'employeeID', 'manager', 'department', 'company', 'distinguishedName', 'title',
                     'physicalDeliveryOfficeName', 'memberOf', 'description' ],
                     'paged_size': 10 }

while True:
    conn.search(**searchParameters)
    for entry in conn.entries:
        for argument in sys.argv[1:]:
            if argument in str(entry['name']) or argument in str(entry['displayName']) or argument in str(entry['sAMAccountName']) or argument in str(entry['employeeID']):
                print(entry)
    cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
    if cookie:
        searchParameters['paged_cookie'] = cookie
    else:
        break
