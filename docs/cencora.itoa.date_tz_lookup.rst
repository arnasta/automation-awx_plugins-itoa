.. _cencora.itoa.date_tz_lookup:


********************
cencora.itoa.date_tz
********************

**This plugin converts date string from one timezone to another**


Version added: 1.1.7

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup returns a datetime string after converting it to another timezone.




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
                        <div>Input date string</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>format</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"%m-%d-%Y %H:%M:%S"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[date_tz]<br>format = %m-%d-%Y %H:%M:%S</p>
                            </div>
                    </td>
                <td>
                        <div>Date format e.g. &#x27;%m-%d-%Y %H:%M:%S&#x27;</div>
                        <div>Default data format is &#x27;%m-%d-%Y %H:%M:%S&#x27;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>in_tz</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[date_tz]<br>in_tz = VALUE</p>
                            </div>
                    </td>
                <td>
                        <div>timezone of date string</div>
                        <div>timezone name as specified in pytz library</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>out_format</b>
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
                                    <p>[date_tz]<br>out_format = </p>
                            </div>
                    </td>
                <td>
                        <div>Date format e.g. &#x27;%m-%d-%Y %H:%M:%S&#x27;</div>
                        <div>format is used for output format if this is not defined</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>out_tz</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[date_tz]<br>out_tz = VALUE</p>
                            </div>
                    </td>
                <td>
                        <div>timezone of date string</div>
                        <div>timezone name as specified in pytz library</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is part of the cencora.itoa collection (version 1.1.8).
   - To install it, use ``ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git``.

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
        input_date: "08-25-2023 05:57:37"
        utc_date: "{{ lookup('cencora.itoa.date_tz', input_date, in_tz='EST', out_tz='UTC') }}"
      tasks:
        - debug:
            msg: "EST {{ input_date }} will be {{ utc_date }} in UTC"



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
                    <b>date_string</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Datetime in another timezone</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">08-25-2023 05:57:37</div>
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
