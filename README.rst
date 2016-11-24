===============
Datadog Builder
===============

Build and manage datadog monitors.

* Free software: Apache Software License 2.0

Authentication
==============

Authentication can be performed by the following envrionment variables:

.. code-block: bash

    export DATADOG_API_KEY="<YOUR API KEY>"
    export DATADOG_APP_KEY="<YOUR APP KEY>"
    export DATADOG_HOST="https://app.datadoghq.com"

Or a config yaml file containing the following:

.. code-block:: yaml

    api_key: <YOUR API KEY>
    app_key: <YOUR APP KEY>
    host_name:
    api_host: https://app.datadoghq.com
    statsd_host:
    statsd_port:
    statsd_use_default_route: False


Jobs File Format
================

The monitors are basically directly representative of the `datadog api`_.

.. code-block:: yaml

    defaults:
      monitors:
        multi: true
        options:
          locked: true

    monitors:
      - name: My monitor
        type: service check

        message: |
          Service is down. That's probably bad.

          {{#is_alert}}fix it{{/is_alert}}
          {{#is_alert_recovery}}fix it{{/is_alert_recovery}}

        query: '"process.up".over("host:myhost","process:service").last(3).count_by_status()'

        options:
          new_host_delay: 300
          notify_audit: false
          notify_no_data: false
          thresholds:
            critical: 1
            ok: 1
            warning: 1

.. _datadog api: http://docs.datadoghq.com/api/#monitor-create
