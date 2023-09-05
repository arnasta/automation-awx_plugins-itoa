from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
  name: ldap_host
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  short_description: This plugin gets host info from ldap
  requirements:
      - python ldap3
  version_added: 1.1.4
  description:
      - This lookup returns a dictionary of host info from ldap server
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.4).
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
      server_base_dn:
          description: base dn for servers
          default: 'OU=ABCServers,DC=abc,DC=amerisourcebergen,DC=com'
          type: string
          ini:
              - section: ldap_host_lookup
                key: server_base_dn
      group_base_dn:
          description: base dn for groups
          default: 'DC=abc,DC=amerisourcebergen,DC=com'
          type: string
          ini:
              - section: ldap_host_lookup
                key: group_base_dn
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
              - A list of object attributes to return (both computer and group)
          type: list
          default: 'cn,description,distinguishedName,dNSHostName,lastLogonTimestamp,objectGUID,objectSid,operatingSystem,operatingSystemVersion,primaryGroupID'
'''

EXAMPLES = r"""
---
collections:
  - name: cencora.itoa
    type: git
    source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
    version: 1.1.4
---
- name: Get host info from LDAP
  hosts: 127.0.0.1
  gather_facts: false
  become: false
  collections:
    - cencora.itoa
  vars:
    server_name: 'test01.abc.amerisourcebergen.com'
    username: 'a132171'
    password: 'mypass'
    host_info: "{{ lookup('cencora.itoa.ldap_host', server_name, username=username, password=password) }}"
  tasks:
    - debug:
        msg:
          - "{{server_name}}: {{ host_info }}"
"""

RETURN = r"""
computer_info:
  description: info from computer search
  returned: always
  type: dict
  contains:
    distinguishedName:
      description: unique attribute in LDAP that hierarchically identifies an entry within the directory tree
      returned: when supported
      type: string
      sample: "CN=MyComputer,OU=Computers,DC=example,DC=com"
    dNSHostName:
      description: contains the FQDN of a computer, which includes the hostname and the complete domain name
      returned: when supported
      type: string
      sample: "mycomputer.example.com"
    lastLogonTimestamp:
      description: date when a computer account logged onto the domain
      returned: when supported
      type: string
      sample: "8/31/2023 11:37:15 PM Eastern Daylight Time"
    objectGUID:
      description: a 128-bit value that is globally unique across all LDAP directories
      returned: when supported
      type: string
      sample: "12345678-9abc-def0-1234-56789abcdef0"
    objectSid:
      description: security identifier for security principals within an Active Directory environment,
      returned: when supported
      type: string
      sample: "S-1-5-21-3623811015-3361044348-30300820-1013"
    operatingSystem:
      description: Operating System of the computer
      returned: when supported
      type: string
      sample: "Red Hat Enterprise Linux release 9.1"
    operatingSystemVersion:
      description: Operating System version
      returned: when supported
      type: string
      sample: "Linux 4.18.0-193.14.3.el8_2.x86_64"
    primaryGroupID:
      description: used to specify the primary group for a user account
      returned: when supported
      type: string
      sample: "513 = ( GROUP_RID_COMPUTERS )"
group_info:
  description: info from group search
  returned: always
  type: list
  elements: dict
  sample:
    - cn: 'prd_access_localadm_mycomputer'
      description: 'Local Admin Access to Server mycomputer'
      distinguishedName: 'CN=prd_access_localadm_mycomputer,OU=Server,OU=Access,OU=Enterprise,OU=ABCGroups,DC=abc,DC=amerisourcebergen,DC=com'
      objectGUID: '12345678-9abc-def0-1234-56789abcdef0'
      objectSid: 'S-1-5-21-3623811015-3361044348-30300820-1013'
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ldap3 import Server, Connection, SAFE_SYNC, ALL, NTLM, utils

display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        server = self.get_option('server')
        server_base_dn = self.get_option('server_base_dn')
        group_base_dn = self.get_option('group_base_dn')
        username = self.get_option('username')
        password = self.get_option('password')
        attributes = self.get_option('attributes')
        ldapServer = Server(self.get_option('server'), get_info=ALL)
        self.display.vvv(f"Connecting to LDAP server: {server} ...")
        c = Connection(ldapServer, user=username, password=password, authentication=NTLM, auto_bind=True)
        ret = []
        for term in terms:
            c.search(search_base = server_base_dn, search_filter = f'(&(objectClass=computer)(name={utils.conv.escape_filter_chars(term)}))', attributes = attributes)
            computer_info = c.response[0]
            c.search(search_base = group_base_dn, search_filter = f'(&(objectClass=group)(cn=*{utils.conv.escape_filter_chars(term)}*))', attributes = attributes)
            group_info = c.response
            ret.append({'computer_info': computer_info, 'group_info': group_info})
        return ret