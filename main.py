import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['TELETHON_SESSION']
admin_ids = [int(i.strip()) for i in os.environ['ADMINS'].split(",")]
client = TelegramClient(StringSession(session_string), api_id, api_hash)

muted_users = {}

@client.on(events.NewMessage(pattern='/mute'))
async def mute(event):
    user_id = event.sender_id
    if user_id in admin_ids:
        if event.is_reply:
            replied_msg = await event.get_reply_message()
            user_to_mute = replied_msg.sender_id
            muted_users[user_to_mute] = True
            await event.respond('User muted successfully!')
        else:
            await event.respond('Please reply to the user you want to mute.')

@client.on(events.NewMessage(pattern='/unmute'))
async def unmute(event):
    user_id = event.sender_id
    if user_id in admin_ids:
        if event.is_reply:
            replied_msg = await event.get_reply_message()
            user_to_unmute = replied_msg.sender_id
            if user_to_unmute in muted_users:
                del muted_users[user_to_unmute]
                await event.respond('User unmuted successfully!')
            else:
                await event.respond('User is not muted!')
        else:
            await event.respond('Please reply to the user you want to unmute.')

@client.on(events.NewMessage)
async def delete_muted_messages(event):
    user_id = event.sender_id
    if user_id in muted_users:
        await event.delete()

client.start()
client.run_until_disconnected()
