Webhooks plugin for `Tutor <https://docs.tutor.edly.io>`__
##########################################################

This plugin will to Open edX the capability to send requests to configurable URLs
after certain events happen.

A `Webhook` is a mechanism that triggers an HTTP POST request to a configurable
URL when certain events happen in the platform, including information relevant
to the event. For example, you can make the platform call an API when a user
logs in, including the user ID and email to connect to another application.

A `Webfilter` is a special case of webhook that allows also modifying the
data and/or interrupting the process. For example, after the user login event
you can update the user full name or prevent the user to log in if it is not
allowed to.

Installation
************

.. code-block::

    pip install tutor-contrib-webhooks

Usage
*****

To enable the functionality you will have to rebuild the Open edX image
and restart the containers. No other configuration is needed.

.. code-block::

    tutor plugins enable webhooks
    tutor images build openedx


How it works
************

This Tutor plugin will just add the `openedx-webhooks <https://pypi.org/project/openedx-webhooks/>`_
module to the list of dependencies of Open edX.

To learn more please refer to the `source code <https://github.com/aulasneo/openedx-webhooks>`_ of openedx-webhooks.

Configuration
*************

A new section named `OPENEDX_WEBHOOKS` will be available in the LMS Django
admin site. It will contain two subsections: `Webhooks` and `Webfilters`.
Add a new webhook to define the URLs that will be called after each event is
received. More than one URL can be configured for each event. In this case,
all URLs will be called.

Configuring webhooks
--------------------

The `Webhooks` Django admin panel has the following settings:

* Description: Add a description for this webhook for reference.
* Event: Choose from the list the event that will trigger the webhook.
* Webhook URL: URL to call. Get it from your webhook processor.
* Enabled: Click to enable the webhook.
* Use WWW form encoding: When enabled, the data will be passed in a web form format. If disabled, data will be passed in JSON format.

Configuring webfilters
----------------------

The `Webfilters` Django admin panel has the following settings:

* Description: Add a description for this webhook for reference.
* Event: Choose from the list the event that will trigger the webhook.
* Webhook URL: URL to call. Get it from your webhook processor.
* Enabled: Click to enable the webhook.
* Disable filtering: If enabled, the data passed to the web filter will not be modified even if the response includes any update.
* Disable halting: If enabled, the process will not be interrupted even if the response includes an exception setting.
* Halt on 4xx: Interrupt the process if the call to the URL returns any 4xx error code.
* Redirect on 4xx: Include an URL to redirect in case of a 4xx response, if the event supports redirection.
* Halt on 5xx: Interrupt the process if the call to the URL returns any 5xx error code.
* Redirect on 5xx: Include an URL to redirect in case of a 5xx response, if the event supports redirection.
* Halt on request exception: Interrupt the process if the call to the URL results in a connection error (e.g., timeout).
* Redirect on request exception: Include an URL to redirect in case of a connection error, if the event supports redirection.
* Use WWW form encoding: When enabled, the data will be passed in a web form format. If disabled, data will be passed in JSON format.

Receiving data
--------------

Both webhooks and webfilters will trigger POST requests to the configured URL.
This request includes in the payload a structure with data relevant to the
event that triggered the call. In all cases, the payload will include an
``event_metadata`` key including at least the event type and the date and time
in UTC format. Other keys included will depend on the event. For example,
log in events usually include ``user`` and ``profile`` keys with details of the
user logging in.

If the ``Use WWW form encoding`` option is enabled, the data will be passed as
plain key-value pairs in form encoding. The structure will be flattened and the
key names will be concatenated. E.g., a log event will include ``user_id``,
``user_email``, ``event_metadata_time``, etc.

Responding to webfilters
------------------------

The webhook processor should respond to a webfilter with a data structure in
JSON format and a successful status code (200). The response can be empty or
can have one or both of these keys:

* data
* exception

Updating data
~~~~~~~~~~~~~

The corresponding objects will be updated with the values returned inside the
``data`` key. Only keys present in the response will be updated. Other keys
will remain unchanged in the original data structures. To disable data updates,
set ``Disable Filtering`` in the webfilter configuration at the Django admin
panel.

For example, to change the full name of a user at registration time, respond
to a `Student Registration Requested` webfilter with this data:

.. code-block::

    {
        "data": {
            "form_data": {
                "name": "New Name"
            }
        }
    }

Interrupting execution
~~~~~~~~~~~~~~~~~~~~~~

To stop the process to complete, add a JSON object as value for the `exception`
key. This object must have only one key-value pair, being the key the name
of the exception to raise. Its value can be either a string representing the
message to be shown, or another JSON object with more data.

For example, to prevent a user to register, respond to the `Student
Registration Requested` webfilter with this data:

.. code-block::

    {
        "exception": {
            "PreventRegistration": "Not allowed to register"
        }
    }

To prevent a webfilter to stop the execution of the process, set ``Disable
halting`` in the webfilter configuration at the Django admin
panel.

Check each function documentation to see the list of available values and
exceptions.

Handling multiple events
------------------------

If you set more than one webhook or webfilter for the same event, all of them
will be triggered. The responses of all the webfilters will be combined in one
data structure and used to update the objects. If more webfilter processors
include data for the same key, the last one will override all the previous.

License
*******

This software is licensed under the terms of the AGPLv3.
