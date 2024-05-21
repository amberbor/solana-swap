from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 25926132
api_hash = '784d85f68b93c3697824bacb37a7303b'

# Your session name
session_name = 'testime'

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await client.start()

    # Get the session string
    session_string = StringSession.save(client.session)
    print("Session String:", session_string)

    print("Client connected successfully!")
    me = await client.get_me()
    print("My account:", me)

# Run the main function
with client:
    client.loop.run_until_complete(main())
