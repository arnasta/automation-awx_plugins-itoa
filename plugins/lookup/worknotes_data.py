# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: worknotes_data
  author: Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
  version_added: "0.1"
  short_description: extracts data from SeriveNow notes
  description:
      - This lookup returns a data object or list of data objects from ServiceNow ticket work notes
  notes:
      - This module is part of the cencora.itoa collection (version 1.0.0).
      - To install it, use C(ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git).
  options:
    _terms:
      description: work_notes string
      required: True
    latest:
      description:
        - it is a flag to return only latest data or all data
      default: true
      type: bool
      ini:
        - section: worknotes_data
          key: latest
"""

EXAMPLES = r"""
---
collections:
  - name: cencora.itoa
    type: git
    source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
    version: 1.0.0
---
- hosts: localhost
  connection: local
  gather_facts: true
  collections:
    - cencora.itoa
  vars:
    work_notes: "08-25-2023 05:57:37 - ITOA Automation (Work notes)\n---
        # yaml start\\n-  
        data:\n        ip:\n        - 10.123.45.67\n       
        - 10.234.56.78\n        palo:\n            fw:\n           
        - fadc-eif01.myabcit.net\n            object:\n           
        - etsse1i1s001\n            zone:\\n           
        - PROD_SHARED_SERVICES\n    name: Data\n...\n\n"
    data: "{{ lookup('cencora.itoa.worknotes_data', work_notes, latest=false) }}"
  tasks:
    - debug:
        msg: "{{ data }}"
"""

RETURN = r"""
worknote_date:
  description: Date of work note
  returned: always
  type: string
  sample: "08-25-2023 05:57:37"
worknote_user:
  description: User who posted the work note
  returned: always
  type: string
  sample: "ITOA Automation"
data:
  description: yaml data in the work note
  returned: always
  type: list
  sample: [
      {
        "data": {
          "ip": [
            "10.123.45.67",
            "10.234.56.78"
          ],
          "palo": {
            "fw": [
              "fadc-eif01.myabcit.net"
            ],
            "object": [
              "etsse1i1s001"
            ],
            "zone": [
              "PROD_SHARED_SERVICES"
            ]
          }
        },
        "name": "Data"
      }
    ]
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import yaml

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        self.set_options(var_options=variables, direct=kwargs)
        latest = self.get_option('latest')
        ret = []
        for term in terms:
            display.debug("worknotes_data lookup term: %s" % term)
            if isinstance(term, str):
                if '--- # yaml start' in term:
                    blocks = term.split('--- # yaml start')
                    data = list()
                    for index, block in enumerate(blocks):
                        if index == 0:
                            continue
                        # Check if timestamp and username is present
                        if not ' (Work notes)' in blocks[index-1]:
                            continue
                        try:
                            block_info = blocks[index-1].split('\n')[-2]
                            worknote_date = block_info.split(' - ')[0]
                            worknote_user = block_info.split(' - ')[1].split(' (Work notes)')[0]
                        except:
                            display.debug(f"Cannot extract date from {block_info}")
                            continue
                        try:
                            worknote_data = yaml.safe_load(block.split('...')[0])
                        except:
                            display.debug(f"Cannot load yaml from {block.split('...')[0]}")
                            continue
                        yaml_dict = dict()
                        yaml_dict['worknote_date'] = worknote_date
                        yaml_dict['worknote_user'] = worknote_user
                        yaml_dict['data'] = worknote_data
                        if latest:
                            data = yaml_dict.copy()
                            break
                        data.append(yaml_dict.copy())
                    ret.append(data)
                else:
                    display.debug("Data not found")
            else:
                raise AnsibleError(f"Input should be a string not '{type(term)}'")
        return ret