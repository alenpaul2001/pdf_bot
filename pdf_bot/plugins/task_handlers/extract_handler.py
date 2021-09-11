# (c) AlenPaulVarghese
# -*- coding: utf-8 -*-

from tools import task_checker, parse_range, mediagroup_generator
from pyrogram.types import Message, InputMediaPhoto
from pyrogram import filters
from tools import Extractor
from pdfbot import Pdfbot
import traceback
import asyncio


@Pdfbot.on_message(filters.command(["extract"]) & filters.create(task_checker))
async def extract_handler(client: Pdfbot, message: Message) -> None:
    if (
        message.reply_to_message is None
        or not message.reply_to_message.document
        or message.reply_to_message.document.mime_type != "application/pdf"
    ):
        await message.reply("Please reply to a PDF file")
        return
    if len(message.command) == 1:
        await message.reply("**usage:** `/extract page-range`")
        return
    status = await message.reply_text("**downloading...**")
    task = client.new_task(Extractor, message.chat.id, message.message_id)
    input_file = task.cwd / f"{message.reply_to_message.message_id}.pdf"
    await message.reply_to_message.download(input_file)
    await status.edit("**processing...**")
    try:
        page_range = parse_range(message.command[1])
        page_range.sort()
        task.set_configuration(input_file, set(page_range))
        await client.process_pool.new_task(task)
        image_list = [
            InputMediaPhoto(str(task.cwd / f"output-{index:02}.jpg"), f"page-{index}")
            for index in task.page_range
        ]
        for media_group in mediagroup_generator(image_list):
            await asyncio.gather(
                message.reply_chat_action("upload_photo"),
                message.reply_media_group(
                    media_group,
                    disable_notification=True,
                ),
            )
        await status.delete()
    except Exception as e:
        traceback.print_exc()
        await status.edit(f"**Task failed: `{e}`**")
    finally:
        task.cleanup()
        client.task_pool.remove_task(message.chat.id)
