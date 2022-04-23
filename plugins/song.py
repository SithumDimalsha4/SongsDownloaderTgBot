import os
import time
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@Client.on_message(filters.command(['start']))
async def start(client, message):
       await message.reply("Hello There👋 I'm Music Download Bot 

I can Download Songs with Useful Features❤️ Do you Want To know More about Me hit the @Soshielogs",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('🙋‍♀News channel ', url='https://t.me/darklabu,)
                    InlineKeyboardButton('🔍Search inline', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['help']))
async def help(client, message):
       await message.reply("<b>Hit help button to find more about how to use me.. Send  - /help </i>\n\n<b>Eg</b> `/song Faded`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('🙋Developer', url='https://t.me/Sithumj')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['about']))
async def about(client, message):
       await message.reply("➪<b>Name</b> : ✫<i>Song Downloader</i>\n➪<b>Developer</b> : ✫[Sithum Dimalsha](https://t.me/Sithumj)\n➪<b>Language</b> : ✫<i>Python3</i>\n➪<b>Server</b> : ✫[𝘏𝘦𝘳𝘰𝘬𝘶](https://heroku.com/)\n➪<b>Source Code</b> : ✫[𝘊𝘭𝘪𝘤𝘬 𝘏𝘦𝘳𝘦](https://github.com/PereraSehath)",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.text)
def a(client, message):
    query=message.text
    print(query)
    m = message.reply('🔍 Searching your Song.')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"MusicDownloadv2bot" 
            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Sorry Not found your Song!!!')
            return
    except Exception as e:
        m.edit(
            "❎ 𝐹𝑜𝑢𝑛𝑑 𝑁𝑜𝑡ℎ𝑖𝑛𝑔.\n\nEg.`Faded`"
        )
        print(str(e))
        return
    m.edit("`Uplodeing your Song...`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'🎧 𝗧𝗶𝘁𝘁𝗹𝗲 : [{title[:35]}]({link})\n⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 : `{duration}`\n👀 𝐕𝐢𝐞𝐰𝐬 : `{views}`\n\n📮 𝗕𝘆: {message.from_user.mention()}\n📤 𝗕𝘆 : @Soshiemanagebot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('𝐅𝐚𝐢𝐥𝐞𝐝\n\n`𝐏𝐥𝐞𝐚𝐬𝐞 𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧 𝐋𝐚𝐭𝐞𝐫...`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
