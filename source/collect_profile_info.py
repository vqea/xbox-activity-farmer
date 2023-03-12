import aiohttp
import os

class Profile_Information:

    @staticmethod
    async def retrieve_information(token):
        headers = {
            'Authorization': token, 
            'X-XBL-Contract-Version': '2', 
            'Accept-Language': 'en-US',
            'Connection': 'keep-alive'
        }

        session = aiohttp.ClientSession()
        try:
            async with session.get(f'https://profile.xboxlive.com/users/me/profile/settings', headers=headers) as info_request:
                if info_request.status in [200, 201, 202, 204]:

                    data = await info_request.json()

                    xuid = data['profileUsers'][0]['id']

                    print(f' \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] successfully retrieved account information! \n \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] my XUID: \x1b[1;35m{xuid}\x1b[1;37m')
                elif info_request.status == 401:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] authorization token invalid! exiting..')
                    os._exit(0)
                else:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] failed to retrieve account information, exiting..')
                    os._exit(0)

            await session.close()
            return xuid
            
        except ConnectionResetError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] excepted \x1b[1;33mConnectionResetError\x1b[1;37m')
            pass
        except OSError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] excepted \x1b[1;31mOSError\x1b[1;37m')
            pass
        except TimeoutError: 
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] excepted \x1b[1;31mTimeoutError\x1b[1;37m')
            pass
