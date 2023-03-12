import aiohttp
import asyncio
import random
import colorama
import ctypes
import os
import sys
import hashlib


class Friend_Scraper:
    def __init__(self):
        colorama.init(autoreset=True)
        self.targets = self.get_targets()
        self.total_completed = 0
        self.rate_limits = 0


    async def scrape_friends(self, xuid):
        headers = {
            'Authorization': await self.choose_token(),
            'X-XBL-Contract-Version': '2'
        }

        session = aiohttp.ClientSession()

        async with session.get(f'https://social.xboxlive.com/users/xuid({xuid})/people', headers=headers) as scrape_friends_request:
            if scrape_friends_request.status in [200, 201, 202, 204]:
                response_data = await scrape_friends_request.json()

                await self.write_data(response_data['people'])
            elif scrape_friends_request.status == 429:
                self.rate_limits += 1
                pass
            else:
                pass

        await session.close()


    async def initiate(self):
        for xuid in self.targets:
            await self.scrape_friends(xuid)
            self.total_completed += 1
            print(f' \x1b[1;37m[\x1b[1;35m+\x1b[1;37m] scraping friends  |  (\x1b[1;35m{self.total_completed}\x1b[1;37m/\x1b[1;35m{len(self.targets)}\x1b[1;37m)', end='\r', flush=True)
            ctypes.windll.kernel32.SetConsoleTitleW(f"friends list scraper  |  scrape results: ({len(open('xuids.txt', 'r').readlines())})  |  rate limits: ({self.rate_limits})")
        await self.remove_dupes()


    @staticmethod
    def get_targets():
        with open('list_to_scrape.txt', 'r') as target_list:
            return [target.strip() for target in target_list]

    
    @staticmethod
    async def choose_token():
        with open('tokens/tokens.txt', 'r') as tokens:
            return random.choice(tokens.read().splitlines())
    

    @staticmethod
    async def write_data(data):
        with open('results/xuids.txt', 'a') as data_file:
            [data_file.write(f"{data[xuid]['xuid']}\n") for xuid in range(len(data))]
                

    @staticmethod
    async def remove_dupes():
        completed_lines_hash = set()
        cleaned_file = open('results/xuids_clean.txt', 'w')
        for line in open('xuids.txt', 'r'):
        	hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
        	if hashValue not in completed_lines_hash:
        		cleaned_file.write(line)
        		completed_lines_hash.add(hashValue)


if __name__ == '__main__':
    os.system('cls' if sys.platform == 'win32' else 'clear')
    scraper = Friend_Scraper()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scraper.initiate())
