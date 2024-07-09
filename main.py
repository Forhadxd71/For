import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto, InputMediaVideo
from aiogram.utils import executor
from telethon import TelegramClient
from telethon.sessions import StringSession

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

api_id = config['api_id']
api_hash = config['api_hash']
bot_token = config['bot_token']
collected_channels = config['collected_channels']
forwarded_channels = config['forwarded_channels']
string_session = config['string_session']

# Initialize the aiogram bot
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Initialize the Telethon client
if string_session:
    client = TelegramClient(StringSession(string_session), api_id, api_hash)
else:
    client = TelegramClient(StringSession(), api_id, api_hash)

async def forward_media(message: types.Message, forwarded_channels):
    media = []
    if message.photo:
        media = [InputMediaPhoto(media=message.photo[-1].file_id)]
    elif message.video:
        media = [InputMediaVideo(media=message.video.file_id)]
    else:
        return

    for channel in forwarded_channels:
        await bot.send_media_group(chat_id=channel, media=media)

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def handle_new_media(message: types.Message):
    chat_id = message.chat.id
    if str(chat_id) in collected_channels:
        await forward_media(message, forwarded_channels)

async def startup(dispatcher):
    # Start the Telethon client
    await client.start()

    if not string_session:
        # Save the session string to the config file
        session_string = client.session.save()
        config['string_session'] = session_string
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
        print("Session saved. You can now restart the script.")

    else:
        # Fetch recent messages from collected channels and forward if they are media
        for channel in collected_channels:
            async for message in client.iter_messages(channel, limit=100):
                if message.photo or message.video:
                    # Forward the media using aiogram bot
                    if message.photo:
                        photos = [types.PhotoSize(file_id=photo.id) for photo in message.photo.sizes]
                        wrapped_message = types.Message(
                            message_id=message.id,
                            from_user=types.User(id=message.sender_id),
                            date=message.date.timestamp(),
                            chat=types.Chat(id=message.chat_id),
                            content_type='photo',
                            photo=photos,
                            bot=dispatcher.bot
                        )
                    elif message.video:
                        video = types.Video(file_id=message.video.id)
                        wrapped_message = types.Message(
                            message_id=message.id,
                            from_user=types.User(id=message.sender_id),
                            date=message.date.timestamp(),
                            chat=types.Chat(id=message.chat_id),
                            content_type='video',
                            video=video,
                            bot=dispatcher.bot
                        )
                    await forward_media(wrapped_message, forwarded_channels)

        # Start polling
        executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup(dp))
