from __future__ import (absolute_import, division, print_function)
from ansible.utils.display import Display
from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
import requests
import json
import base64
__metaclass__ = type

DOCUMENTATION = r"""
name: secrets_safe
author:
  - Eduardas Sizovas eduardas.sizovas@amerisourcebergen.com
  - Matt Cengic matt.cengic@amerisourcebergen.com
  - Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com
short_description: This collection creates a lookup plugin for BeyondTrust teams passwords, texts, and files
description:
  - This lookup plugin can be used to fetch credentials, text strings and files from BeyondTrust.
notes:
  - This module is part of the cencora.itoa collection (version 1.1.5).
  - To set up with AWX execution.
  - Order Teams password safe and make sure access is provisioned for service account.
    You'll need an Active Directory service account. Once you have that, send an email
    (template to be determined) to PrivilegedAccessManagement@amerisourcebergen.com so
    they can provision access to your BT safe. Be sure to note your service account
    should not have multifactor authentication enabled for this.
  - In AWX, create custom credential of type BeyondTrust and provide username, password
    and api key. Note the name of the BeyondTrust folder your credentials are stored in.
  - Add the custom credential from step 2 to playbook execution template.
  - Add playbook that uses collection lookup vars according to your needs, see below.
  - To install it, use C(ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-beyond_trust).
  - You'll also want to create C(collections/requirements.yml) in your AWX playbook that 
    contains this content
version_added: 1.1.0
options:
  _terms:
      description:
        - credential titles to fetch
        - can be specified with folder name e.g. folder/my_creds
      required: True
  bt_uri:
    description: 
      - Base uri. If not set C(BT_URI) environment variable will be used.
    required: True
    type: str
    vars: 
      - name: bt_uri
    env: 
      - name: BT_URI
  bt_folder:
    description: 
      - folder location in BeyondTrust. If not set C(BT_FOLDER) environment variable will be used.
      - if folder is specified in term this is optional
    type: str
    default: ''
    vars: 
      - name: bt_folder
    env: 
      - name: BT_FOLDER
  bt_username:
    description: 
      - Username. If not set C(BT_USERNAME) environment variable will be used.
    required: True
    type: str
    vars: 
      - name: bt_username
    env: 
      - name: BT_USERNAME
  bt_password:
    description: 
      - Password. If not set C(BT_PASSWORD) environment variable will be used.
    required: True
    type: str
    vars: 
      - name: bt_password
    env: 
      - name: BT_PASSWORD
  bt_apikey:
    description: 
      - API key. If not set C(BT_APIKEY) environment variable will be used.
    required: True
    type: str
    vars: 
      - name: bt_apikey
    env: 
      - name: BT_APIKEY
  bt_cert_verify:
    description:
      - Path to cert file, otherwise set to False to disable certificate checking. If not set C(BT_CERT_VERIFY) environment variable will be used.
    type: str
    default: False
    vars: 
      - name: bt_cert_verify
    env: 
      - name: BT_CERT_VERIFY
"""

EXAMPLES = r"""
---
collections:
  - name: cencora.itoa
    type: git
    source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
    version: 1.1.5
---
- name: Retrieve credentials from bt prod instance
  hosts: 127.0.0.1
  gather_facts: false
  become: false
  collections:
    - cencora.itoa
  vars:
    credentials: "{{ lookup('cencora.itoa.secrets_safe', 'credential by title', 'optionally specify additional credential by title here', bt_folder='AWX Vault') }}"
    bt_uri: https://iambyti1p002.abc.amerisourcebergen.com/ 
  tasks:
    - debug:
        msg:
          - "Username {{ credentials['credential by title']['username'] }}"
          - "Password {{ credentials['credential by title']['password'] }}"
"""

RETURN = r"""
cred_title:
  description: Credential title as specified in the request e.g. 'folder/my_creds'
  returned: always
  type: dict
  contains:
    username:
      description: Username
      returned: when supported
      type: string
      sample: "svc_ansible"
    password:
      description: Password
      returned: when supported
      type: string
      sample: "another_random_password"
    text:
      description: Contents of text secret.
      returned: when supported
      type: string
      sample: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    file:
      description: File data encoded in base64.
      returned: when supported
      type: string
      sample: 'TWFueSBoYW5kcyBtYWtlIGxpZ2h0IHdvcmsu'
"""

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        requests.packages.urllib3.disable_warnings()
        self.set_options(var_options=variables, direct=kwargs)
        bt_folder = self.get_option('bt_folder')
        bt_uri = self.get_option('bt_uri')
        bt_apikey = self.get_option('bt_apikey')
        bt_username = self.get_option('bt_username')
        bt_password = self.get_option('bt_password')
        bt_cert_verify = self.get_option('bt_cert_verify')
        if bt_cert_verify is None or bt_cert_verify.lower()=="false":
          bt_cert_verify=False
        bt = BtApi(
            bt_uri,
            bt_apikey,
            bt_username,
            bt_password,
            bt_cert_verify
        )
        display.debug(f"Doing bt authenticate...")
        bt.authenticate()
        display.debug(f"Get folders")
        bt.get_folders()
        ret = []
        creds_dict = dict()
        for term in terms:
            display.debug(f"Searching for {term}")
            term_split = term.split('/')
            if len(term_split) > 1:
                title = term_split[-1]
                folder = term_split[-2]
            else:
                title = term
                if not bt_folder:
                    raise AnsibleError(f"bt_folder should be set if it is not specified in credential name")
                folder = bt_folder
            try:
              folder_id = next(f['Id'] for f in bt.folders if f['Name'] == folder)
            except:
              raise AnsibleError(f"bt_folder={folder} not found in BeyondTrust")
            bt.get_credentials(folder_id)
            if len(bt.credentials)==0:
                raise AnsibleError(f"Unable to find any credentials with parameters supplied.")
            for credential in bt.credentials:
                if credential['Title'] !=  title:
                    continue
                creds_dict[term] = dict()
                if credential['SecretType']=="Credential":
                    res = bt.get_credential(credential['Id'])
                    creds_dict[term]['username'] = res['Username']
                    creds_dict[term]['password'] = res['Password']
                    
                elif credential['SecretType']=="Text":
                    res = bt.get_credential(credential['Id'])
                    creds_dict[term]['text'] = res['Password']
                elif credential['SecretType']=="File":
                    res = bt.get_file(credential['Id'])
                    creds_dict[term]['file'] = res['filecontent']
                else:
                    raise AnsibleError(f"Found a matching secret, but this is plugin is unable to handle its SecretType. The SecretType found was {credential['SecretType']}.")
        ret.append(creds_dict)
        bt.signout()
        if len(ret)==0:
          raise AnsibleError(f"Unable to find a secret matching the title supplied")
        return ret

class BtApi:
    def __init__(
            self,
            base_uri,
            api_key,
            username,
            password,
            bt_cert_verify
            ):
        self.base_uri = f"{base_uri}BeyondTrust/api/public/v3"
        self.bt_cert_verify=bt_cert_verify
        display.debug(f"Base uri is: {self.base_uri}")
        self.auth_header = {
            "Authorization":
            f"PS-Auth key={api_key}; runas={username}; pwd=[{password}];"
        }
        
        self.session = requests.Session()

    def get_folders(self):
        display.debug("Getting folder list for Team Passwords")
        try:
            response = self.session.get(
                f"{self.base_uri}/Secrets-Safe/Folders")
        except Exception as e:
            raise AnsibleError(f"Unable to get Secrets-Safe folders. Error was {e}")
        self.folders = self.__handle_reponse(response)

    def get_credentials(self, folder_id):
        display.debug(f"Getting credential list for folder {folder_id}")
        try:
            response = self.session.get(
                f"{self.base_uri}/Secrets-Safe/Folders/{folder_id}/secrets")
        except Exception as e:
            raise AnsibleError(f"Unable to get credential list. Error was {e}")
        self.credentials = self.__handle_reponse(response)

    def get_credential(self, credential_id):
        display.debug(f"Getting credential information for credential ID {credential_id}")
        try:
            response = self.session.get(
                f"{self.base_uri}/Secrets-Safe/Secrets/{credential_id}")
        except Exception as e:
            raise AnsibleError(f"Unable to get credential list. Error was {e}")
        return self.__handle_reponse(response)

    def get_file(self, file_id):
        display.debug(f"Getting file for {file_id}")
        try:
            response = self.session.get(
                f"{self.base_uri}/Secrets-Safe/Secrets/{file_id}/file/download")
        except Exception as e:
            raise AnsibleError(f"Unable to get credential list. Error was {e}")
        return self.__handle_reponse_filecontents(response)

    def authenticate(self):
        display.debug("Authenticating to BeyondTrust API")
        url = f"{self.base_uri}/Auth/SignAppin"
        try:
            response = self.session.post(
                url, headers=self.auth_header, verify=self.bt_cert_verify)
        except Exception as e:
            raise AnsibleError(f"Could not connect to {url} Error was: {e}")
        self.__handle_reponse(response)
        display.debug("Succesfully authenticated to BeyondTrust API")

    def signout(self):
        display.debug("Signing out from BeyondTrust API")
        try:
            self.session.post(
                f"{self.base_uri}/Auth/SignOut", verify=self.bt_cert_verify)
        except Exception as e:
            raise AnsibleError(f"Could not connect to {self.base_uri}")
        display.debug("Succesfully signed out from BeyondTrust API")

    def __handle_reponse(self, response):
        if not response.status_code == 200:
            raise AnsibleError(
                f"Reponse {response.status_code} received from {response.request.url}")
        try:
            results = json.loads(response.text)
        except Exception as e:
            raise AnsibleError(f"Could not parse BeyondTrust response: {e}")
        return results

    def __handle_reponse_filecontents(self, response):
        if not response.status_code == 200:
            raise AnsibleError(
                f"Reponse {response.status_code} received from {self.base_uri}")
        try:
            results = {"filecontent":base64.b64encode(response.content).decode('utf-8')}
        except Exception as e:
            raise AnsibleError(f"Could not parse BeyondTrust response: {e}")
        return results

