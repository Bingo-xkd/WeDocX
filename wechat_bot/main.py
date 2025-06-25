"""
Wechaty Bot Main Entry
"""
import asyncio
import os
from typing import Optional

from wechaty import Wechaty, WechatyOptions, Message, Room
from wechaty_puppet import MessageType

from command_handler import handle_command, poll_task_status
from wechat_bot.utils import parse_url
from wechat_bot.api_client import start_task
from logging_config import setup_bot_logging, get_bot_logger

logger = get_bot_logger()


async def main():
    """
    Async Main function
    """
    setup_bot_logging()
    # Set Wechaty token
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        logger.error('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a token to run the Wechaty bot.
            You can get a free token from https://wechaty.js.org/docs/token
        ''')
        return

    options = WechatyOptions()
    bot = Wechaty(options)

    bot.on('message', on_message)

    await bot.start()

    logger.info(f'Bot {bot.name()} started.')


async def on_message(msg: Message):
    """
    Message handler function
    """
    if msg.is_self() or msg.age() > 60:
        return

    room: Optional[Room] = msg.room()
    talker = msg.talker()
    msg_type = msg.type()
    text = msg.text()

    # 首先检查是否是指令
    if msg_type == MessageType.MESSAGE_TYPE_TEXT:
        is_command = await handle_command(msg)
        if is_command:
            return

    # 根据消息类型进行不同处理
    if msg_type == MessageType.MESSAGE_TYPE_TEXT:
        log_message(room, talker, f'Received Text: {text}')
    elif msg_type == MessageType.MESSAGE_TYPE_URL:
        url = parse_url(text)
        if url:
            log_message(room, talker, f'Received URL: {url}')
            try:
                task_data = await start_task(url)
                task_id = task_data.get("task_id")
                await msg.say(f"Task started successfully!\nTask ID: {task_id}\nI will notify you when it's done.")
                # Start a background task to poll for the result
                asyncio.create_task(poll_task_status(msg, task_id))
            except Exception as e:
                await msg.say(f"Error starting task for URL {url}: {e}")
        else:
            log_message(room, talker, f'Could not parse URL from message: {text}')
    elif msg_type == MessageType.MESSAGE_TYPE_IMAGE:
        log_message(room, talker, 'Received an Image.')
    else:
        log_message(room, talker, f'Received an unhandled message type: {msg_type.name}')


async def log_message(room: Optional[Room], talker, content: str):
    """Helper function to log messages"""
    if room:
        topic = await room.topic()
        logger.info(f'Room: "{topic}" | Talker: "{talker.name}" | Content: {content}')
    else:
        logger.info(f'Private Chat | Talker: "{talker.name}" | Content: {content}')


if __name__ == "__main__":
    asyncio.run(main()) 