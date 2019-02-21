#!/usr/bin/env python3
"""
    Purpose:
        Test File for slack_helpers.py
"""

# Python Library Imports
import os
import sys
import simplejson
import pytest
from unittest import mock

# Import File to Test
from slack_helpers import slack_helpers


###
# Fixtures
###

#
# Payload Fixtures
#


@pytest.fixture
def example_message():
    """
    Purpose:
        Set example message to show in Slack
    Args:
        N/A
    Return:
        example_message (Pytest Fixture (String)): example message to show in Slack
    """

    return "This is an example message"


@pytest.fixture
def example_channel():
    """
    Purpose:
        Set example channel to post to in Slack
    Args:
        N/A
    Return:
        example_channel (Pytest Fixture (String)): example channel to post to in Slack
    """

    return "#fake_channel"


@pytest.fixture
def example_name():
    """
    Purpose:
        Set example username to show in Slack
    Args:
        N/A
    Return:
        example_name (Pytest Fixture (String)): example name to post to in Slack
    """

    return "fake-name"


@pytest.fixture
def example_icon():
    """
    Purpose:
        Set example icon to show in Slack
    Args:
        N/A
    Return:
        example_icon (Pytest Fixture (String)): example icon to post to in Slack
    """

    return ":parrot:"


@pytest.fixture
def example_payload(example_message, example_channel, example_name, example_icon):
    """
    Purpose:
        Set example payload with all values set (superset of other fixtures)
    Args:
        example_message (Pytest Fixture (String)): example message to show in Slack
        example_channel (Pytest Fixture (String)): example channel to post to in Slack
        example_name (Pytest Fixture (String)): example name to post to in Slack
        example_icon (Pytest Fixture (String)): example icon to post to in Slack
    Return:
        example_payload (Pytest Fixture (JSON Object)): example payload with all values
            set (superset of other fixtures)
    """

    return slack_helpers.build_slack_payload(
        example_message, channel=example_channel, name=example_name, icon=example_icon
    )


#
# Header Fixtures
#


@pytest.fixture
def example_headers():
    """
    Purpose:
        Set example headers for posting to Slack
    Args:
        N/A
    Return:
        example_headers (Pytest Fixture (Object)): Set example headers for posting to
            Slack
    """

    return {
        "Content-Type": "application/json"
    }


#
# Slack Specific Fixtures
#


@pytest.fixture
def example_url():
    """
    Purpose:
        Set example URL for posting to Slack
    Args:
        N/A
    Return:
        example_url (Pytest Fixture (String)): example URL for posting to Slack
    """

    return (
        "https://hooks.slack.com/services/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"
    )


###
# Mocked Functions
###


class MockRequestResponse(object):
    """
    Purpose:
        Mock a Request POST
    """

    def __init__(self, json_data, status_code):
        """
        Purpose:
            Initialize the MockRequestResponse Object
        """

        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """
        Purpose:
            Return the json_data from the call
        """

        return self.json_data


def mocked_requests_post_successful(*args, **kwargs):
    """
    Purpose:
        Mock a successful request
    """

    return MockRequestResponse({}, 200)


def mocked_requests_post_failure(*args, **kwargs):
    """
    Purpose:
        Mock a successful request
    """

    return MockRequestResponse(None, 404)


###
# Test Payload
###


def test_build_payload_empty():
    """
    Purpose:
        Tests that a payload needs a message
    Args:
        N/A
    Return:
        N/A
    """

    with pytest.raises(Exception):
        payload = slack_helpers.build_slack_payload()


def test_build_payload_only_message(example_message):
    """
    Purpose:
        Tests that a payload message is set properly
    Args:
        example_message (Pytest Fixture (String)): example message to show in Slack
    Return:
        N/A
    """

    expected_payload = {"text": example_message}
    payload = slack_helpers.build_slack_payload(example_message)

    assert payload == simplejson.dumps(expected_payload)


def test_build_payload_with_channel(example_message, example_channel):
    """
    Purpose:
        Tests that a payload channel is set properly
    Args:
        example_message (Pytest Fixture (String)): example message to show in Slack
        example_channel (Pytest Fixture (String)): example channel to post to in Slack
    Return:
        N/A
    """

    expected_payload = {"text": example_message, "channel": example_channel}
    payload = slack_helpers.build_slack_payload(
        example_message, channel=example_channel
    )

    assert payload == simplejson.dumps(expected_payload)


def test_build_payload_with_name(example_message, example_name):
    """
    Purpose:
        Tests that a payload name is set properly
    Args:
        example_message (Pytest Fixture (String)): example message to show in Slack
        example_name (Pytest Fixture (String)): example name to post to in Slack
    Return:
        N/A
    """

    expected_payload = {"text": example_message, "username": example_name}
    payload = slack_helpers.build_slack_payload(example_message, name=example_name)

    assert payload == simplejson.dumps(expected_payload)


def test_build_payload_with_icon(example_message, example_icon):
    """
    Purpose:
        Tests that a payload icon is set properly
    Args:
        example_message (Pytest Fixture (String)): example message to show in Slack
        example_icon (Pytest Fixture (String)): example icon to post to in Slack
    Return:
        N/A
    """

    expected_payload = {"text": example_message, "icon_emoji": example_icon}
    payload = slack_helpers.build_slack_payload(example_message, icon=example_icon)

    assert payload == simplejson.dumps(expected_payload)


###
# Test Headers
###


def test_build_headers(example_headers):
    """
    Purpose:
        Tests that a payload icon is set properly
    Args:
        example_headers (Pytest Fixture (Object)): Set example headers for posting to
            Slack
    Return:
        N/A
    """

    expected_headers = example_headers
    headers = slack_helpers.build_slack_headers()

    assert headers == expected_headers


###
# Test Request/Post
###


@mock.patch("requests.post", side_effect=mocked_requests_post_successful)
def test_post_to_slack_successful(mocked_method, example_url, example_payload, example_headers):
    """
    Purpose:
        Tests succesfully posting to slack (spoofs the request)
    Args:
        example_url (Pytest Fixture (String)): example URL for posting to Slack
        example_payload (Pytest Fixture (JSON Object)): example payload with all values
            set (superset of other fixtures)
        example_headers (Pytest Fixture (Object)): Set example headers for posting to
            Slack
    Return:
        N/A
    """

    response = slack_helpers.post_to_slack(
        example_url, example_payload, example_headers
    )

    assert response.status_code == 200
    assert response.json_data == {}


@mock.patch("requests.post", side_effect=mocked_requests_post_failure)
def test_post_to_slack_failure(mocked_method, example_url, example_payload, example_headers):
    """
    Purpose:
        Tests failure in posting to slack (spoofs the request)
    Args:
        example_url (Pytest Fixture (String)): example URL for posting to Slack
        example_payload (Pytest Fixture (JSON Object)): example payload with all values
            set (superset of other fixtures)
        example_headers (Pytest Fixture (Object)): Set example headers for posting to
            Slack
    Return:
        N/A
    """

    with pytest.raises(Exception):
        response = slack_helpers.post_to_slack(
            example_url, example_payload, example_headers
        )
