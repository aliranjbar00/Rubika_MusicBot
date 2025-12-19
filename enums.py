


class ChatKeyPads:
    join = {
        "rows": [
            {
                "buttons": [
                    {"id": "im_joinchannel", "type": "Simple", "button_text": "عضو شدم✅"}
                ]
            }
        ],
        "resize_keyboard": True,
        "on_time_keyboard": False,
    }

    main = {
        "rows": [
            {
                "buttons": [
                    {"id": "find_music", "type": "Simple", "button_text": "جستجوی موزیک🎵"}
                ]
            },
            {
                "buttons": [
                    {"id": "about", "type": "Simple", "button_text": " پشتیبانی🧑\u200d💻"},
                    {"id": "help", "type": "Simple", "button_text": "راهنما❓"},
                ]
            },
            {
                "buttons": [
                    {"id": "add_group", "type": "Simple", "button_text": "افزودن به گروه➕"}
                ]
            },
        ],
        "resize_keyboard": True,
        "on_time_keyboard": False,
    }


class InlineKeyPads:
    search_box = {
        "rows": [
            {
                "buttons": [
                    {
                        "id": "search_box",
                        "type": "Textbox",
                        "button_text": "نام آهنگ خود را وارد کنید 🎶: ",
                        "button_textbox": {
                            "type_line": "SingleLine",
                            "type_keypad": "String",
                            "title": "نام آهنگ خود را وارد کنید 🎶: ",
                        },
                    }
                ]
            }
        ]
    }
