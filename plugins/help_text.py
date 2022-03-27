#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K & @No_OnE_Kn0wS_Me
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters 
from pyrogram import Client as Mai_bOTs

#from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram

from pyrogram.errors import UserNotParticipant, UserBannedInChannel 
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from database.database import *
from database.db import *


@Mai_bOTs.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry, You're Banned")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Due To The Huge Traffic Only Channel Members Can Use This Bot Means You Need To Join The Below Mentioned Channel Before Using Me! **",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="𝙹𝚘𝚒𝚗 𝙼𝚢 𝚄𝚙𝚍𝚊𝚝𝚎 𝙲𝚑𝚊𝚗𝚗𝚎𝚕", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📝𝚁𝚎𝚗𝚊𝚖𝚎', callback_data = "rnme"),
                    InlineKeyboardButton('📂𝙵𝚒𝚕𝚎 𝚃𝚘 𝚅𝚒𝚍𝚎𝚘', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('🎞️𝙲𝚞𝚜𝚝𝚘𝚖 𝚃𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕', callback_data = "cthumb"),
                    InlineKeyboardButton('📑𝙲𝚞𝚜𝚝𝚘𝚖 𝙲𝚊𝚙𝚝𝚒𝚘𝚗', callback_data = "ccaption"),
                ]
            ]
        )
    )       

@Mai_bOTs.on_message(pyrogram.filters.command(["start"]))
async def start_me(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("You are Banned")
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry,You've Been Flooding Me So My Owner Removed You From Using Me If You Think It's An Error Contact : @mr_MKN")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Due To The Huge Traffic Only Channel Members Can Use This Bot Means You Need To Join The Below Mentioned Channel Before Using Me! **",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_photo(
                photo="https://telegra.ph/file/3423a131fbb267aa93021.png",
                caption=f"👋 𝙷𝚊𝚒 {update.from_user.first_name} , \n𝙸'𝚖 𝙰 𝚂𝚒𝚖𝚙𝚕𝚎 𝙵𝚒𝚕𝚎 𝚁𝚎𝚗𝚊𝚖𝚎+𝙵𝚒𝚕𝚎 𝚃𝚘 𝚅𝚒𝚍𝚎𝚘 𝙲𝚘𝚟𝚎𝚛𝚝𝚎𝚛 𝙱𝙾𝚃 𝚆𝚒𝚝𝚑 𝙿𝚎𝚛𝚖𝚊𝚗𝚎𝚗𝚝 𝚃𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕 𝙰𝚗𝚍 𝙲𝚞𝚜𝚝𝚘𝚖 𝙲𝚊𝚙𝚝𝚒𝚘𝚗 𝚂𝚞𝚙𝚙𝚘𝚛𝚝! \n𝙱𝙾𝚃 𝙲𝚛𝚎𝚊𝚝𝚎𝚍 𝙱𝚢: @mr_MKN & @Mr_MKN_TG \n ",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("ℹ️ 𝙷𝙴𝙻𝙿 ℹ️", callback_data = "ghelp")
                ],
                [
                    InlineKeyboardButton('🤠 𝙲𝚁𝙴𝙰𝚃𝙴𝚁 🤠', url='https://t.me/mr_MKN'),
                    InlineKeyboardButton('📢 support group 📢', url='https://t.me/MKN_BOTZ_DISCUSSION_GROUP'),
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )
            return 

@Mai_bOTs.on_callback_query()
async def cb_handler(client: Mai_bOTs , query: CallbackQuery):
    data = query.data
    if data == "rnme":
        await query.message.edit_text(
            text=Translation.RENAME_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "f2v":
        await query.message.edit_text(
            text=Translation.C2V_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "ccaption":
        await query.message.edit_text(
            text=Translation.CCAPTION_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝚂𝚑𝚘𝚠 𝙲𝚞𝚛𝚛𝚎𝚗𝚝 𝙲𝚊𝚙𝚝𝚒𝚘𝚗', callback_data = "shw_caption"),
                    InlineKeyboardButton("𝙳𝚎𝚕𝚎𝚝𝚎 𝙲𝚊𝚙𝚝𝚒𝚘𝚗", callback_data = "d_caption")
                ],
                [
                    InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data = "ghelp"),
                    InlineKeyboardButton('🔒 𝙲𝙻𝙾𝚂𝙴', callback_data = "close")
                ]
            ]
        )
     )
    elif data == "cthumb":
        await query.message.edit_text(
            text=Translation.THUMBNAIL_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "closeme":
        await query.message.delete()
        try:
            await query.message.reply_text(
                text = "<b>Process Cancelled</b>"
     )
        except:
            pass 
    elif data == "ghelp":
        await query.message.edit_text(
            text=Translation.HELP_USER,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📝𝚁𝚎𝚗𝚊𝚖𝚎', callback_data = "rnme"),
                    InlineKeyboardButton('📂𝙵𝚒𝚕𝚎 𝚃𝚘 𝚅𝚒𝚍𝚎𝚘', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('🎞️𝙲𝚞𝚜𝚝𝚘𝚖 𝚃𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕', callback_data = "cthumb"),
                    InlineKeyboardButton('📑𝙲𝚞𝚜𝚝𝚘𝚖 Caption', callback_data = "ccaption")
                ],
                [
                    InlineKeyboardButton('💬𝙰𝚋𝚘𝚞𝚝', callback_data = "about")
                ]
            ]
        )
    )       

    elif data =="shw_caption":
             try:
                caption = await get_caption(query.from_user.id)
                c_text = caption.caption
             except:
                c_text = "Sorry but you haven't added any caption yet please set your caption through /scaption command" 
             await query.message.edit(
                  text=f"<b>Your Custom Caption:</b> \n\n{c_text} ",
                  parse_mode="html", 
                  disable_web_page_preview=True, 
                  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data = "ccaption"),
                    InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "about":
        await query.message.edit_text(
            text=Translation.ABOUT_ME,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "d_caption":
        try:
           await del_caption(query.from_user.id)   
        except:
            pass
        await query.message.edit_text(
            text="<b>caption deleted successfully</b>",
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data = "ccaption"),
                    InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
