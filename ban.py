import logging
import re
import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsBanned
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime
from var import Var
from telethon.errors.rpcerrorlist import FloodWaitError

logging.basicConfig(level=logging.INFO)

print("Starting.....")

Riz = TelegramClient('Riz', Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)

SUDO_USERS = []
for x in Var.SUDO: 
    SUDO_USERS.append(x)

@Riz.on(events.NewMessage(pattern="^/start"))  
async def start(e):
    if e.sender_id in SUDO_USERS:
        await message.reply_photo(
                            photo = f"https://telegra.ph/file/fff2ee6f504bc061cb7d3.jpg",
                            caption = f"ʜᴇʏ, ᴛʜɪs ɪs ᴀ sɪᴍᴘʟᴇ ʙᴀɴ ᴀʟʟ ʙᴏᴛ ᴡʜɪᴄʜ ɪs ʙᴀsᴇᴅ ᴏɴ ᴘʏʀᴏɢʀᴀᴍ ʟɪʙᴇʀᴀʀʏ ᴛᴏ ʙᴀɴ ᴏʀ ᴅᴇsᴛʀᴏʏ ᴀʟʟ ᴛʜᴇ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ɪɴ ᴀ ғᴇᴡ  sᴇᴄᴏɴᴅs!\n\nᴛᴏ ᴄʜᴇᴄᴋ ᴍʏ ᴀʙɪʟɪᴛʏ ɢɪʙ me ғᴜʟʟ ᴘᴏᴡᴇʀs\n\nᴛʏᴘᴇ /ʙᴀɴᴀʟʟ ᴛᴏ ꜱᴇᴇ ᴍᴀɢɪᴄ ɪɴ ɢʀᴏᴜᴘ.",
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER}")
                ]       
           ]
      )
)

@Riz.on(events.NewMessage(pattern="^/ping"))  
async def ping(e):
    if e.sender_id in SUDO_USERS:
        start = datetime.now()
        text = "Pong!"
        event = await e.reply(text, parse_mode=None, link_preview=None )
        end = datetime.now()
        ms = (end-start).microseconds / 1000
        await event.edit(f"**I'm On** \n\n __Pong__ !! `{ms}` ms")

@Riz.on(events.NewMessage(pattern="^/cbanall"))
async def cbanall(event):
   if event.sender_id in SUDO_USERS:
     if not event.is_channel:
         Reply = f"Noob !! Use This Cmd in Channel."
         await event.reply(Reply)
     else:
         await event.delete()
         RiZ = await event.get_chat()
         admin = RiZ.admin_rights
         creator = RiZ.creator
         if not admin and not creator:
              return await event.reply("I Don't have sufficient Rights !!")
         RiZoeL = await Riz.send_message(event.chat_id, "**Banning all users...**")
         all = 0
         banned = 0
         async for user in event.client.iter_participants(event.chat_id):
             all += 1
             try:
                await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None)))
                banned += 1
                await asyncio.sleep(0.1)
             except Exception as e:
                print(str(e))
                await asyncio.sleep(0.1)
         await RiZoeL.edit(f"**Users Banned Successfully ! \n\n Banned Users:** `{banned}` \n **Total Users:** `{all}`")

@Riz.on(events.NewMessage(pattern="^/unbanall"))
async def unbanall(event):
   if event.sender_id in SUDO_USERS:
     if not event.is_channel:
         Reply = f"Noob !! Use This Cmd in Channel."
         await event.reply(Reply)
     else:
         await event.delete()
         RiZ = await event.get_chat()
         admin = RiZ.admin_rights
         creator = RiZ.creator
         if not admin and not creator:
              return await event.reply("I Don't have sufficient Rights !!")
         RiZoeL = await Riz.send_message(event.chat_id, "**Unbanning all users...**")
         all = 0
         unbanned = 0
         async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsBanned):
             all += 1
             try:
                await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=0)))
                unbanned += 1
                await asyncio.sleep(0.1)
             except Exception as e:
                print(str(e))
                await asyncio.sleep(0.1)
         await RiZoeL.edit(f"**Users Unbanned Successfully ! \n\n Unbanned Users:** `{unbanned}` \n **Total Users:** `{all}`")

@Riz.on(events.NewMessage(pattern="^/leave"))
async def leave(e):
    if e.sender_id in SUDO_USERS:
        rizoel = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        if len(e.text) > 7:
            bc = rizoel[0]
            bc = int(bc)
            text = "Leaving....."
            event = await e.reply(text, parse_mode=None, link_preview=None )
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("Succesfully Left")
            except Exception as e:
                await event.edit(str(e))   
        else:
            bc = e.chat_id
            text = "Leaving....."
            event = await e.reply(text, parse_mode=None, link_preview=None )
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("Succesfully Left")
            except Exception as e:
                await event.edit(str(e))   

@Riz.on(events.NewMessage(pattern="^/restart"))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        text = "__Restarting__ !!!"
        await e.reply(text, parse_mode=None, link_preview=None )
        try:
            await Riz.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()

print("\n\n")
print("Your Ban All Bot Deployed Successfully ✅")

Riz.run_until_disconnected()
                 
