#!/usr/bin/env python3
"""
    Purpose:
        Helper Library for Sending Messages to a Slack Webhook
"""

# Python Library Imports
import logging
import simplejson
import requests


###
# Slack Helpers
###


def post_to_slack(webhook_url, payload, headers):
    """
    Purpose:
        Post Payload (JSON) to Slack Channel
    Args:
        webhook_url (String): URL for Slack Webhook accepting requests
        payload (JSON Obj): JSON Object payload to send Slack Webhook
        headers (Dict): Dictionary of headers to send Slack Webhook
    Returns:
        response (Requests Reponse Object): Response object from Slack Webhook
    """
    logging.info(f"Sending Alert in Slack: {payload}")

    response = requests.post(
        webhook_url,
        data=payload,
        headers=headers,
    )

    if response.status_code != 200:
        error_msg = f"Slack Message Failed to Send: code = {response.status_code}, "\
            "message = {response.message}"
        logging.error(error_msg)
        raise Exception(error_msg)

    return response


def build_slack_payload(message, channel=None, name=None, icon=None):
    """
    Purpose:
        Build the Payload to send to the Slack Webhook
    Args:
        message (String): Message to send the Slack Webhook
        channel (String): Channel to post to. if not set, use Webhook default
        name (String): Name to post as. if not set, use Webhook default
        icon (String): Icon to display in Slack. if not set, use Webhook default
    Returns:
        payload (JSON Obj): JSON Object payload to send Slack Webhook
    """

    payload = {
        "text": message,
    }

    if channel:
        payload["channel"] = channel
    if name:
        payload["username"] = name
    if icon:
        payload["icon_emoji"] = icon

    return simplejson.dumps(payload)


def build_slack_headers():
    """
    Purpose:
        Build the Header to send to the Slack Webhook
    Args:
        N/A
    Returns:
        headers (Dict): Dictionary of headers to send Slack Webhook
    """

    return {
        'Content-Type': 'application/json',
    }
