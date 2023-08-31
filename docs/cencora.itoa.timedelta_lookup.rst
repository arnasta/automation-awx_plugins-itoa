.. _cencora.itoa.timedelta_lookup:


**********************
cencora.itoa.timedelta
**********************

**This plugin calculates timedelta**


Version added: 0.1

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup returns a datetime string after adding or subtracting timedelta.




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
                    <b>delta</b>
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
                                    <p>[timedelta_lookup]<br>delta = VALUE</p>
                            </div>
                    </td>
                <td>
                        <div>Time delta string in form of &#x27;-1 day&#x27;</div>
                        <div>First character should be sign &#x27;+&#x27; or &#x27;-&#x27;</div>
                        <div>Amount should go after sign</div>
                        <div>Units should follow the amount separated by space</div>
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
                        <b>Default:</b><br/><div style="color: blue">"%Y-%m-%dT%H:%M:%S.%f%z"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[timedelta_lookup]<br>format = %Y-%m-%dT%H:%M:%S.%f%z</p>
                            </div>
                    </td>
                <td>
                        <div>Date format e.g. &#x27;%m-%d-%Y %H:%M:%S&#x27;</div>
                        <div>Default data forma is &#x27;%Y-%m-%dT%H:%M:%S.%f%z&#x27;</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is part of the cencora.itoa collection (version 1.1.1).
   - To install it, use ``ansible-galaxy collection install git+https://github.com/abcorp-itops/automation-awx_plugins-itoa.git``.


You'll also want to create ``collections/requirements.yml`` in your AWX playbook that contains this content

.. code-block:: yaml

    ---
    collections:
      - name: cencora.itoa
        type: git
        source: https://github.com/abcorp-itops/automation-awx_plugins-itoa
        version: 1.1.1



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
        future_date: "{{ lookup('cencora.itoa.timedelta', input_date, delta='+16 days', format='%m-%d-%Y %H:%M:%S') }}"
      tasks:
        - debug:
            msg: "16 days from {{ input }} will be {{ future_date }}"



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
                            <div>Date with timedelta applied</div>
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
