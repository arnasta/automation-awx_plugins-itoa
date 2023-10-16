.. _cencora.itoa.url_to_backend_lookup:


***************************
cencora.itoa.url_to_backend
***************************

**This plugin resolves what backend server(s) are behind url**


Version added: 1.1.9

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup returns list of servers that are servicing specific url.




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
                        <div>url in form of https://my.url.com</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>adm_hostname</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"mas.myabcit.net"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[url_to_backend]<br>adm_hostname = mas.myabcit.net</p>
                            </div>
                    </td>
                <td>
                        <div>Hostname of ADM</div>
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
                                <div>env:ADM_PASSWORD</div>
                    </td>
                <td>
                        <div>Password for user.</div>
                        <div>If the value is not specified, the value of environment variable <code>ADM_PASSWORD</code> will be used instead.</div>
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
                                <div>env:ADM_USERNAME</div>
                    </td>
                <td>
                        <div>Name of user for connection to ADM.</div>
                        <div>If the value is not specified, the value of environment variable <code>ADM_USERNAME</code> will be used instead.</div>
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
                    <b>returned_value</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>List of server dictionaries</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;servicegroupname&#x27;: &#x27;www.amerisourcebergen.com_default_sg&#x27;, &#x27;ip&#x27;: &#x27;20.0.0.0&#x27;, &#x27;port&#x27;: 8080, &#x27;svrstate&#x27;: &#x27;UP&#x27;, &#x27;statechangetimesec&#x27;: &#x27;Wed Sep 20 14:41:12 2023&#x27;, &#x27;tickssincelaststatechange&#x27;: &#x27;187440408&#x27;, &#x27;weight&#x27;: &#x27;1&#x27;, &#x27;servername&#x27;: &#x27;20.0.0.0&#x27;, &#x27;customserverid&#x27;: &#x27;None&#x27;, &#x27;serverid&#x27;: &#x27;0&#x27;, &#x27;state&#x27;: &#x27;ENABLED&#x27;, &#x27;hashid&#x27;: &#x27;0&#x27;, &#x27;graceful&#x27;: &#x27;NO&#x27;, &#x27;delay&#x27;: &#x27;0&#x27;, &#x27;delay1&#x27;: &#x27;0&#x27;, &#x27;nameserver&#x27;: &#x27;0.0.0.0&#x27;, &#x27;dbsttl&#x27;: &#x27;0&#x27;, &#x27;orderstr&#x27;: &#x27;Default&#x27;, &#x27;trofsdelay&#x27;: &#x27;0&#x27;}]</div>
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
