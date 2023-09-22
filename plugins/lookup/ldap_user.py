from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
  name: ldap_user
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  short_description: This plugin gets host info from ldap
  requirements:
      - python ldap3
  version_added: 1.1.6
  description:
      - This lookup returns user info from ldap server
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.6).
      - To install it, use C(ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git).
      - You'll also want to create C(collections/requirements.yml) in your AWX playbook that 
        contains this content
  options:
      _terms:
          description: server hostname
          required: True
      server:
          description: LDAP server address
          default: 'abcldap.abc.amerisourcebergen.com'
          type: string
          ini:
              - section: ldap_host_lookup
                key: server
      base_dn:
          description: base dn for user search
          default: ''
          type: string
          ini:
              - section: ldap_host_lookup
                key: server_base_dn
      username:
          description:
              - Name of user for connection to LDAP.
              - If the value is not specified, the value of environment variable C(LDAP_USERNAME) will be used instead.
          required: true
          type: str
          env:
              - name: LDAP_USERNAME
      password:
          description:
              - Password for username.
              - If the value is not specified, the value of environment variable C(LDAP_PASSWORD) will be used instead.
          required: true
          type: str
          env:
              - name: LDAP_PASSWORD
      attributes:
          description:
              - A list of object attributes to return
          type: list
          default: 'c,cn,co,company,department,displayName,distinguishedName,employeeNumber,givenName,info,l,lastLogon,mail,manager,mobile,name,physicalDeliveryOfficeName,sAMAccountName,sn,streetAddress,title,userPrincipalName'
'''

EXAMPLES = r"""
---
collections:
  - name: cencora.itoa
    type: git
    source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
    version: 1.1.6
---
- name: Get user info from LDAP
  hosts: 127.0.0.1
  gather_facts: false
  become: false
  collections:
    - cencora.itoa
  vars:
    user_id: 'a132171'
    username: 'a132171'
    password: 'mypass'
    user_info: "{{ lookup('cencora.itoa.ldap_host', user_id, username=username, password=password) }}"
  tasks:
    - debug:
        msg:
          - "{{user_id}}: {{ user_info }}"
"""

RETURN = r"""
users:
  description: info from group search
  returned: always
  type: list
  elements: dict
  sample:
    - c: 'US'
      cn: 'John, Doe (a123456_tr1)'
      co: 'United States of America'
      company: 'AmerisourceBergen Drug Corporation'
      department: 'Foundation Reliability'
      displayName: 'a123456_tr1'
      distinguishedName:  'CN=John\, Doe (a123456_tr1),OU=Accounts,OU=Tier1,OU=Admin,DC=abc,DC=amerisourcebergen,DC=com'
      employeeNumber: '123456'
      givenName: 'John'
      info: 'This Account was created by an automated process via MYID'
      l: 'Middle of Nowhere'
      lastLogon: '9/20/2023 10:47:19 AM Eastern Daylight Time'
      mail: 'a123456_tr1@amerisourcebergen.com'
      manager: 'CN=Mr.\, T (a000001),OU=Enterprise,OU=ABCUsers,DC=abc,DC=amerisourcebergen,DC=com'
      mobile: '01234567890'
      name: 'John, Doe (A123456)'
      physicalDeliveryOfficeName: 'USA Remote - Middle of Nowhere'
      sAMAccountName: 'a123456'
      sn: 'Doe'
      streetAddress: 'Mulholland Drive 42'
      title: 'IT Operations Automation Developer'
      userPrincipalName: 'a123456@amerisourcebergen.com'
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ldap3 import Server, Connection, SAFE_SYNC, ALL, NTLM, utils
import datetime

display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        server = self.get_option('server')
        base_dn = self.get_option('base_dn')
        if not base_dn:
            base_dn = 'DC=' + ',DC='.join(server.split('.')[1:])
        username = self.get_option('username')
        password = self.get_option('password')
        attributes = self.get_option('attributes')
        ldapServer = Server(self.get_option('server'), get_info=ALL)
        display.vvv(f"Connecting to LDAP server: {server} ...")
        c = Connection(ldapServer, user=username, password=password, authentication=NTLM, auto_bind=True)
        ret = []
        for term in terms:
            user_list = list()
            display.vvv(f"Searching (&(objectClass=person)(name=*{utils.conv.escape_filter_chars(term)}*))")
            c.search(search_base = base_dn, search_filter = f'(&(objectClass=person)(name=*{utils.conv.escape_filter_chars(term)}*))', attributes = attributes)
            for entry in c.response:
                if entry['type'] != 'searchResRef':
                    user_info = dict()
                    for attribute in entry['attributes']:
                        if entry['attributes'][attribute]:
                            if isinstance(entry['attributes'][attribute], datetime.datetime):
                                user_info[attribute] = str(entry['attributes'][attribute])
                            else:
                                user_info[attribute] = entry['attributes'][attribute]
                    user_list.append(user_info)
            if user_list:
                ret.append({'users': user_list})
            else:
                ret.append({})
        return ret