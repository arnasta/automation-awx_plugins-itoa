# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: ip_to_vserver
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: 1.1.9
  short_description: This plugin resolves what NetScaler Application Delivery Controllers are servicing url
  description:
      - This lookup returns list of NetScaler devices and associated vservers.
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.10).
      - To install it, use C(ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git).
      - You'll also want to create C(collections/requirements.yml) in your AWX playbook that 
        contains this content
  options:
    _terms:
      description: url in form of https://my.url.com
      required: True
    adm_hostname:
      description: Hostname of ADM
      default: 'mas.myabcit.net'
      type: string
      ini:
        - section: ip_to_vserver
          key: adm_hostname
    username:
      description:
        - Name of user for connection to ADM.
        - If the value is not specified, the value of environment variable C(ADM_USERNAME) will be used instead.
      required: true
      type: str
      env:
        - name: ADM_USERNAME
    password:
      description:
        - Password for user.
        - If the value is not specified, the value of environment variable C(ADM_PASSWORD) will be used instead.
      required: true
      type: str
      env:
        - name: ADM_PASSWORD
    protocol:
      description: Protocol for vserver IP lookup
      default: 'SSL'
      type: string
      ini:
        - section: ip_to_vserver
          key: protocol
"""

EXAMPLES = r"""
---
collections:
  - name: cencora.itoa
    type: git
    source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
    version: 1.1.9
---
- hosts: localhost
  connection: local
  gather_facts: true
  collections:
    - cencora.itoa
  vars:
    input_url: "https://cencora.com/"
    vservers: "{{ lookup('cencora.itoa.ip_to_vserver', input_url, username=username, password=password) }}"
  tasks:
    - debug:
        msg: "vservers for {{ input_url }} are {{ vservers }}"
"""

RETURN = r"""
returned_value:
  description: List of vserver objects in NetScaler
  returned: always
  type: list
  elements: dict
  sample:
    - name: "www.amerisourcebergen.com-443_cs"
      type: "SSL"
      load_balancer:"LADC-PFE02.myabcit.net"
      ip_address: "209.182.164.44"
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import requests
from requests.auth import HTTPBasicAuth
import ipaddress

display = Display()

api_path = '/nitro/v1/config/'
adm_lbvservers_endpoint = api_path + 'ns_lbvserver'
adm_csvservers_endpoint = api_path + 'ns_csvserver'

def api_call(url, auth):
    display.vv(f"Fetching info from {url}")
    response = requests.get(url, auth=auth, verify=False)
    display.vvv(f"Response status code {str(response.status_code)}")
    if response.status_code != 200:
        raise AnsibleError(f"http error : {response.status_code}: {response.text}")
    return response.json()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        adm_hostname = 'https://' + self.get_option('adm_hostname')
        adc_domain = '.'.join(self.get_option('adm_hostname').split('.')[-2:])
        username = self.get_option('username')
        password = self.get_option('password')
        protocol = self.get_option('protocol')
        auth = HTTPBasicAuth(username, password)
        ret = []
        for term in terms:
            display.v("ip_to_vserver lookup term: %s" % term)
            if isinstance(term, str):
                try:
                    ip_address = ipaddress.ip_address(term)
                    display.v(f'{ip_address} is a correct IP{ip_address.version} address.')
                except ValueError:
                    display.v(f'IP address is invalid: {term}')
                ret_list = []
                cs_vservers = api_call(adm_hostname + adm_csvservers_endpoint + '?filter=vsvr_ip_address:' + str(ip_address) + ',vsvr_type:' + protocol, auth).get('ns_csvserver', [])
                vserver_type = 'cs'
                vserver = next(iter(cs_vservers), '')
                if not vserver:
                    lb_vservers = api_call(adm_hostname + adm_lbvservers_endpoint + '?filter=vsvr_ip_address:' + str(ip_address) + ',vsvr_type:' + protocol, auth).get('ns_lbvserver', [])
                    vserver = next(iter(lb_vservers), '')
                    vserver_type = 'lb'
                if vserver:
                    ret_list.append({'name': vserver['name'], 'type': vserver_type, 'load_balancer': vserver['hostname'] + '.' + adc_domain, 'ip_address': str(ip_address)})
                else:
                    display.vv(f"No lb or cs vservers found on ADM")
                ret.append(ret_list)
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
        return ret