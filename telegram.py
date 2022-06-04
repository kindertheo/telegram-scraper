import time
import telethon
from telethon.sync import TelegramClient
from pprint import pprint
from telethon.errors.rpcerrorlist import ChannelPrivateError, ChatAdminRequiredError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import InputPeerEmpty
from telethon import functions, types
import re
from string import ascii_lowercase
import csv

class telegram:

    def __init__(self, api_id, api_hash, phone) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)


    def _connect(self):
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone)
            self.client.sign_in(self.phone, input('Enter the code: '))

    def run(self):
        self._connect()
        channels = self.get_channels()
        for chan in channels:
            self.get_users_from_channel(chan)

    def find_channel():
        pass

    def find_groups():
        pass

    def get_users_from_channel(self, channel: telethon.tl.types.Channel):
        queryKey = list(ascii_lowercase)
        all_participants = []
        # channel = 'The Moon Group'
        chan_id = channel.id
        for key in queryKey:
            offset = 0
            limit = 100
            while True:
                participants = self.client(GetParticipantsRequest(
                    chan_id, ChannelParticipantsSearch(key), offset, limit,
                    hash=0
                ))
                if not participants.users:
                    break
                i = 0
                for user in participants.users:
                    try:
                        if re.findall(r"\b[a-zA-Z]", user.first_name)[0].lower() == key:
                            all_participants.append(user)
                            print(i)
                            i = i + 1            
                    except Exception as e:
                        print(e)
                        pass

                offset += len(participants.users)
                self.write_users_to_csv(channel.title, participants.users)

                print(offset)

    def get_channels(self):
        chats = []
        last_date = None
        chunk_size = 200
        
        result = self.client(GetDialogsRequest(
                    offset_date=last_date,
                    offset_id=0,
                    offset_peer=InputPeerEmpty(),
                    limit=chunk_size,
                    hash = 0
                ))

        chats.extend(result.chats)
        channels = []
        for chat in chats:
            try:
                channels.append(chat.title)
            except:
                continue
        
        return chats;

    def write_users_to_csv(self, channel: telethon.tl.types.Channel, users):
        pprint(channel)
        with open(channel + '.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for user in users:
                print("write", user)
                try:
                    writer.writerow({ user.id, 
                    user.access_hash, 
                    user.first_name, 
                    user.last_name, 
                    user.username, 
                    user.phone })
                except Exception as e:
                    print(e)

    def iter_participants_from_channel(self, channel):
        try:
        
            channel_connect = self.client.get_entity(channel.id)
            channel_full_info = self.client(GetFullChannelRequest(channel=channel_connect))
            user_count = channel_full_info.full_chat.participants_count
            print(user_count)
            user_list = self.client.iter_participants(channel)

            # user_count = self.client.participant_count(chat)
            # print(user_list)
            i = 0
            for user in user_list:
                if not isinstance(user, (types.ChannelParticipantBanned, types.ChannelParticipantLeft)):
                    i = i + 1
                    if (i % 3000) == 0:
                        time.sleep(10)
                    print(i,"/",user_count)
                    print(user.id, user.access_hash, user.phone, user.first_name, user.last_name)

        except (ChatAdminRequiredError, ChannelPrivateError):
            print(channel.title, "no permission")


        # user_list = self.client.iter_dialogs()
        # print(user_list)
        # for user in user_list:
        #     if user.is_channel:
        #         print(user.entity)