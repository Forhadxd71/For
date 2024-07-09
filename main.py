import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto, InputMediaVideo
from aiogram.utils import executor
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

api_id = config['api_id']
api_hash = config['api_hash']
bot_token = config['bot_token']
collected_channels = config['collected_channels']
forwarded_channels = config['forwarded_channels']

# Initialize the aiogram bot
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Initialize the Telethon client
client = TelegramClient(StringSession(), api_id, api_hash)

async def forward_media(message: types.Message, forwarded_channels):
    if message.photo:
        media = InputMediaPhoto(media=message.photo[-1].file_id)
    elif message.video:
        media = InputMediaVideo(media=message.video.file_id)
    else:
        return

    for channel in forwarded_channels:
        await bot.send_media_group(chat_id=channel, media=[media])

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def handle_new_media(message: types.Message):
    chat_id = message.chat.id
    if chat_id in collected_channels:
        await forward_media(message, forwarded_channels)

async def main():
    # Start the Telethon client
    await client.start()

    # Fetch recent messages from collected channels and forward if they are media
    for channel in collected_channels:
        async for message in client.iter_messages(channel, limit=100):
            if message.photo or message.video:
                await forward_media(message, forwarded_channels)

    # Start polling
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    from aiogram import executor
    executor.start(dp, on_startup=main)
