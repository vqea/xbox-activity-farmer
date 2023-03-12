def main():
    with open('splits/non_split.txt', 'r') as xuid_list:
        for xuid in [xuid.strip() for xuid in xuid_list]:
            with open('splits/split.txt', 'a') as file:
                file.write(f"{xuid.split(':')[1]}\n")

if __name__ == '__main__':
    main()
