# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: date_tz
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: 1.1.7
  short_description: This plugin converts date string from one timezone to another
  description:
      - This lookup returns a datetime string after converting it to another timezone.
  notes:
      - This module is part of the cencora.itoa collection (version 1.1.9).
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
        - Default data format is '%m-%d-%Y %H:%M:%S'
      default: '%m-%d-%Y %H:%M:%S'
      type: string
      ini:
        - section: date_tz
          key: format
    out_format:
      description:
        - Date format e.g. '%m-%d-%Y %H:%M:%S'
        - format is used for output format if this is not defined
      type: string
      default: ''
      ini:
        - section: date_tz
          key: out_format
    in_tz:
      description:
        - timezone of date string
        - timezone name as specified in pytz library
      required: True
      type: string
      ini:
        - section: date_tz
          key: in_tz
    out_tz:
      description:
        - timezone of date string
        - timezone name as specified in pytz library
      required: True
      type: string
      ini:
        - section: date_tz
          key: out_tz
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
    input_date: "08-25-2023 05:57:37"
    utc_date: "{{ lookup('cencora.itoa.date_tz', input_date, in_tz='EST', out_tz='UTC') }}"
  tasks:
    - debug:
        msg: "EST {{ input_date }} will be {{ utc_date }} in UTC"
"""

RETURN = r"""
date_string:
  description: Datetime in another timezone
  returned: always
  type: string
  sample: "08-25-2023 05:57:37"
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import datetime
import pytz


display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        self.set_options(var_options=variables, direct=kwargs)
        format = self.get_option('format')
        out_format = self.get_option('out_format')
        in_tz = self.get_option('in_tz')
        out_tz = self.get_option('out_tz')
        ret = []
        for term in terms:
            display.vvv("date_tz lookup term: %s" % term)
            if isinstance(term, str):
                try:
                    input_date = datetime.datetime.strptime(term, format)
                except:
                    raise AnsibleError(f"Input data string: '{term}' does not match date format: '{format}'")
                if in_tz == out_tz:
                    output_date = input_date
                else:
                    if not (in_tz in pytz.all_timezones and out_tz in pytz.all_timezones):
                        raise AnsibleError(f"Timezone string should be one of '{pytz.all_timezones}'")
                    dt_with_tz = pytz.timezone(in_tz).localize(input_date)
                    output_date = dt_with_tz.astimezone(pytz.timezone(out_tz))
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
            if out_format:
                ret.append(output_date.strftime(out_format))
            else:
                ret.append(output_date.strftime(format))
        return ret