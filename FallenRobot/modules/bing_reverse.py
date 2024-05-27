# Bing reverse api made by @Qewertyy
# This module is made by @Dhruv-Tara
# Licensed under MIT License
# Copyright (c) 2022-2024 AnonymousX1025
 
from .. import dispatcher, TOKEN
from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
import requests


async def bing_reverse_image(image_url):
    url = "https://api.qewertyy.dev/image-reverse/bing?img_url="

    get_path = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={image_url}"
        ).json()
    
    file_path = get_path["result"]["file_path"]
    resp = await requests.post(f"{url}https://api.telegram.org/file/bot${Token}/${file_path}")

    if resp.data.code == 2: 
        return_str = "Showing Top 5 results from Bing:\n\n"

        for i in range(5):
            return_str += f"{i+1} - {resp.data.content.bestResults[i].name}\n\n"

        return return_str
    
    else:
        return "No results found."
    


async def bing_reverse(update: Update, context: CallbackContext):
    
    message = update.effective_message
    reply = update.effective_message.reply_to_message

    if not reply :
        await message.reply_text("Reply to a photo to reverse search it.")
        return
    
    elif not reply.photo and not reply.document.mime_type == "image/png" :
        await message.reply_text("Reply to a photo to reverse search it.")
        return
    
    else :
        
        edit_message = await message.reply_text("Searching results in Bing....")
        file_id = reply.photo[-1].file_id if reply.photo else reply.document.file_id
        edit = await bing_reverse_image(file_id)
        await edit_message.edit_text(edit)
        return
    


BING_REVERSE_HANDLER = CommandHandler(['pp','reverse'], bing_reverse)
dispatcher.add_handler(BING_REVERSE_HANDLER)