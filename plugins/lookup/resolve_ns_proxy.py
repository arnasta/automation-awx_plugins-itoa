# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: url_to_backend
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: 1.1.9
  short_description: This plugin resolves what NetScaler ADC are servicing url
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
        - section: url_to_backend
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
    ns_proxies: "{{ lookup('cencora.itoa.resolve_ns_proxy', input_url, username=username, password=password) }}"
  tasks:
    - debug:
        msg: "NetScaler proxies for {{ input_url }} are {{ ns_proxies }}"
"""

RETURN = r"""
returned_value:
  description: List of NetScaler proxy dictionaries
  returned: always
  type: list
  elements: dict
  sample:
    - servicegroupname: "www.amerisourcebergen.com_default_sg"
      ip: "20.0.0.0"
      port: 8080
      svrstate: "UP"
      statechangetimesec: "Wed Sep 20 14:41:12 2023"
      tickssincelaststatechange: "187440408"
      weight: "1"
      servername: "20.0.0.0"
      customserverid: "None"
      serverid: "0"
      state: "ENABLED"
      hashid: "0"
      graceful: "NO"
      delay: "0"
      delay1: "0"
      nameserver: "0.0.0.0"
      dbsttl: "0"
      orderstr: "Default"
      trofsdelay: "0"
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
from dns import resolver

display = Display()

api_path = '/nitro/v1/config/'
adm_lbvservers_endpoint = api_path + 'ns_lbvserver'
adm_csvservers_endpoint = api_path + 'ns_csvserver'

def resolve_ip(hostname, nameserver=''):
    ret = []
    res = resolver.Resolver()
    if nameserver:
        display.v(f"Trying to resolve {hostname} using: {nameserver} server")
        res.nameservers = [nameserver]
    try:
        answer = res.query(hostname)
        ips = [ip.to_text() for ip in answer]
        display.v(f"Hostname {hostname} resolved to: {','.join(ips)}")
        ret = ips
    except Exception as e:
        display.v(f"Error resolving {hostname}: {e}")
        if not nameserver:
            ret = resolve_ip(hostname, '8.8.8.8')
    return ret

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
        auth = HTTPBasicAuth(username, password)
        ret = []
        for term in terms:
            display.v("url_to_backend lookup term: %s" % term)
            if isinstance(term, str):
                ns_proxies = {}
                if term.lower().startswith('https://'):
                    protocol = 'SSL'
                elif term.lower().startswith('http://'):
                    protocol = 'HTTP'
                else:
                    raise AnsibleError(f"URL should start with 'http://' or 'https://'")
                hostname = term.replace('https://','').replace('http://','').split("/")[0]
                ip_addresses = resolve_ip(hostname)
                for ip_address in ip_addresses:
                    lb_vservers = api_call(adm_hostname + adm_lbvservers_endpoint + '?filter=vsvr_ip_address:' + ip_address + ',vsvr_type:' + protocol, auth).get('ns_lbvserver', [])
                    cs_vservers = api_call(adm_hostname + adm_csvservers_endpoint + '?filter=vsvr_ip_address:' + ip_address + ',vsvr_type:' + protocol, auth).get('ns_csvserver', [])
                    if not cs_vservers and not lb_vservers:
                        display.vv(f"No lb or cs vservers found on ADM")
                    for lb_vserver in lb_vservers:
                        if lb_vserver['hostname'] in ns_proxies:
                            ns_proxy = ns_proxies[lb_vserver['hostname']]
                            ns_proxy['lb_vservers'].append(lb_vserver['name'])
                        else:
                            ns_proxy = {'lb_vservers': [lb_vserver['name']]}
                            ns_proxies[lb_vserver['hostname']] = ns_proxy
                    for cs_vserver in cs_vservers:
                        if cs_vserver['hostname'] in ns_proxies:
                            ns_proxy = ns_proxies[cs_vserver['hostname']]
                            ns_proxy['cs_vservers'].append(cs_vserver['name'])
                        else:
                            ns_proxy = {'cs_vservers': [cs_vserver['name']]}
                            ns_proxies[cs_vserver['hostname']] = ns_proxy
                ret.append(ns_proxies)
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
        return ret