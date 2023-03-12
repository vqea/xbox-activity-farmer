import asyncio
import os
import ctypes
from sys import platform
from getpass import getpass
from colorama import init
from source import collect_profile_info, crawler
from tools import remove_dupes, filter, database_manager


class Activity_Farmer:
    def __init__(self) -> None:
        init(autoreset=True)
        self.profile_info = collect_profile_info.Profile_Information()
        self.crawler = crawler.Activity_Crawler()
        self.cleaner = remove_dupes.Remove_Dupes()
        self.filter = filter.Filter_Targets()
        self.manager = database_manager.Database_Manager()
        self.xuid = ''
        self.token = ''
        self.total = 0
        self.unfiltered_xuid_database = []
        self.xuid_database = []


    async def initialise(self):
        await self.collect_token()
        if platform == 'win32':
            ctypes.windll.kernel32.SetConsoleTitleW('collecting profile information..')
        self.xuid = await self.profile_info.retrieve_information(self.token)
        await self.verify_xuid_database()
        await asyncio.shield(self.begin_crawler())
        print('\n\n \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] reached end of database, cleaning scrape results..')
        await self.cleaner.clean()
        print('\n\n \x1b[1;37m[\x1b[1;36m+\x1b[1;37m] database completed!')
        await self.manager.clear_file()


    async def begin_crawler(self):
        for xuid in self.xuid_database:
            await asyncio.shield(self.crawler.get_recent_post(self.token, xuid, self.xuid))
            self.total += 1
            if platform == 'win32':
                ctypes.windll.kernel32.SetConsoleTitleW(f"activity crawler  |  XUID's loaded: ({len(self.xuid_database)})  |  completed: ({self.total}/{len(self.xuid_database)})  |  scrape results: ({len(open('database/scraping/scraped_database.txt', 'r').readlines())})")
            await self.manage_database(xuid)
            await asyncio.sleep(2)


    async def manage_database(self, xuid):
        await self.manager.write_recents(xuid)
        await self.manager.clean_loaded_database(xuid)
    

    async def collect_token(self):
        self.token = getpass(' \x1b[1;37m[\x1b[1;36m+\x1b[1;37m] authorization token: ')


    @staticmethod
    def collect_target_list():
        with open('database/xuid_database/xuid_list.txt', 'r') as xuid_list:
            return [xuid.strip() for xuid in xuid_list]
    

    async def verify_xuid_database(self):
        for xuid in self.collect_target_list():
            if xuid.isnumeric() and len(xuid) == 16:
                self.unfiltered_xuid_database.append(xuid)
        self.xuid_database = await self.filter.filter_database(self.unfiltered_xuid_database)
        await self.manager.clear_file()
        await self.manager.write_clean_list(self.xuid_database)



if __name__ == "__main__":
    os.system('cls' if platform == 'win32' else 'clear')
    if platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW('welcome to activity crawler')
    farmer = Activity_Farmer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.shield(farmer.initialise()))
