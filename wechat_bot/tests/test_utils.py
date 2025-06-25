"""
Unit tests for wechat_bot/utils.py
"""

import pytest

from wechat_bot.utils import parse_command, parse_task_id, parse_url


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Check this out: https://www.example.com", "https://www.example.com"),
        ("http://test.com/path?query=1", "http://test.com/path?query=1"),
        ("No url here", None),
        ("ftp://invalid.com", None),
    ],
)
def test_parse_url(text, expected):
    assert parse_url(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "task id is 123e4567-e89b-12d3-a456-426614174000",
            "123e4567-e89b-12d3-a456-426614174000",
        ),
        (
            "ID: 550e8400-e29b-41d4-a716-446655440000.",
            "550e8400-e29b-41d4-a716-446655440000",
        ),
        ("No task id", None),
        ("Invalid-id-format", None),
    ],
)
def test_parse_task_id(text, expected):
    assert parse_task_id(text) == expected


@pytest.mark.parametrize(
    "text, expected_cmd, expected_args",
    [
        ("/start https://example.com", "start", "https://example.com"),
        (
            "/status 123e4567-e89b-12d3-a456-426614174000",
            "status",
            "123e4567-e89b-12d3-a456-426614174000",
        ),
        ("/help", "help", ""),
        ("  /test  arg1 arg2  ", "test", "arg1 arg2"),
        ("not a command", "not a command", ""),
    ],
)
def test_parse_command(text, expected_cmd, expected_args):
    cmd, args = parse_command(text)
    assert cmd == expected_cmd
    assert args == expected_args
