from loader import bot
from data import User


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Referral(Singleton):
    def __init__(self, referrer_id: str, user_id: str):
        self.referrer_id = referrer_id
        self.user_id = user_id
        self.referrer = User(self.referrer_id)

    async def add(self):
        ref = User(self.referrer_id)
        ref.add_referral()

        await bot.send_message(
        chat_id=self.referrer_id,
        text=f"<b>✅ Новый реферал: </b> @{self.user_id}", parse_mode='html')

    async def invites_successfull(self):
        if self.referrer.get_refs_amount() == 5:
                await bot.send_message(
                    chat_id=self.referrer_id,
                    text='<b>🥳Поздравляю, вы набрали нужное количество рефералов\n✅ Бот отправит вам Gift как только придет ваша очередь!</b>'
                )