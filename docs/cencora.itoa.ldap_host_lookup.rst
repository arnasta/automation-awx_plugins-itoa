.. _cencora.itoa.ldap_host_lookup:


**********************
cencora.itoa.ldap_host
**********************

**This plugin gets host info from ldap**


Version added: 1.1.4

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup returns a dictionary of host info from ldap server



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
                        <b>Default:</b><br/><div style="color: blue">"cn,description,distinguishedName,dNSHostName,lastLogonTimestamp,objectGUID,objectSid,operatingSystem,operatingSystemVersion,primaryGroupID"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>A list of object attributes to return (both computer and group)</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_base_dn</b>
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
                                    <p>[ldap_host_lookup]<br>group_base_dn = </p>
                            </div>
                    </td>
                <td>
                        <div>base dn for groups</div>
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
                    <b>server_base_dn</b>
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
                        <div>base dn for servers</div>
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
   - This module is part of the cencora.itoa collection (version 1.1.7).
   - To install it, use ``ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git``.

You'll also want to create ``collections/requirements.yml`` in your AWX playbook that contains this content

.. code-block:: yaml

    ---
    collections:
      - name: cencora.itoa
        type: git
        source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
        version: 1.1.7



Examples
--------

.. code-block:: yaml

    ---
    - name: Get host info from LDAP
      hosts: 127.0.0.1
      gather_facts: false
      become: false
      collections:
        - cencora.itoa
      vars:
        server_name: 'test01.abc.amerisourcebergen.com'
        username: 'a132171'
        password: 'mypass'
        host_info: "{{ lookup('cencora.itoa.ldap_host', server_name, username=username, password=password) }}"
      tasks:
        - debug:
            msg:
              - "{{server_name}}: {{ host_info }}"



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
                    <b>computer_info</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>info from computer search</div>
                    <br/>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>distinguishedName</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>unique attribute in LDAP that hierarchically identifies an entry within the directory tree</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">CN=MyComputer,OU=Computers,DC=example,DC=com</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>dNSHostName</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>contains the FQDN of a computer, which includes the hostname and the complete domain name</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">mycomputer.example.com</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>lastLogonTimestamp</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>date when a computer account logged onto the domain</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">8/31/2023 11:37:15 PM Eastern Daylight Time</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>objectGUID</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>a 128-bit value that is globally unique across all LDAP directories</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">12345678-9abc-def0-1234-56789abcdef0</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>objectSid</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>security identifier for security principals within an Active Directory environment,</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">S-1-5-21-3623811015-3361044348-30300820-1013</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>operatingSystem</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>Operating System of the computer</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Red Hat Enterprise Linux release 9.1</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>operatingSystemVersion</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>Operating System version</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Linux 4.18.0-193.14.3.el8_2.x86_64</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>primaryGroupID</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when supported</td>
                <td>
                            <div>used to specify the primary group for a user account</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">513 = ( GROUP_RID_COMPUTERS )</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>group_info</b>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;cn&#x27;: &#x27;prd_access_localadm_mycomputer&#x27;, &#x27;description&#x27;: &#x27;Local Admin Access to Server mycomputer&#x27;, &#x27;distinguishedName&#x27;: &#x27;CN=prd_access_localadm_mycomputer,OU=Server,OU=Access,OU=Enterprise,OU=ABCGroups,DC=abc,DC=amerisourcebergen,DC=com&#x27;, &#x27;objectGUID&#x27;: &#x27;12345678-9abc-def0-1234-56789abcdef0&#x27;, &#x27;objectSid&#x27;: &#x27;S-1-5-21-3623811015-3361044348-30300820-1013&#x27;}]</div>
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
