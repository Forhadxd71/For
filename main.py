import io
from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterGif

api_id = 24232038
api_hash = '6b55079d2ba17ccc133881d67df066a9'
source_channels = ['unofficialmagi', '+fDZo8WCjA-FhNDMy', 'RedZoneDrop', 'nudobazz', 'publicnudity11']  # Add more source channels here
destination_channels = ['+c4uZQoRyVnQ3MWM9']  # Destination channels to forward media to
pic_down = './pic'
gif_down = './gif'
video_down = './video'
history_file = './history.txt'

def IsChongFu(content, file):
    xinxi = io.open(file, 'r', encoding='utf-8-sig')
    xinxi_list = xinxi.readlines()
    if content + '\n' in xinxi_list:
        print(content + ' is already done!')
        return True
    else:
        saveMessage(content, file)
        return False

def saveMessage(content, file):
    with open(file, 'a+', encoding='utf-8-sig') as fp:
        fp.write(content + "\n")

def download(client, file, filename):
    client.download_media(file, filename)

def forward_message(client, message, destinations):
    for destination in destinations:
        client.forward_messages(destination, message)

def getMediaList(client, channel, filter_type, download_path, file_extension):
    channel_link = 'https://t.me/' + channel
    messages = client.get_messages(channel_link, None, filter=filter_type)
    total = len(messages)
    index = 0
    for message in messages:
        filename = f"{download_path}/{channel}/{message.id}.{file_extension}"
        index += 1
        if IsChongFu(filename, history_file):
            continue
        print(f"downloading: {index}/{total} : {filename}")
        download(client, message, filename)
        forward_message(client, message, destination_channels)
    print(f'{filter_type.__name__.split("InputMessagesFilter")[1].lower()}s are done..')

def process_channel(client, channel):
    print(channel + ' is starting...')
    getMediaList(client, channel, InputMessagesFilterPhotos, pic_down, "jpg")
    getMediaList(client, channel, InputMessagesFilterGif, gif_down, "mp4")
    getMediaList(client, channel, InputMessagesFilterVideo, video_down, "mp4")

if __name__ == "__main__":
    client = TelegramClient('my_session', api_id=api_id, api_hash=api_hash).start()
    for channel in source_channels:
        process_channel(client, channel)
    client.disconnect()
    print('ALL done !!')
