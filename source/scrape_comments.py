import aiohttp
import os

class Database_Collector:
    def __init__(self) -> None:
        self.continuation_token = ''


    async def get_comment_xuids(self, token, post_link, feed_xuid):
        headers = {
            'Authorization': token,
            'X-XBL-Contract-Version': '3',
            'Accept-Language': 'en-US'
        }

        session = aiohttp.ClientSession()
        try:
            async with session.get(f'https://comments.xboxlive.com/{post_link}/comments?continuationToken={self.continuation_token}', headers=headers) as scrape_request:
                if scrape_request.status in [200, 201, 202, 204]:

                    comment_data = await scrape_request.json()

                    if len(comment_data['comments']) >= 1:

                        for xuid_range in range(len(comment_data['comments'])):
                            await self.write_scraped_data(comment_data['comments'][xuid_range]['xuid'])

                        print(f" \x1b[1;37m[\x1b[1;36m+\x1b[1;37m] collected {len(comment_data['comments'])} XUID's from \x1b[1;36m{feed_xuid}\x1b[1;37m")

                    else:
                        print(f' \x1b[1;37m[\x1b[1;33m!\x1b[1;37m] \x1b[1;36m{feed_xuid}\x1b[1;37m\'s post has no comments!')
                elif scrape_request.status == 401:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] authorization token invalid! exiting..')
                    os._exit(0)
                else:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] failed to collect \x1b[1;36m{feed_xuid}\x1b[1;37m\'s post\'s comment data. status: \x1b[1;33m{scrape_request.status}')

            await session.close()
            
        except ConnectionResetError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] excepted \x1b[1;33mConnectionResetError\x1b[1;37m')
            pass
        except OSError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] excepted \x1b[1;31mOSError\x1b[1;37m')
            pass
        except TimeoutError: 
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] excepted \x1b[1;31mTimeoutError\x1b[1;37m')
            pass

    
    @staticmethod
    async def write_scraped_data(xuid):
        with open('database/scraping/scraped_database.txt', 'a') as scraped_data:
            scraped_data.write(f'{xuid}\n')
