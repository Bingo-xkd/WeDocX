"""
Utility functions for the Wechaty Bot
"""
import re
from typing import Optional, Tuple

URL_REGEX = r'(https?://[^\s]+)'
TASK_ID_REGEX = r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b'


def parse_url(text: str) -> Optional[str]:
    """
    Parse URL from text.
    Returns the first URL found.
    """
    match = re.search(URL_REGEX, text)
    if match:
        return match.group(0)
    return None


def parse_task_id(text: str) -> Optional[str]:
    """
    Parse Task ID from text.
    Returns the first Task ID found.
    """
    match = re.search(TASK_ID_REGEX, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return None

def parse_command(text: str) -> Tuple[str, str]:
    """
    Parse command and its arguments from text.
    e.g. "/status my-task-id" -> ("status", "my-task-id")
    """
    parts = text.strip().split(maxsplit=1)
    command = parts[0].lstrip('/').lower()
    args = parts[1] if len(parts) > 1 else ""
    return command, args 