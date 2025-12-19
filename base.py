from rubka.asynco import Robot
from rubka.context import Message, InlineMessage

from typing import Union
import database

from aiohttp import ClientSession
from aiofiles import open as aioopen


import enums

from time import time

from enum import Enum

from ddgs import DDGS, exceptions as ddgsexceptions
from requests import get, exceptions

from random import randint


from typing import Literal, Union, Any
from bs4 import BeautifulSoup
import os

class Messages(str, Enum):
    join_channel = (
        "سلام دوست عزیز! 🌟\n"
        "برای استفاده از ربات، لطفاً ابتدا در کانال‌های زیر عضو شوید:\n"
        "1. کانال اول: @linkdony_rubikas\n"
        "2. کانال دوم: @VazirBots\n\n"
        "پس از عضویت، لطفاً روی دکمه 'عضو شدم✅' کلیک کنید تا بتوانید از ربات استفاده کنید. 🎵\n"
    )

    help_fa = (
        "🎶 به موزیک‌فایندر خوش اومدی! 🎶\n"
        "اگه دنبال آهنگ هستی، من اینجام که کمکت کنم! 😍\n"
        "دستورات من:\n"
        "/add - اضافه کردن گروه! 🆕\n"
        "/search <عبارت> - جستجوی آهنگ مورد علاقه‌ات! 🔍\n"
        "اگه کمک بیشتری خواستی، فقط بگو! 💬"
    )
    add_group = (
        "🤖 برای اد کردن ربات مراحل زیر را پیش ببرید:\n\n"
        "1️⃣ آیدی ربات را بدون @ کپی و در گروهتون اد کنید\n"
        "2️⃣ ربات را برای دریافت پیام ادمین کامل کنید\n"
        "3️⃣ حدود ۱ دقیقه صبر کنید و سپس دستور /add را در گروه ارسال کنید\n"
        "✅ حالا ربات آماده استفاده است!"
    )


class dataHandler:
    DOWNLOAD_ERORR = 'خطا در دانلود'
    MESSAGE_ERORR = 'لطفا اسم آهنگ را بعد از دستور سرچ وارد کنید 🎵\n\nمثال: /search الو از تتلو'


    def __init__(self, bot:Robot, message:Union[Message, InlineMessage]):
        self.bot = bot
        self.message = message

        self.chat_id = message.chat_id
        self.message_id = message.message_id

        self.CHAT_KEYPAD = enums.ChatKeyPads
        self.INLINE_KEYPAD = enums.InlineKeyPads

        self.ddgs = DDGS()
        self.search_type = 'music'
        self.__end = '.mp3'

    
    async def search(self, prompt:str) -> Union[list[dict[str, Any]], str]:
        # SEARCH IN WEB
        try:
            results:list = self.ddgs.text(
                query=prompt,
                max_results=10
            )
        
        except ddgsexceptions.TimeoutException:
            return 'Timeout Erorr, check internet or proxy'

        
        # ADD DOWNLOAD LINK
        for i in range(10):
            page_url = results[i]['href']
            try:
                response = get(page_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    # To avoid errors
                    href = a.get('href', 'Not_found')
                    if href.endswith(self.__end):
                        results[i]['download_url'] = href
                        break
            
            except exceptions.ConnectionError:
                continue

            except exceptions.InvalidURL:
                continue
                
            except Exception:
                # print(e)
                continue
                
        return results

    
    async def download(self, down_link:str, name:str) -> Union[int, str]:
        async with ClientSession() as session:
            async with session.get(down_link) as response:
                try:
                    result = await response.read() if response.status == 200 else False
                    if isinstance(result, bytes):
                        async with aioopen(f'{name}.mp3', 'wb') as file:
                            try:
                                return await file.write(result)
                            except Exception:
                                return self.DOWNLOAD_ERORR
                    return self.DOWNLOAD_ERORR
                except Exception:
                    return self.DOWNLOAD_ERORR
    
    async def find_music(self, prompt:str) -> Union[bool, str]:
        name = f'{randint(1_000_000 , 10_000_000)}'
        try:
            results = await self.search(prompt)
            # print(results)
            if isinstance(results, list):
                for i in range(len(results)):
                    try:
                        download_link = results[i].get('download_url', False)
                        if not isinstance(download_link, str):
                            continue

                        # print(download_link)
                        result = await self.download(download_link,name)
                        if isinstance(result, int):
                            return True, name

                        else:
                            await self.message.reply('نتونستم دانلود کنم - تلاش مجدد⌛')
                            continue
                    
                    except Exception:
                        continue
                    
            return False, name

        except Exception:
            # print(e)
            return self.DOWNLOAD_ERORR , name
        
    async def send_music(self, prompt:str):
        result, name = await self.find_music(prompt)
        if isinstance(result, str):
            return await self.message.reply(result)
        
        elif isinstance(result, bool):
            if result == True:
                await self.message.reply('در حال ارسال موزیک ... ⏳')
                await self.bot.send_music(
                    self.chat_id,
                    f'{name}.mp3',
                    text='موزیک درخواستی شما👆❤️',
                    reply_to_message_id=self.message_id
                )
                try:
                    await self.remove(name)

                except Exception:
                    pass
                return 

            return await self.message.reply(self.DOWNLOAD_ERORR)
    
    async def remove(self, name):
        return os.remove(f'{name}.mp3')

    

class Group(dataHandler):
    def __init__(self, bot:Robot, message:Union[Message, InlineMessage]):
        self.bot = bot
        self.message = message

        self.chat_id = message.chat_id
        self.message_id = message.message_id

        self.database = database.Database()
        super().__init__(bot, message)
    
    @property
    def is_group(self) -> bool:
        data = self.database.is_in_table(self.chat_id, 'groups')
        return True if data else False

    async def add_group(self, chat_id:str):
        self.database.insert_or_ignore(chat_id, 'groups')
        await self.message.reply('ربات با موفقیت فعال شد ✅')
    
    async def handler_group(self, text:str):
        if text in ['/help', 'راهنما', 'کمک']:
           await self.message.reply(Messages.help_fa.value)

        elif text.startswith('/search'):
            text = text.replace('/search', '').strip()
            if text:
                await self.message.reply('در حال جستجو ... ⏳')
                await self.send_music(text)
                
            else:
                await self.message.reply(self.MESSAGE_ERORR)
        


people = {}
class User(dataHandler):
    def __init__(self, bot:Robot, message:Union[Message, InlineMessage]):
        self.bot = bot
        self.message = message

        self.chat_id = message.chat_id
        self.message_id = message.message_id

        self.database = database.Database()
        super().__init__(bot, message)
    
    @property
    def is_user(self) -> bool:
        data = self.database.is_in_table(self.chat_id, 'users')
        return True if data else False
    
    async def add_user(self, chat_id:str):
        return self.database.insert_or_ignore(chat_id, 'users')

    async def handler_user(self, message:Union[Message, InlineMessage]):
        
        if isinstance(message, Message):
            button_id = None
            if message.aux_data:
                button_id = message.aux_data.button_id

            if not message.chat_id in people:
                people[message.chat_id] = {}
            
            text = message.text
            if text is None:
                return

            if button_id == 'start' or text == '/start':
                people[message.chat_id] = {'time': time()}
                await self.bot.send_message(
                    message.chat_id,
                    Messages.join_channel.value,
                    chat_keypad=self.CHAT_KEYPAD.join,
                    chat_keypad_type='New'
                )
            
            elif button_id == 'im_joinchannel':
                start_time = people[message.chat_id].get('time')
                if start_time and (int(time()) - start_time) >= 10:
                    await self.bot.send_message(
                        message.chat_id,
                        'عضویتت تایید شد حالا میتونی از ربات استفاده کنی❤️',
                        chat_keypad=enums.ChatKeyPads.main,
                        chat_keypad_type='New'
                    )
                else:
                    await message.reply('هنوز عضو نشدی که😡')
            
            elif button_id == 'find_music':
                await self.bot.send_message(
                    message.chat_id,
                    'روی دکمه زیر بزن و اسم اهنگتو بفرست:🎵',
                    inline_keypad=self.INLINE_KEYPAD.search_box
                )

            elif button_id == 'help':
                await message.reply(Messages.help_fa.value)

            elif button_id == 'about':
                await message.reply('برای پشتیبانی با @VazirRanjbar در ارتباط باشید ❤️')

            elif button_id == 'add_group':
                await message.reply(Messages.add_group.value)

            elif text.startswith('/search'):
                text = text.replace('/search', '').strip()
                if text:
                    await self.message.reply('در حال جستجو ... ⏳')
                    await self.send_music(text)
                    
                else:
                    await self.message.reply(self.MESSAGE_ERORR)


        elif isinstance(message, InlineMessage):
            # print('hi')
            button_id = None
            if message.aux_data:
                button_id = message.aux_data.button_id
            
            text = message.text
            if text is None:
                return

            
            
            if button_id == 'search_box':
                text = text.strip()
                if text:
                    await self.message.reply('در حال جستجو ... ⏳')
                    await self.send_music(text)
                    
                else:
                    await self.message.reply(self.MESSAGE_ERORR)