.. _cencora.itoa.ldap_user_lookup:


**********************
cencora.itoa.ldap_user
**********************

**This plugin gets host info from ldap**


Version added: 1.1.6

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup returns user info from ldap server



Requirements
------------
The below requirements are needed on the local Ansible controller node that executes this lookup.

- python ldap3


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
                        <div>server hostname</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>attributes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"c,cn,co,company,department,displayName,distinguishedName,employeeNumber,givenName,info,l,lastLogon,mail,manager,mobile,name,physicalDeliveryOfficeName,sAMAccountName,sn,streetAddress,title,userPrincipalName"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>A list of object attributes to return</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>base_dn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ldap_host_lookup]<br>server_base_dn = </p>
                            </div>
                    </td>
                <td>
                        <div>base dn for user search</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:LDAP_PASSWORD</div>
                    </td>
                <td>
                        <div>Password for username.</div>
                        <div>If the value is not specified, the value of environment variable <code>LDAP_PASSWORD</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>server</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"abcldap.abc.amerisourcebergen.com"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ldap_host_lookup]<br>server = abcldap.abc.amerisourcebergen.com</p>
                            </div>
                    </td>
                <td>
                        <div>LDAP server address</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:LDAP_USERNAME</div>
                    </td>
                <td>
                        <div>Name of user for connection to LDAP.</div>
                        <div>If the value is not specified, the value of environment variable <code>LDAP_USERNAME</code> will be used instead.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is part of the cencora.itoa collection (version 1.1.9).
   - To install it, use ``ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git``.

You'll also want to create ``collections/requirements.yml`` in your AWX playbook that contains this content

.. code-block:: yaml

    ---
    collections:
      - name: cencora.itoa
        type: git
        source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
        version: 1.1.9



Examples
--------

.. code-block:: yaml

    ---
    - name: Get user info from LDAP
      hosts: 127.0.0.1
      gather_facts: false
      become: false
      collections:
        - cencora.itoa
      vars:
        user_id: 'a132171'
        username: 'a132171'
        password: 'mypass'
        user_info: "{{ lookup('cencora.itoa.ldap_host', user_id, username=username, password=password) }}"
      tasks:
        - debug:
            msg:
              - "{{user_id}}: {{ user_info }}"



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this lookup:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>users</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>info from group search</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;c&#x27;: &#x27;US&#x27;, &#x27;cn&#x27;: &#x27;John, Doe (a123456_tr1)&#x27;, &#x27;co&#x27;: &#x27;United States of America&#x27;, &#x27;company&#x27;: &#x27;AmerisourceBergen Drug Corporation&#x27;, &#x27;department&#x27;: &#x27;Foundation Reliability&#x27;, &#x27;displayName&#x27;: &#x27;a123456_tr1&#x27;, &#x27;distinguishedName&#x27;: &#x27;CN=John\\, Doe (a123456_tr1),OU=Accounts,OU=Tier1,OU=Admin,DC=abc,DC=amerisourcebergen,DC=com&#x27;, &#x27;employeeNumber&#x27;: &#x27;123456&#x27;, &#x27;givenName&#x27;: &#x27;John&#x27;, &#x27;info&#x27;: &#x27;This Account was created by an automated process via MYID&#x27;, &#x27;l&#x27;: &#x27;Middle of Nowhere&#x27;, &#x27;lastLogon&#x27;: &#x27;9/20/2023 10:47:19 AM Eastern Daylight Time&#x27;, &#x27;mail&#x27;: &#x27;a123456_tr1@amerisourcebergen.com&#x27;, &#x27;manager&#x27;: &#x27;CN=Mr.\\, T (a000001),OU=Enterprise,OU=ABCUsers,DC=abc,DC=amerisourcebergen,DC=com&#x27;, &#x27;mobile&#x27;: &#x27;01234567890&#x27;, &#x27;name&#x27;: &#x27;John, Doe (A123456)&#x27;, &#x27;physicalDeliveryOfficeName&#x27;: &#x27;USA Remote - Middle of Nowhere&#x27;, &#x27;sAMAccountName&#x27;: &#x27;a123456&#x27;, &#x27;sn&#x27;: &#x27;Doe&#x27;, &#x27;streetAddress&#x27;: &#x27;Mulholland Drive 42&#x27;, &#x27;title&#x27;: &#x27;IT Operations Automation Developer&#x27;, &#x27;userPrincipalName&#x27;: &#x27;a123456@amerisourcebergen.com&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Arnas Tamulionis arnas.tamulionis@amerisourcebergen.com


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
