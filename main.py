import io
from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterGif

api_id = 9307366
api_hash = '1ce7a3a4670658d10a01b7e6b090fc07'
source_channels = ['+Jy6JUPHajxoyMjg8']  # Source channels to collect media from
destination_channels = ['gsjjsbsbsb']  # Destination channels to forward media to
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

def getPhotoList(client, channel):
    channel_link = 'https://t.me/' + channel
    photos = client.get_messages(channel_link, None, filter=InputMessagesFilterPhotos)
    total = len(photos)
    index = 0
    for photo in photos:
        filename = pic_down + "/" + channel + "/" + str(photo.id) + ".jpg"
        index += 1
        if IsChongFu(filename, history_file):
            continue
        print("downloading: ", index, "/", total, " : ", filename)
        download(client, photo, filename)
        forward_message(client, photo, destination_channels)
    print('photos are done..')

def getGifList(client, channel):
    channel_link = 'https://t.me/' + channel
    gifs = client.get_messages(channel_link, None, filter=InputMessagesFilterGif)
    total = len(gifs)
    index = 0
    for gif in gifs:
        filename = gif_down + "/" + channel + "/" + str(gif.id) + ".mp4"
        index += 1
        if IsChongFu(filename, history_file):
            continue
        print("downloading: ", index, "/", total, " : ", filename)
        download(client, gif, filename)
        forward_message(client, gif, destination_channels)
    print('gifs are done..')

def getVideoList(client, channel):
    channel_link = 'https://t.me/' + channel
    videos = client.get_messages(channel_link, None, filter=InputMessagesFilterVideo)
    total = len(videos)
    index = 0
    for video in videos:
        filename = video_down + "/" + channel + "/" + str(video.id) + ".mp4"
        index += 1
        if IsChongFu(filename, history_file):
            continue
        print("downloading: ", index, "/", total, " : ", filename)
        download(client, video, filename)
        forward_message(client, video, destination_channels)
    print('videos are done..')

if __name__ == "__main__":
    client = TelegramClient('my_session', api_id=api_id, api_hash=api_hash).start()
    for channel in source_channels:
        print(channel + ' is starting...')
        getPhotoList(client, channel)
        getGifList(client, channel)
        getVideoList(client, channel)
    client.disconnect()
    print('ALL done !!')
