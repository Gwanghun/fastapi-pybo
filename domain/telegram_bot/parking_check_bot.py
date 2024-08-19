import telegram
from starlette.config import Config

config = Config(".env")
# bot.sendMessage(chat_id='@hooeni', text='테스트 메시지입니다.')

class parking_check_bot:
    def __init__(self):
        self.token = config('TELEGRAM_BOT_TOKEN')
        self.bot = telegram.Bot(self.token)
        self.check_id = "201221481"

    async def get_check_id(self):
        await self.bot.sendMessage(chat_id=self.check_id, text='테스트 메시지입니다.')
        # print(self.token)
        # updates = self.bot.getUpdates()
        # print(updates)
        # print(updates[0].message.chat_id)
