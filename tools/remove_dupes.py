import hashlib

class Remove_Dupes:
    
    async def clean(self):
        completed_lines_hash = set()
        cleaned_file = open('database/scraping/dupes_cleared.txt', 'w')
        for line in open('database/scraping/scraped_database.txt', 'r'):
            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
            if hashValue not in completed_lines_hash:
                cleaned_file.write(line)
                completed_lines_hash.add(hashValue)
