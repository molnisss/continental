from aiogram import executor

import modules
import time
from loader import vip
from colorama import Fore, Style


start = Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Бот успешно запущен!" + Fore.RESET + Style.NORMAL + '\n'

if __name__ == '__main__':
    time.sleep(0.03)
    print(start, end='', flush=True)
    executor.start_polling(vip)
