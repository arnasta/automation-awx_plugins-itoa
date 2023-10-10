# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: timedelta
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: 1.0.0
  short_description: This plugin calculates timedelta
  description:
      - This lookup returns a datetime string after adding or subtracting timedelta.
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.8).
      - To install it, use C(ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git).
      - You'll also want to create C(collections/requirements.yml) in your AWX playbook that 
        contains this content
  options:
    _terms:
      description: Input date string
      required: True
    format:
      description:
        - Date format e.g. '%m-%d-%Y %H:%M:%S'
        - Default data format is '%Y-%m-%dT%H:%M:%S.%f%z'
      default: '%Y-%m-%dT%H:%M:%S.%f%z'
      type: string
      ini:
        - section: timedelta_lookup
          key: format
    out_format:
      description:
        - Date format e.g. '%m-%d-%Y %H:%M:%S'
        - format is used for output format if this is not defined
      type: string
      default: ''
      ini:
        - section: timedelta_lookup
          key: out_format
    delta:
      description:
        - Time delta string in form of '-1 day'
        - First character should be sign '+' or '-'
        - Amount should go after sign
        - Units should follow the amount separated by space
      required: True
      type: string
      ini:
        - section: timedelta_lookup
          key: delta
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
    input_date: "08-25-2023 05:57:37"
    future_date: "{{ lookup('cencora.itoa.timedelta', input_date, delta='+16 days', format='%m-%d-%Y %H:%M:%S') }}"
  tasks:
    - debug:
        msg: "16 days from {{ input }} will be {{ future_date }}"
"""

RETURN = r"""
date_string:
  description: Date with timedelta applied
  returned: always
  type: string
  sample: "08-25-2023 05:57:37"
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import datetime

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        self.set_options(var_options=variables, direct=kwargs)
        format = self.get_option('format')
        out_format = self.get_option('out_format')
        delta = self.get_option('delta')
        ret = []
        for term in terms:
            display.debug("timedelta lookup term: %s" % term)
            if isinstance(term, str):
                sign = delta[0]
                try:
                    amount = int(delta[1:].split(' ')[0])
                except:
                    raise AnsibleError(f"Amount should be integer. String '{delta[1:].split(' ')[0]}' cannot be converted to integer.")
                try:
                    unit = delta[1:].split(' ')[1]
                except:
                    raise AnsibleError(f"Unit not for in term '{term}'")
                try:
                    input_date = datetime.datetime.strptime(term, format)
                except:
                    raise AnsibleError(f"Input data string: '{term}' does not match date format: '{format}'")
                if sign == '+':
                    if unit == 'days':
                        output_date = input_date + datetime.timedelta(days=amount)
                    elif unit == 'seconds':
                        output_date = input_date + datetime.timedelta(seconds=amount)
                    elif unit == 'microseconds':
                        output_date = input_date + datetime.timedelta(microseconds=amount)
                    elif unit == 'milliseconds':
                        output_date = input_date + datetime.timedelta(milliseconds=amount)
                    elif unit == 'minutes':
                        output_date = input_date + datetime.timedelta(minutes=amount)
                    elif unit == 'hours':
                        output_date = input_date + datetime.timedelta(hours=amount)
                    elif unit == 'weeks':
                        output_date = input_date + datetime.timedelta(weeks=amount)
                    else:
                        raise AnsibleError(f"Units should be a string of 'days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours' or 'weeks' not '{unit}'")
                elif sign == '-':
                    if unit == 'days':
                        output_date = input_date - datetime.timedelta(days=amount)
                    elif unit == 'seconds':
                        output_date = input_date - datetime.timedelta(seconds=amount)
                    elif unit == 'microseconds':
                        output_date = input_date - datetime.timedelta(microseconds=amount)
                    elif unit == 'milliseconds':
                        output_date = input_date - datetime.timedelta(milliseconds=amount)
                    elif unit == 'minutes':
                        output_date = input_date - datetime.timedelta(minutes=amount)
                    elif unit == 'hours':
                        output_date = input_date - datetime.timedelta(hours=amount)
                    elif unit == 'weeks':
                        output_date = input_date - datetime.timedelta(weeks=amount)
                    else:
                        raise AnsibleError(f"Units should be a string of 'days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours' or 'weeks' not '{unit}'")
                else:
                    raise AnsibleError(f"Amount should be prepended with sign '+' or '-', not '{sign}'")
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
            if out_format:
                ret.append(output_date.strftime(out_format))
            else:
                ret.append(output_date.strftime(format))
        return ret