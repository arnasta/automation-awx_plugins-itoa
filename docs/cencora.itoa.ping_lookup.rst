.. _cencora.itoa.ping_lookup:


*****************
cencora.itoa.ping
*****************

**This plugin is used to ping host using ICMP**


Version added: 1.1.8

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup returns response time of ping packet.
- It utilizes ping command in os.




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
                        <div>IP address or hostname to ping</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>size</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">56</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ping]<br>size = 56</p>
                            </div>
                    </td>
                <td>
                        <div>Size of ICMP packet payload in bytes</div>
                        <div>Size value range is 1-65500</div>
                        <div>The total ICMP packet size is 8 bytes larger.</div>
                        <div>E.g. 8 (header) + 56 (payload) = 64 bytes</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">4</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ping]<br>timeout = 4</p>
                            </div>
                    </td>
                <td>
                        <div>Timeout value of ping packet</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ttl</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">64</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ping]<br>ttl = 64</p>
                            </div>
                    </td>
                <td>
                        <div>Time-To-Live value of ICMP packet</div>
                        <div>The packet is discarded if it does not reach the target host after jumps in under TTL value</div>
                        <div>TTL value range is 1-255</div>
                        <div>If value is out of range default will be used</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>unit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"s"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ping]<br>unit = s</p>
                            </div>
                    </td>
                <td>
                        <div>Unit of returned value</div>
                        <div>Can be ms for milliseconds or s for seconds</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is part of the cencora.itoa collection (version 1.1.8).
   - To install it, use ``ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git``.
   - Plugin sends 4 ping packets
   - Plugin returns '' empty string is host is unreachable
   - Plugin returns False if there was antoher error
   - To look at errors use verbose run mode

You'll also want to create ``collections/requirements.yml`` in your AWX playbook that contains this content

.. code-block:: yaml

    ---
    collections:
      - name: cencora.itoa
        type: git
        source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
        version: 1.1.8



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
        hostname: "example.com"
        ping_result: "{{ lookup('cencora.itoa.ping', hostname) }}"
      tasks:
        - debug:
            msg: "Ping of {{ hostname }} is {{ ping_result }}"



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
                    <b>ping_time</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">float</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Ping result</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">0.21569726151007967</div>
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
