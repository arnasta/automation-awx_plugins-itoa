from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
  name: sccm_host
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  short_description: This plugin gets host info from sccm
  requirements:
      - python requests
      - python requests_ntlm
  version_added: 1.1.3
  description:
      - This lookup returns host information from SCCM server
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.8).
      - To install it, use C(ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git).
      - You'll also want to create C(collections/requirements.yml) in your AWX playbook that 
        contains this content
  options:
      _terms:
          description: server hostname
          required: True
      server:
          description: SCCM server address
          default: 'svrsccm1p001.abc.amerisourcebergen.com'
          type: string
          ini:
              - section: sccm_host_lookup
                key: server
      fields:
          description: Fields from SCCM to fetch
          type: list
          ini:
              - section: sccm_host_lookup
                key: fields
      username:
          description:
              - Name of user for connection to SCCM.
              - If the value is not specified, the value of environment variable C(SCCM_USERNAME) will be used instead.
          required: true
          type: str
          env:
              - name: SCCM_USERNAME
      password:
          description:
              - Password for username.
              - If the value is not specified, the value of environment variable C(SCCM_PASSWORD) will be used instead.
          required: true
          type: str
          env:
              - name: SCCM_PASSWORD
'''

EXAMPLES = r"""
---
collections:
  - name: cencora.itoa
    type: git
    source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
    version: 1.1.8
---
- name: Get host info from SCCM
  hosts: 127.0.0.1
  gather_facts: false
  become: false
  collections:
    - cencora.itoa
  vars:
    server_name: 'test01.abc.amerisourcebergen.com'
    username: 'a132171'
    password: 'mypass'
    host_info: "{{ lookup('cencora.itoa.sccm_host', server_name, username=username, password=password) }}"
  tasks:
    - debug:
        msg:
          - "{{server_name}}: {{ host_info }}"
"""

RETURN = r"""
MachineId:
    description: MachineId
    returned: when supported
    type: integer
    sample: 16777222
Name:
    description: hostname
    returned: when supported
    type: string
    sample: "SVRSCM2P002"
Domain:
    description: Domain name
    returned: when supported
    type: string
    sample: "CFD"
IsVirtualMachine:
    description: Virtual machine flag
    returned: when supported
    type: boolean
    sample: true
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import requests
import urllib.parse
from requests_ntlm import HttpNtlmAuth

display = Display()

def api_call(auth, endpoint, filter, fields):
    if fields:
        fields = '$select=' + ','.join([urllib.parse.quote(field) for field in fields])
    if filter:
        filter = '$filter=' + urllib.parse.quote(filter)
    if fields and filter:
        url = f"{endpoint}?{fields}&{filter}"
    elif fields:
        url = f"{endpoint}?{fields}"
    elif filter:
        url = f"{endpoint}?{filter}"
    else:
        url = f"{endpoint}"   
    display.vvv(f"Feching host info from {url}")
    response = requests.get(url, auth=auth, verify=False)
    display.vvv(f"Response status code {str(response.status_code)}")
    if response.status_code != 200:
        raise AnsibleError(f"http error : {response.status_code}: {response.text}")
    results = response.json()
    display.vvv(f"{str(len(results['value']))} host(s) found")
    if results['value']:
        return results['value'][0]
    else:
        return dict()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        server = 'https://' + self.get_option('server')
        fields = self.get_option('fields')
        username = self.get_option('username')
        password = self.get_option('password')
        ret = []
        for term in terms:
            ntlm_auth = HttpNtlmAuth(username, password)
            sccm_info = api_call(ntlm_auth, server + "/AdminService/v1/Device", f"Name eq '{term}'", fields)
            system_info = api_call(ntlm_auth, server + "/AdminService/wmi/SMS_R_System", f"name eq '{term}'", fields)
            sccm_info.update(system_info)
            ret.append(sccm_info)
        return ret