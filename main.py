import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon import events

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
session_string = os.environ['TELETHON_SESSION']
admin_ids = [int(i.strip()) for i in os.environ['admins'].split(",")]
client = TelegramClient(StringSession(session_string), api_id, api_hash)

users_to_delete_messages = {}

@client.on(events.NewMessage(chats=events.ChatAction()))
async def delete_user_message(event):
    if event.sender_id in users_to_delete_messages:
        user_id = event.sender_id
        await event.delete()
        

@client.on(events.NewMessage(chats=events.ChatAction(), pattern='/mute'))
async def add_user_to_delete_list(event):
    if event.sender_id in admin_ids:
        if event.is_private and event.is_reply:
            replied_message = await event.get_reply_message()
            user_id = replied_message.sender_id
            users_to_delete_messages[user_id] = True
            await event.reply(f"User {user_id} has been muted in this chat.")

@client.on(events.NewMessage(chats=events.ChatAction(), pattern='/unmute'))
async def remove_user_from_delete_list(event):
    if event.sender_id in admin_ids:
        if event.is_private and event.is_reply:
            replied_message = await event.get_reply_message()
            user_id = replied_message.sender_id
            if user_id in users_to_delete_messages:
                del users_to_delete_messages[user_id]
                await event.reply(f"User {user_id} has been unmuted in this chat.")
            else:
                await event.reply("User is not in delete list.")

client.start()
client.run_until_disconnected()
