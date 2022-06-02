from telethon.sync import TelegramClient
from pprint import pprint


api_id = 0
api_hash = ''
phone = ''
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))

chats.extend(result.chats)

for chat in chats:
    try:
        print(chat.title)
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue


from telethon import functions, types
channel_username='DAVO TRADING 🦅' # your channel
channel_entity=client.get_entity(channel_username)
posts = client(functions.messages.GetHistoryRequest(
    peer=channel_entity,
    limit=100,
    offset_date=None,
    offset_id=0,
    max_id=0,
    min_id=0,
    add_offset=0,
    hash=0))

# channel = client(ResolveUsernameRequest(channel_username))

user_list = client.iter_dialogs()
print(user_list)
for user in user_list:
    if user.is_channel:
        print(dir(user.entity))
for mess in posts.messages:
    try:
        pass
        #print(mess.message)
    except Exception:
        pass
exit()

pprint(groups)

pprint(dir(result.chats[0]))
pprint(result.chats)
