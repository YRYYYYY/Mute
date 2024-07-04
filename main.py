import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['TELETHON_SESSION']
admin_ids = [int(i.strip()) for i in os.environ['ADMINS'].split(",")]
#admin_ids = [1008961594,1008981594]
client = TelegramClient(StringSession(session_string), api_id, api_hash)

muted_users = {}


@client.on(events.NewMessage(pattern='/mute'))
async def mute(event):
    user_id = event.sender_id
    if user_id == 1008961594:
    muted_users[user_id] = True
    await event.respond('User muted successfully!')


@client.on(events.NewMessage(pattern='/unmute'))
async def unmute(event):
    user_id = event.sender_id
    if user_id == 1008961594:
    if user_id in muted_users:
        del muted_users[user_id]
        await event.respond('User unmuted successfully!')
    else:
        await event.respond('User is not muted!')

uted users
@client.on(events.NewMessage)
async def delete_muted_messages(event):
    user_id = event.sender_id
    if user_id in muted_users:
        await event.delete()




client.start()
client.run_until_disconnected()
