import asyncio
import zipfile
from pathlib import Path
from shutil import rmtree
from opentele.tl import TelegramClient
from opentele.api import UseCurrentSession


class Converter:

    def __init__(self, number) -> None:
        self.number = number
        self.tdata_path = f'../data/tdata/{number}'
        self.session_path = f'../data/session/{number}'

    async def _convert(self):
        try:
            client = TelegramClient(f'{self.session_path}.session')
            await client.connect()

            if not await client.is_user_authorized():
                raise Exception("Клієнт не авторизований")

            tdesk = await client.ToTDesktop(flag=UseCurrentSession)
            tdesk.SaveTData(f'{self.tdata_path}')
            print(f'tdata saved to {self.tdata_path}')
        except Exception as e:
            print(f"Error during conversion: {e}")
        finally:
            await client.disconnect()

    def _zip(self):

        dir = Path(self.tdata_path)

        with zipfile.ZipFile(f'{self.tdata_path}.zip', "w", zipfile.ZIP_DEFLATED) as zip_file:
            for entry in dir.rglob("*"):
                zip_file.write(entry, entry.relative_to(dir))
        
        print('tdata ziped')


    async def run(self):
        await self._convert() 
        self._zip()
        rmtree(self.tdata_path)
        print('data folder deleted')