# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: url_to_backend
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: 1.1.7
  short_description: This plugin resolves what backend server(s) are behind url
  description:
      - This lookup returns list of servers that are servicing specific url.
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.8).
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
    version: 1.1.8
---
- hosts: localhost
  connection: local
  gather_facts: true
  collections:
    - cencora.itoa
  vars:
    input_url: "https://cencora.com/"
    backend_servers: "{{ lookup('cencora.itoa.url_to_backend', input_url, username=username, password=password) }}"
  tasks:
    - debug:
        msg: "Backend servers for {{ input_url }} are {{ backend_servers }}"
"""

RETURN = r"""
returned_value:
  description: List of server dictionaries
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
      delay: 0
      delay1: 0
      nameserver: "0.0.0.0"
      dbsttl: 0
      orderstr: "Default"
      trofsdelay: "0
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
adc_csvserver_cspolicy_binding_endpoint = api_path + 'csvserver_cspolicy_binding'
adc_lbvserver_service_binding_endpoint = api_path + 'lbvserver_service_binding'
adc_lbvserver_servicegroup_binding_endpoint = api_path+ 'lbvserver_servicegroup_binding'
adc_cspolicy_endpoint = api_path + 'cspolicy'
adc_service_endpoint = api_path + 'service'
adc_servicegroup_servicegroupmember_binding_endpoint = api_path + 'servicegroup_servicegroupmember_binding'
adc_server_endpoint = api_path + 'server'

def resolve_ip(hostname):
    try:
        answer = resolver.query(hostname)
        ips = [ip.to_text() for ip in answer]
        return ips
    except Exception as e:
        display.v(f"Error resolving {hostname}: {e}")
        return []

def api_call(url, auth):
    display.vv(f"Feching info from {url}")
    response = requests.get(url, auth=auth, verify=False)
    display.vvv(f"Response status code {str(response.status_code)}")
    if response.status_code != 200:
        raise AnsibleError(f"http error : {response.status_code}: {response.text}")
    return response.json()

def convert_to_new_rule(rule):
    return rule.replace("req.http.url == '",'http.req.url.startswith("').replace("*'",'")')

def policy_match(url, rule):
    url = url.lower()
    rule = rule.lower()
    display.vvv(f"Url: {url}")
    display.vvv(f"Policy rule: {rule}")
    url_split = url.replace('https://','').replace('http://','').split("/")
    hostname = url_split[0]
    if len(url_split) > 1:
        path = '/' + '/'.join(url_split[1:])
    else:
        path = ''
    if '&&' in rule and '||' in rule: # compound expression e.g. http.req.hostname.eq("abcordersnd.amerisourcebergen.com") && (HTTP.REQ.URL.STARTSWITH("/bw") || HTTP.REQ.URL.STARTSWITH("/sap"))
        # split_and = rule.split('&&')
        display.vvv(f"Advanced compound expression found in rule: {rule}. This is not supproted")
        return False
    elif '&&' in rule:
        rules = rule.split('&&')
        results = []
        for nested_rule in rules:
            results.append(policy_match(url, nested_rule))
        return all(results)
    elif '||' in rule:
        rules = rule.split('||')
        results = []
        for nested_rule in rules:
            results.append(policy_match(url, nested_rule))
        return any(results) 
    else:
        if 'req.http' in rule: # old format
            rule = convert_to_new_rule(rule)
        rule = rule.strip().strip('(').strip(')').strip('"').replace("'",'')
        if not (rule.startswith('http.req.url.') or rule.startswith('http.req.hostname.')):
            display.vvv(f"Rule not supported: {rule}.")

        rule = rule.replace('.set_text_mode(ignorecase)','').replace('http.req.','')
        split_rule = rule.split('("')
        if not len(split_rule) == 2:
            display.vvv(f"Rule did not split well: {split_rule}.")
            return False
        first_part_split = split_rule[0].split('.')
        if not len(first_part_split) == 2:
            display.vvv(f"Rule did not split well: {split_rule}.")
            return False
        element = first_part_split[0]
        test = first_part_split[1]
        eval_var = split_rule[1]
        if element == 'hostname':
            if test == 'eq':
                return hostname == eval_var
            elif test == 'ne':
                return hostname != eval_var
            elif test == 'contains':
                return eval_var in hostname
            else:
                display.vvv(f"Test not supported: {test}.")
                return False
        else:
            if test == 'startswith':
                return path.startswith(eval_var)
            elif test == 'contains':
                return eval_var in path
            else:
                display.vvv(f"Test not supported: {test}.")
                return False

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        adm_hostname = 'https://' + self.get_option('adm_hostname')
        username = self.get_option('username')
        password = self.get_option('password')
        auth = HTTPBasicAuth(username, password)
        ret = []
        for term in terms:
            display.v("url_to_backend lookup term: %s" % term)
            if isinstance(term, str):
                target_servers = []
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
                    targetlbvservers = []
                    if not cs_vservers and not lb_vservers:
                        display.vv(f"No lb or cs vservers found on ADM")
                    for lb_vserver in lb_vservers:
                        targetlbvservers.append({'ns_ip_address': lb_vserver['ns_ip_address'], 'name': lb_vserver['name']})
                    for cs_vserver in cs_vservers:
                        ns_ip_address = cs_vserver['ns_ip_address']
                        cs_vserver_name = cs_vserver['name']
                        targetlbvserver = cs_vserver['targetlbvserver']
                        csvserver_policies = api_call('https://' + ns_ip_address + adc_csvserver_cspolicy_binding_endpoint + '/' + cs_vserver_name, auth).get('csvserver_cspolicy_binding', [])
                        sorted_policies = sorted(csvserver_policies, key=lambda x: int(x['priority']))
                        for policy in sorted_policies:
                            policy_rule = policy.get('rule', '')
                            if not policy_rule:
                                display.vvv(f"Policy rule not found for {policy['policyname']} doing extra API call")
                                cspolicy = api_call('https://' + ns_ip_address + adc_cspolicy_endpoint + '/' + policy['policyname'], auth).get('cspolicy', [])
                                if cspolicy:
                                    policy_rule = cspolicy[0].get('rule', '')
                            display.vvv(f"Evaluating policy: {policy['policyname']}")
                            if policy_match(term, policy_rule):
                                targetlbvserver = policy['targetlbvserver']
                                display.vv(f"Found matching policy. Target loadbalancer {policy['targetlbvserver']}")
                                break
                        targetlbvservers.append({'ns_ip_address': ns_ip_address, 'name': targetlbvserver})
                    for targetlbvserver in targetlbvservers:
                        if not targetlbvserver['name']:
                            continue
                        service_bindings = api_call('https://' + targetlbvserver['ns_ip_address'] + adc_lbvserver_service_binding_endpoint + '/'  + targetlbvserver['name'], auth).get('lbvserver_service_binding', [])
                        for service_binding in service_bindings:
                            services = api_call('https://' + targetlbvserver['ns_ip_address'] + adc_service_endpoint + '/'  + service_binding['servicename'], auth).get('service', [])
                            for service in services:
                                servers = api_call('https://' + targetlbvserver['ns_ip_address'] + adc_server_endpoint + '/'  + service['servername'], auth).get('server', [])
                                for server in servers:
                                    target_servers.append(server)
                        servicegroup_bindings = api_call('https://' + targetlbvserver['ns_ip_address'] + adc_lbvserver_servicegroup_binding_endpoint + '/'  + targetlbvserver['name'], auth).get('lbvserver_servicegroup_binding', [])
                        for servicegroup_binding in servicegroup_bindings:
                            servicegroup_members = api_call('https://' + targetlbvserver['ns_ip_address'] + adc_servicegroup_servicegroupmember_binding_endpoint + '/'  + servicegroup_binding['servicename'], auth).get('servicegroup_servicegroupmember_binding', [])
                            for servicegroup_member in servicegroup_members:
                                servers = api_call('https://' + targetlbvserver['ns_ip_address'] + adc_server_endpoint + '/'  + servicegroup_member['servername'], auth).get('server', [])
                                for server in servers:
                                    target_servers.append(server)
                ret.append(target_servers)
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
        return ret