from tools import database_manager

class Filter_Targets:
    def __init__(self) -> None:
        self.filtered_targets = []
        self.clean_targets = 0
        self.completed_database = self.collect_completed()
        self.manager = database_manager.Database_Manager()


    async def filter_database(self, database):
        self.clean_targets = 0
        for xuid in database:
            if xuid not in self.completed_database:
                self.filtered_targets.append(xuid)
                self.clean_targets += 1
            print(f' \x1b[1;37m[\x1b[1;35m*\x1b[1;37m] filtering current database  |  new targets: (\x1b[1;36m{self.clean_targets}\x1b[1;37m/\x1b[1;36m{len(database)}\x1b[1;37m)', end='\r', flush=True)
        print(f' \x1b[1;37m[\x1b[1;35m*\x1b[1;37m] filtering current database  |  new targets: (\x1b[1;36m{self.clean_targets}\x1b[1;37m/\x1b[1;36m{len(database)}\x1b[1;37m)', end='\r\n', flush=True)
        return self.filtered_targets


    @staticmethod
    def collect_completed():
        with open('database/completed/completed_database.txt', 'r') as completed_database_list:
            completed_database_list = [xuid.strip() for xuid in completed_database_list]
        return completed_database_list
