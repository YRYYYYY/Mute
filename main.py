import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession


api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
session_string = os.environ['TELETHON_SESSION']
admin_ids = [int(i.strip()) for i in os.environ['admins'].split(",")]
client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(pattern='/mute'))
async def mute_user(event):
    
    if event.sender_id in admin_ids:
        if event.is_group and event.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            user_id_to_mute = replied_message.sender_id
            
            await event.reply(f"User {user_id_to_mute} has been muted in this chat.")

@client.on(events.NewMessage(pattern='/unmute'))
async def unmute_user(event):
    
    if event.sender_id in admin_ids:
        if event.is_group and event.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            user_id_to_unmute = replied_message.sender_id
           
            await event.reply(f"User {user_id_to_mute} has been unmuted in this chat.")


client.start()
client.run_until_disconnected()
