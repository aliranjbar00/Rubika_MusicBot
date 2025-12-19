from rubka.asynco import Robot, filters
from rubka.context import Message, InlineMessage


from rubka.exceptions import APIRequestError

from asyncio import run, sleep as asleep
# from enum import Enum

from typing import Union

import base 
group_handler = base.Group
user_handler = base.User

import enums
ChatKeyPads = enums.ChatKeyPads
InlineKeyPads = enums.InlineKeyPads


from time import sleep


bot = Robot(
    'BIBDF0FNJNOTHTMZGYKKVHWIBXYQXUSFEFBPPRHWRTJAOXOTBUZIAKSZDFNATQHY',
    web_hook='https://bots.aliranjbarapi.ir/tnw/webhook.php',
)

# print('1')

def log_execution(func):
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        
        except KeyError as e:
            print(f"KeyError in {func.__name__}: {e}")
            pass  # Handle KeyError specifically if needed
            
        except APIRequestError as e:
            print(f"APIRequestError in {func.__name__}: {e}")
            await asleep(5)
            return await log_execution(func)(*args, **kwargs)

        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            await asleep(5)
            return await log_execution(func)(*args, **kwargs)
        
    return wrapper

# @log_execution
async def main():
    # print('2')
    @bot.on_message_group()
    @log_execution
    async def update(bot:Robot, message:Message):
        text = message.text
        chat_id = message.chat_id
        
        if text is None or chat_id is None:
            return

        group = group_handler(bot, message)
        if text == '/add':
            if not group.is_group:
                await group.add_group(chat_id)

            else:
                await message.reply('گروه شما قبلا ثبت شده است ✅')
        
        return await group.handler_group(text)

    # print('3')
        
    @bot.on_message_private()
    @log_execution
    async def update(bot:Robot, message:Message):
        user = user_handler(bot, message)

        chat_id = message.chat_id
        text = message.text

        # button_id = None
        # if message.aux_data:
        #     button_id = message.aux_data.button_id

        if text is None or chat_id is None:
            return
        
        if not user.is_user:
            user.database.insert_or_ignore(chat_id, 'users')
        
        return await user.handler_user(message)

    
    @bot.on_inline_query()
    @log_execution
    async def update(bot:Robot, message:InlineMessage):
        user = user_handler(bot, message)
        chat_id = message.chat_id
        text = message.text

        if text is None or chat_id is None:
            return
        
        return await user.handler_user(message)
    
    await bot.run()
    


while True:
    try:
        run(main())
        
    except Exception as e:
        print(e)
        sleep(10)
        continue
