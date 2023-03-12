from re import sub

class Database_Manager:
    def __init__(self) -> None:
        pass


    @staticmethod
    async def write_recents(xuid):
        with open('database/completed/completed_database.txt', 'a') as completed_database:
            completed_database.write(f"{xuid}\n")


    @staticmethod
    async def clean_loaded_database(xuid):
        with open('database/xuid_database/xuid_list.txt', 'r+') as current_file:
            text = current_file.read()
            text = sub(xuid, '', text)
            current_file.seek(0)
            current_file.write(text)
            current_file.truncate()
        

    @staticmethod
    async def clear_file():
        open('database/xuid_database/xuid_list.txt', 'w').close()
    

    @staticmethod
    async def write_clean_list(database):
        with open('database/xuid_database/xuid_list.txt', 'a') as completed_database:
            [completed_database.write(f"{xuid}\n") for xuid in database]
