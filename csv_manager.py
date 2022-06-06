from telethon.tl.types import Channel
import csv
import os

CSV_PATH = os.getcwd() + '/csv/' 

HEADERS = ['INDEX', 'ID', 'access_hash', 'first_name', 'last_name', 'username', 'phone']

def path_csv(channel: Channel):
    return CSV_PATH + channel + '.csv'

def get_csv_files():
    return [f for f in os.listdir(CSV_PATH) if os.path.isfile(os.path.join(CSV_PATH, f))]

def write_users_to_csv(channel: Channel, users):
    with open(path_csv(channel), 'a', newline='', encoding='UTF8') as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADERS)
        for user in users:
            try:
                print(user.username)
                writer.writerow({ user.id, 
                user.access_hash, 
                user.first_name, 
                user.last_name, 
                user.username, 
                user.phone })
            except Exception as e:
                print(e)

def write_users_to_csv_dictwriter(channel: Channel, users):
    rows = [{
        'ID':           user.id,
        'access_hash':  user.access_hash,
        'first_name':   user.first_name,
        'last_name':    user.last_name, 
        'username' :    user.username, 
        'phone' :       user.phone
    } for user in users]

    write_header = os.path.exists(path_csv(channel))
    with open(path_csv(channel), 'a', newline='', encoding='UTF8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        if not write_header: writer.writeheader()
        writer.writerows(rows)

def read_csv(csv_file: str):
    with open(CSV_PATH + csv_file, 'r', encoding="UTF8") as csvfile:
        reader = csv.DictReader(csvfile)
        result = list()
        for row in reader:
            result.append(row)
    return result