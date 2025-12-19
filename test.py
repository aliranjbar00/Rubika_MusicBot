from rubka import Robot

bot = Robot('BHEHA0HGFBWHAPODZJTFXJJGFTYOSDCGTQFVDQQHIMUBQZVGSKKBPOWYCACOCELS')
print(bot.set_commands(
    [
        {"command": "start", "description": "شروع ربات🤖"},
        {"command": "search", "description": "جستجوی آهنگ🔍"},
        {"command": "add", "description": "افزودن به گروه➕"}
    ]
))