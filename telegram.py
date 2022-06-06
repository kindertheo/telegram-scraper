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
from telethon.tl.types import Channel
from telethon import functions, types
import re
from string import ascii_lowercase
import csv_manager
from invit import invit_users_with_list

class telegram:

    def __init__(self, api_id, api_hash, phone) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        self._connect()
        self.client.get_dialogs()

    def _connect(self):
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone)
            self.client.sign_in(self.phone, input('Enter the code: '))

    def get_users(self):
        self._connect()
        channels = self.get_channels()
        for chan in channels:
            try:
                self.get_users_from_channel(chan)
            except Exception as e:
                print(chan, e)

    def find_channel():
        pass

    def find_groups():
        pass

    def invit_users(self, channel, user_list):
        channel = self.get_channel_by_name(channel)
        print(channel)
        print(type(channel))
        invit_users_with_list(client=self.client, channel=channel, user_list=user_list)

    def get_users_from_channel(self, channel: str):
        channel = self.client.get_entity(channel)
        if isinstance(channel, list):
            channel = channel[0]
            print(type(channel))
        queryKey = list(ascii_lowercase)
        all_participants = []

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
                for user in participants.users:
                    try:
                        if re.findall(r"\b[a-zA-Z]", user.first_name)[0].lower() == key:
                            all_participants.append(user)
                    except Exception as e:
                        pass

                offset += len(participants.users)
                # csv_manager.write_users_to_csv(channel.title, participants.users)
                csv_manager.write_users_to_csv_dictwriter(channel.title, participants.users)

                print(offset)
            print(len(all_participants))


    def get_channel_by_name(self, name):
        channels_name = self.get_channels_entity()
        for cname in channels_name:
            if cname.title.lower() == name.lower():
                print("cname", type(channels_name[0]))
                return cname

    def get_channels_entity(self):
        last_date = None
        chunk_size = 200
        
        return self.client(GetDialogsRequest(
                    offset_date=last_date,
                    offset_id=0,
                    offset_peer=InputPeerEmpty(),
                    limit=chunk_size,
                    hash = 0
                )).chats

    def get_channels(self):
        # chats = []
        # last_date = None
        # chunk_size = 200
        
        # result = self.client(GetDialogsRequest(
        #             offset_date=last_date,
        #             offset_id=0,
        #             offset_peer=InputPeerEmpty(),
        #             limit=chunk_size,
        #             hash = 0
        #         ))

        # chats.extend(result.chats)
        chats = self.get_channels_entity()
        channels = []
        for chat in chats:
            try:
                channels.append(chat.title)
            except:
                continue
        
        return channels

    def iter_participants_from_channel(self, channel):
        try:
        
            channel_connect = self.client.get_entity(channel.id)
            channel_full_info = self.client(GetFullChannelRequest(channel=channel_connect))
            user_count = channel_full_info.full_chat.participants_count
            print("Number of users : ", user_count)
            user_list = self.client.iter_participants(channel)

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