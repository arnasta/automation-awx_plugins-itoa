.. _cencora.itoa.secrets_safe_lookup:


*************************
cencora.itoa.secrets_safe
*************************

**This collection creates a lookup plugin for BeyondTrust teams passwords, texts, and files**


Version added: 1.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup plugin can be used to fetch credentials, text strings and files from BeyondTrust.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>_terms</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>credential titles to fetch</div>
                        <div>can be specified with folder name e.g. folder/my_creds</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bt_apikey</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:BT_APIKEY</div>
                                <div>var: bt_apikey</div>
                    </td>
                <td>
                        <div>API key. If not set <code>BT_APIKEY</code> environment variable will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bt_cert_verify</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"no"</div>
                </td>
                    <td>
                                <div>env:BT_CERT_VERIFY</div>
                                <div>var: bt_cert_verify</div>
                    </td>
                <td>
                        <div>Path to cert file, otherwise set to False to disable certificate checking. If not set <code>BT_CERT_VERIFY</code> environment variable will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bt_folder</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                                <div>env:BT_FOLDER</div>
                                <div>var: bt_folder</div>
                    </td>
                <td>
                        <div>folder location in BeyondTrust. If not set <code>BT_FOLDER</code> environment variable will be used.</div>
                        <div>if folder is specified in term this is optional</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bt_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:BT_PASSWORD</div>
                                <div>var: bt_password</div>
                    </td>
                <td>
                        <div>Password. If not set <code>BT_PASSWORD</code> environment variable will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bt_uri</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:BT_URI</div>
                                <div>var: bt_uri</div>
                    </td>
                <td>
                        <div>Base uri. If not set <code>BT_URI</code> environment variable will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bt_username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:BT_USERNAME</div>
                                <div>var: bt_username</div>
                    </td>
                <td>
                        <div>Username. If not set <code>BT_USERNAME</code> environment variable will be used.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is part of the cencora.itoa collection (version 1.1.6).
   - To set up with AWX execution.
   - Order Teams password safe and make sure access is provisioned for service account. You'll need an Active Directory service account. Once you have that, send an email (template to be determined) to PrivilegedAccessManagement@amerisourcebergen.com so they can provision access to your BT safe. Be sure to note your service account should not have multifactor authentication enabled for this.
   - In AWX, create custom credential of type BeyondTrust and provide username, password and api key. Note the name of the BeyondTrust folder your credentials are stored in.
   - Add the custom credential from step 2 to playbook execution template.
   - Add playbook that uses collection lookup vars according to your needs, see below.
   - To install it, use ``ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-beyond_trust``.

You'll also want to create ``collections/requirements.yml`` in your AWX playbook that contains this content

.. code-block:: yaml

    ---
    collections:
      - name: cencora.itoa
        type: git
        source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
        version: 1.1.6



Examples
--------

.. code-block:: yaml

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



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this lookup:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>cred_title</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Credential title as specified in the request e.g. &#x27;folder/my_creds&#x27;</div>
                    <br/>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>file</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>File data encoded in base64.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">TWFueSBoYW5kcyBtYWtlIGxpZ2h0IHdvcmsu</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>Password</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">another_random_password</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>text</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>Contents of text secret.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Lorem ipsum dolor sit amet, consectetur adipiscing elit</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>username</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>Username</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">svc_ansible</div>
                </td>
            </tr>

    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Eduardas Sizovas eduardas.sizovas@amerisourcebergen.com
- Matt Cengic matt.cengic@amerisourcebergen.com
- Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
