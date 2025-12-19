from ddgs import DDGS
from httpx import get
from bs4 import BeautifulSoup
from time import sleep , time
from random import randint

from rubka import Robot
from rubka.context import Message
# import rubpy

# from urllib.parse import quote

from rubka.keypad import ChatKeypadBuilder , InlineBuilder



class Keys:
    im_joined = (
        ChatKeypadBuilder().row(
            ChatKeypadBuilder().button('im_joined','عضو شدم')
        ).build()
    )
    main = (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button('find_music','جستجوی اهنگ🔍')
        )
        .row(
            ChatKeypadBuilder().button('history','🕘 (غیر فعال)آخرین جستجوها'),
            ChatKeypadBuilder().button('support','🧑‍💼 تماس با ادمین / گزارش مشکل')
        ).build()

    )

    input_musicname = (
        InlineBuilder().row(
            InlineBuilder().button_textbox(
                'input_musicname',
                'نام اهنگ خود را وارد کنید: ',
                'SingleLine',
                'String'
            )
        ).build()
    )
    
bot = Robot(
    'BHEHA0HGFBWHAPODZJTFXJJGFTYOSDCGTQFVDQQHIMUBQZVGSKKBPOWYCACOCELS',
    web_hook = 'https://bots.aliranjbarapi.ir/music/get_message.php?key=your-secret-api-key'
)
ddgs = DDGS()
def find_music(prompt) ->  str:
    results = ddgs.text(f'دانلود اهنگ {prompt}', max_results=10)
    for r in results:
        page_url = r['href']
        try:
            response = get(page_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            for a in soup.find_all('a', href=True):
                if a['href'].endswith('.mp3') and isinstance(a['href'], str):
                    return a['href']
                
            else:
                sleep(0.5)
                return find_music(prompt)
            
        except Exception:
            sleep(0.5)
            return find_music(prompt)

def download_files(download_link) -> str:
    """ return file_name """
    file_name = f'{randint(1_000_000 , 10_000_000)}.mp3'
    try:
        file_bytes = get(download_link)
        file_bytes = file_bytes.read() if file_bytes.status_code == 200 else False
        if isinstance(file_bytes, bool):
            sleep(0.5)
            return download_files(download_link)

    except Exception:
        return download_files(download_link)
        # print(e)

    with open(file_name, 'wb') as file:
        if isinstance(file_bytes, bytes):
            file.write(file_bytes)
        
    return file_name

def make_channels():
    data_ = {
        1:'@linkdony_rubikas',
        2:'@gol_frOoshe',
        3:'@VazirBots'
    }
    data = []
    for i , link in data_.items():
        text = f'کانال شماره {i} : {link}'
        data.append(text)

    return '\n'.join(data)
people = {}




def run_bot(bot:Robot, message:Message):
    global people
    message,sourse_data = message,message.raw_data

    send_time = sourse_data.get('time')
    if isinstance(send_time,str):
        send_time = int(send_time)

    button_id = sourse_data.get('aux_data')

    if isinstance(button_id,dict):
        button_id = button_id.get('button_id')
    
    type_ = message.sender_type.lower()
    
    chat_id = message.chat_id

    if not isinstance(send_time, int) or (int(time()) - send_time) < 10 and type_ == 'user':
        if not chat_id in people:
            people[chat_id] = {}

        if message.text == '/start':
            first_time = time()
            people[chat_id]['time'] = first_time

            links = make_channels()
            message.reply_keypad(
                f'سلام خوش اومدی \n برای استفاده از ربات توی لینک های زیر عضو شو \n {links}',
                Keys.im_joined
            )
            # welcome message and take time()
            # pass

        elif button_id == 'im_joined':
            if int(time() - people[chat_id]['time']) >= 10:
                message.reply_keypad(
                    'عضویتت تایید شد حالا میتونی از ربات استفاده کنی❤️',
                    Keys.main
                )
                
                return
            
            message.reply('هنوز عضو نشدی که😡')

            # check is join  and send menu
            # pass
        elif button_id == 'find_music':
            message.reply_inline(
                'روی دکمه زیر بزن و اسم اهنگتو بفرست:🎵',
                Keys.input_musicname
            )

        elif button_id == 'input_musicname':
            text_ = message.text.strip()
            bot.send_message(chat_id, f' پیامت که حاوی : {text_} بود رو دریافت کردم✅')
            down_link = find_music(text_)
            down_link = down_link.replace(' ', '%20')
            bot.send_message(chat_id, f'لینک دانلود مستقیم اهنگ: {down_link} \n\n توجه‼️ : به دلیل محدودیت های روبیکا فعلا قادر به ارسال موزیک در خود روبیکا نیستیم با تشکر')
            # message_id = result.get('message_id')
            # down_link = find_music(text_)
            # file_name = download_files(down_link)
    # bot.send_document(
    #             chat_id,
    #             '7091810.mp3'
    #         )

def main():
    @bot.on_message()
    def update_message(bot:Robot, message:Message):
        return run_bot(
            bot,
            message
        )

    bot.run()

while True:
    try:
        main()
    
    except Exception:
        sleep(10)
        continue

        

# link = find_music('الو از تتلو ')
# download_files(link)


