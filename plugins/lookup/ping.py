# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: ping
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: 1.1.8
  short_description: This plugin is used to ping host using ICMP
  description:
      - This lookup returns result of ping.
      - It utilizes ping3 module of python3.
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.8).
      - To install it, use C(ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git).
      - You'll also want to create C(collections/requirements.yml) in your AWX playbook that 
        contains this content
  options:
    _terms:
      description: IP address or hostname to ping
      required: True
    timeout:
      description:
        - Timeout value of ping packet
      default: 4
      type: int
      ini:
        - section: ping
          key: timeout
    unit:
      description:
        - Unit of returned value
        - Can be ms for milliseconds or s for seconds
      type: string
      default: 's'
      ini:
        - section: ping
          key: unit
    ttl:
      description:
        - Time-To-Live value of ICMP packet
        - The packet is discarded if it does not reach the target host after jumps in under TTL value
        - TTL value range is 1-255
        - If value is out of range default will be used
      default: 64
      type: int
      ini:
        - section: ping
          key: ttl
    size:
      description:
        - Size of ICMP packet payload in bytes
        - Size value range is 1-65500
        - The total ICMP packet size is 8 bytes larger.
        - E.g. 8 (header) + 56 (payload) = 64 bytes
      default: 56
      type: int
      ini:
        - section: ping
          key: size
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
    hostname: "example.com"
    ping_result: "{{ lookup('cencora.itoa.ping', hostname) }}"
  tasks:
    - debug:
        msg: "Ping of {{ hostname }} is {{ ping_result }}"
"""

RETURN = r"""
ping_time:
  description: Ping result
  returned: always
  type: float
  sample: 0.215697261510079666
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import subprocess

display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        timeout = self.get_option('timeout')
        unit = self.get_option('unit').lower()
        ttl = self.get_option('ttl')
        size = self.get_option('size')
        ret = []
        for term in terms:
            display.vvv("Pinging: %s" % term)
            if isinstance(term, str):
                if ttl < 1 and ttl > 256:
                    display.vvv("TTL is outside allowed range default value of 64 will be used")
                    ttl = 64
                if size < 1 and size > 65500: # max size is 65507 which is 65535 (max ip length) - 20 (ip hdr) - 8 (icmp/ping hdr) = 65507
                    # Windows OS blocks max size at 65500 but in Linux you can ping up to the real limit
                    display.vvv("Size is outside allowed range default value of 56 will be used")
                    size = 56
                if not (unit == 's' or unit == 'ms'):
                    display.vvv("Unit can only be 's' or 'ms'. Default value of 's' will be used")
                    unit = 's'
                try:
                    output = subprocess.check_output(["ping", "-c", "4", "-W", str(timeout), "-t", str(ttl), "-s", str(size), term], stderr=subprocess.STDOUT)
                    try:
                        ping_result = float(output.split(b'\n')[-2].split()[-2].split(b'/')[1])
                        if unit == 's':
                            ping_result = ping_result/1000
                    except:
                        display.vvv(f"Cannot parse output: {output}")
                        ping_result = False
                except subprocess.CalledProcessError as e:
                    if e.returncode == 1:
                        display.vvv(f"{term} unreachable")
                        ping_result = None
                    elif b'Name or service not known' in e.output:
                        display.vvv(f"{term} - Name or service not known")
                        ping_result = False
                    else:
                        display.vvv(f"Other error: {e.output}")
                        ping_result = False
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
            ret.append(ping_result)
        return ret