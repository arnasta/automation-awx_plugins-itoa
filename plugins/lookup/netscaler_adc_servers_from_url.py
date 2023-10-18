# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: netscaler_adc_servers_from_url
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: 1.1.9
  short_description: This plugin resolves what backend server(s) are behind url
  description:
      - This lookup returns list of servers that are servicing specific url.
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.9).
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
        - section: netscaler_adc_servers_from_url
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
    external_dns:
      description:
        - External DNS servers used to resolve hostname
        - If the value is not specified, default value of 8.8.8.8 will be used
      default: '8.8.8.8'
      type: str
      ini:
        - section: netscaler_adc_servers_from_url
          key: external_dns
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
    backend_servers: "{{ lookup('cencora.itoa.netscaler_adc_servers_from_url', input_url, username=username, password=password) }}"
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
adc_lbvserver_endpoint = api_path+ 'lbvserver'
adc_csvserver_endpoint = api_path + 'csvserver'
adc_csvserver_cspolicy_binding_endpoint = api_path + 'csvserver_cspolicy_binding'
adc_lbvserver_service_binding_endpoint = api_path + 'lbvserver_service_binding'
adc_lbvserver_servicegroup_binding_endpoint = api_path+ 'lbvserver_servicegroup_binding'
adc_cspolicy_endpoint = api_path + 'cspolicy'
adc_service_endpoint = api_path + 'service'
adc_servicegroup_servicegroupmember_binding_endpoint = api_path + 'servicegroup_servicegroupmember_binding'
adc_server_endpoint = api_path + 'server'

def resolve_ip(hostname, nameserver=''):
    ret = []
    owner = ''
    res = resolver.Resolver()
    if nameserver:
        display.v(f"Trying to resolve {hostname} using: {nameserver} dns server")
        res.nameservers = [nameserver]
    else:
        display.v(f"Trying to resolve {hostname} using: default dns server")
    try:
        answer = res.query(hostname)
        owner = answer.canonical_name.to_text()
        ips = [ip.to_text() for ip in answer]
        display.v(f"Hostname {hostname} resolved to: {','.join(ips)}")
        ret = ips
    except Exception as e:
        display.v(f"Error resolving {hostname}: {e}")
        if nameserver:
            ret, owner = resolve_ip(hostname)
    return ret, owner

def api_call(url, auth):
    display.vv(f"Fetching info from {url}")
    response = requests.get(url, auth=auth, verify=False)
    display.vvv(f"Response status code {str(response.status_code)}")
    if response.status_code != 200:
        raise AnsibleError(f"http error : {response.status_code}: {response.text}")
    return response.json()

open_list = ['(']
close_list = [')']
operator_list = ['|','&']

def convert_to_advanced_expression(rule):
    return rule.replace("req.http.url == '",'http.req.url.startswith("').replace("*'",'")')

def eval_advanced_expression(rule, hostname, path):
    rule = rule.replace(']','')
    rule_split = rule.split('[')
    first_part_split = rule_split[0].split('.')[2:]
    eval_var = rule_split[1]
    element = first_part_split[0]
    test = first_part_split[1]
    ret = False
    display.vvv(f'Test: {element} {test} {eval_var}')
    if element == 'hostname':
        if test == 'eq':
            ret = bool(hostname == eval_var)
        elif test == 'ne':
            ret = bool(hostname != eval_var)
        elif test == 'contains':
            ret = bool(eval_var in hostname)
        else:
            display.v(f"Test not supported: {test}.")
    else:
        if test == 'startswith':
            ret = bool(path.startswith(eval_var))
        elif test == 'contains':
            ret = bool(eval_var in path)
        else:
            display.v(f"Test not supported: {test}.")
    return ret

def eval_compound_advanced_expression(rule, hostname, path):
    display.vvv(f'Expression: "{rule}"')
    expression =  ''
    previous_char = ''
    previous_test = False
    operator = 'or'
    open_count = 0
    result = False
    for i in rule:
        if i in open_list:
            display.vvvv(f'Opening parenthesis found.')
            open_count+=1
            if expression:
                expression += i
        elif i in close_list:
            display.vvvv(f'Closing parenthesis found.')
            open_count-=1
            if open_count == 0:
                display.vvvv(f'Top most closing parenthesis found. Expression: "{expression}"')
                if operator == 'or':
                    recursive_result = eval_compound_advanced_expression(expression, hostname, path)
                    result = bool(previous_test or recursive_result)
                else:
                    recursive_result = eval_compound_advanced_expression(expression, hostname, path)
                    result = bool(previous_test and recursive_result)
                previous_test = result
                expression =  ''
            else:
                expression += i
        elif i in operator_list and previous_char == i and open_count == 0:
            display.vvvv(f'Full operator found "{i}{i}"')
            if i == '|':
                operator = 'or'
            else:
                operator = 'and'
        elif i in operator_list and open_count == 0:
            display.vvvv(f'Operator found "{i}"')
            if expression:
                display.vvvv(f'Completing expression: "{expression}"')
                if operator == 'or':
                    recursive_result = eval_compound_advanced_expression(expression, hostname, path)
                    display.vvvv(f'Recursive result: {recursive_result}')
                    result = bool(previous_test or recursive_result)
                else:
                    recursive_result = eval_compound_advanced_expression(expression, hostname, path)
                    display.vvvv(f'Recursive result: {recursive_result}')
                    result = bool(previous_test and recursive_result)
                previous_test = result
                expression =  ''
        else:
            expression += i
        previous_char = i
    if expression:
        display.vvvv(f'Completing expression: "{expression}". Operator: "{operator}"')
        if operator == 'or':
            result = bool(previous_test or eval_advanced_expression(expression, hostname, path))
        else:
            result = bool(previous_test and eval_advanced_expression(expression, hostname, path))
        previous_test = result
        expression =  ''
    display.vvvv(f'Returning result: {result}')
    return result

def policy_match(url, rule):
    url = url.lower()
    rule = rule.lower()
    url_split = url.replace('https://','').replace('http://','').split("/")
    hostname = url_split[0]
    if len(url_split) > 1 and url_split[-1]:
        path = '/' + '/'.join(url_split[1:])
    else:
        path = ''
    display.vvv(f"Url: '{url}'")
    display.vvv(f"Hostname: '{hostname}'")
    display.vvv(f"Path: '{path}'")
    display.vvv(f"Policy rule: '{rule}'")
    if 'req.http' in rule: # classic policy expression
        display.vvv(f"Classic policy expression: {rule} detected. Converting to advanced.")
        rule = convert_to_advanced_expression(rule)
    rule = rule.replace('("','[') # replacing parenthesis with brackets for better code control
    rule = rule.replace('")',']') # replacing parenthesis with brackets for better code control
    rule = rule.replace(' ','') # removing spaces
    rule = rule.replace('url.path','url') # there are url.path and url clauses so replacing url.path with url
    rule = rule.replace('get(1).','') # there are some rules that have fuction get(1) this is removed
    rule = rule.replace('set_text_mode(ignorecase).','') # remove set_text_mode(ignorecase) since lower is used
    display.vvv(f"Final optimized rule: '{rule}'")
    try:
        result = eval_compound_advanced_expression(rule, hostname, path)
        display.vvv(f"Expression evaluated to {result}")
    except Exception as e:
         display.vvv(f"Error evaluating policy expression {rule}. Error: {e}. Setting result to false.")
         result = False
    return result

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        adm_hostname = 'https://' + self.get_option('adm_hostname')
        adc_domain = '.'.join(self.get_option('adm_hostname').split('.')[-2:])
        username = self.get_option('username')
        password = self.get_option('password')
        external_dns = self.get_option('external_dns')
        auth = HTTPBasicAuth(username, password)
        ret = []
        for term in terms:
            display.v("netscaler_adc_servers_from_url lookup term: %s" % term)
            if isinstance(term, str):
                url = term.lower()
                vserver_list = []
                server_list = []
                ip_address_list = []
                if url.startswith('https://'):
                    protocol = 'SSL'
                elif url.startswith('http://'):
                    protocol = 'HTTP'
                else:
                    raise AnsibleError(f"URL should start with 'http://' or 'https://'")
                hostname = url.replace('https://','').replace('http://','').split("/")[0]
                ip_addresses, owner = resolve_ip(hostname, external_dns)
                for ip_address in ip_addresses:
                    ip_address_list.append({'ip_address': ip_address, 'owner': owner})
                    cs_vservers = api_call(adm_hostname + adm_csvservers_endpoint + '?filter=vsvr_ip_address:' + ip_address + ',vsvr_type:' + protocol, auth).get('ns_csvserver', [])
                    vserver_type = 'cs'
                    vserver = next(iter(cs_vservers), '')
                    if not vserver:
                        lb_vservers = api_call(adm_hostname + adm_lbvservers_endpoint + '?filter=vsvr_ip_address:' + ip_address + ',vsvr_type:' + protocol, auth).get('ns_lbvserver', [])
                        vserver = next(iter(lb_vservers), '')
                        vserver_type = 'lb'
                    if vserver:
                        vserver_list.append({'name': vserver['name'], 'type': vserver_type, 'load_balancer': vserver['hostname'] + '.' + adc_domain, 'ip_address': ip_address})
                    else:
                        display.vv(f"No lb or cs vservers found on ADM")
                for vserver in  vserver_list:
                    if vserver['type'] == 'lb':
                        lb_vserver = api_call('https://' + vserver['load_balancer'] + adc_lbvserver_endpoint + '/' + vserver['name'], auth)['lbvserver'][0]
                        target_lbvserver = lb_vserver['name']
                    else:
                        cs_vserver = api_call('https://' + vserver['load_balancer'] + adc_csvserver_endpoint + '/' + vserver['name'], auth)['csvserver'][0]
                        target_lbvserver = cs_vserver['lbvserver']
                        csvserver_policies = api_call('https://' + vserver['load_balancer'] + adc_csvserver_cspolicy_binding_endpoint + '/' + vserver['name'], auth).get('csvserver_cspolicy_binding', [])
                        sorted_policies = sorted(csvserver_policies, key=lambda x: int(x['priority']))
                        for policy in sorted_policies:
                            policy_rule = policy.get('rule', '')
                            if not policy_rule:
                                display.vvv(f"Policy rule not found for {policy['policyname']} doing extra API call")
                                cspolicy = api_call('https://' + vserver['load_balancer'] + adc_cspolicy_endpoint + '/' + policy['policyname'], auth).get('cspolicy', [])
                                if cspolicy:
                                    policy_rule = cspolicy[0].get('rule', '')
                            display.vvv(f"Evaluating policy: {policy['policyname']}")
                            if policy_match(url, policy_rule):
                                target_lbvserver = policy['targetlbvserver']
                                display.vv(f"Found matching policy. Target loadbalancer {target_lbvserver}")
                                break
                    service_bindings = api_call('https://' + vserver['load_balancer'] + adc_lbvserver_service_binding_endpoint + '/'  + target_lbvserver, auth).get('lbvserver_service_binding', [])
                    for service_binding in service_bindings:
                        services = api_call('https://' + vserver['load_balancer'] + adc_service_endpoint + '/'  + service_binding['servicename'], auth).get('service', [])
                        for service in services:
                            servers = api_call('https://' + vserver['load_balancer'] + adc_server_endpoint + '/'  + service['servername'], auth).get('server', [])
                            for server in servers:
                                server_list.append(server)
                    servicegroup_bindings = api_call('https://' + vserver['load_balancer'] + adc_lbvserver_servicegroup_binding_endpoint + '/'  + target_lbvserver, auth).get('lbvserver_servicegroup_binding', [])
                    for servicegroup_binding in servicegroup_bindings:
                        servicegroup_members = api_call('https://' + vserver['load_balancer'] + adc_servicegroup_servicegroupmember_binding_endpoint + '/'  + servicegroup_binding['servicename'], auth).get('servicegroup_servicegroupmember_binding', [])
                        for servicegroup_member in servicegroup_members:
                            servers = api_call('https://' + vserver['load_balancer'] + adc_server_endpoint + '/'  + servicegroup_member['servername'], auth).get('server', [])
                            for server in servers:
                                server_list.append(server)
                ret.append({'ip_address_list': ip_address_list, 'vserver_list': vserver_list, 'server_list': server_list})
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
        return ret