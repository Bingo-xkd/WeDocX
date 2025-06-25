from wechat_bot.api_client import start_task, get_task_status
from logging_config import get_bot_logger

logger = get_bot_logger()

# ... existing code ...
    try:
        status_data = await get_task_status(task_id)
        # ...
        await msg.say(response_text)
    except Exception as e:
        logger.error(f"Error checking status for Task ID {task_id}: {e}", exc_info=True)
        await msg.say(f"Error checking status for Task ID {task_id}: An internal error occurred.")


async def handle_start(msg: Message, args: str):
    try:
        # ...
        task_data = await start_task(url)
        task_id = task_data.get("task_id")
        await msg.say(f"Task started successfully!\nTask ID: {task_id}\nI will notify you when it's done.")
        
        # ...
        asyncio.create_task(poll_task_status(msg, task_id))

    except Exception as e:
        logger.error(f"Error starting task for URL {url}: {e}", exc_info=True)
        await msg.say(f"Error starting task for URL {url}: An internal error occurred.")


async def poll_task_status(msg: Message, task_id: str):
    while True:
        try:
            # ...
        except Exception as e:
            logger.error(f"Error polling status for Task ID {task_id}: {e}", exc_info=True)
            await msg.say(f"Error polling status for Task ID {task_id}: An internal error occurred.")
            break
