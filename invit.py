from random import random
import time
import re
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest
from telethon.tl.types import InputPeerChannel ,InputUser, PeerUser
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError

api_id = 12209102
api_hash = 'd891d23e6c60510b501ea2a16a3cc9d2'
phone = '+33774573971'
session = phone + '.session'

client = TelegramClient(phone, api_id, api_hash);
client.connect()

def invit_users_with_list(client: TelegramClient, channel: types.Channel, user_list: list):
    # chann=client.get_entity(channel) 
    channel_id = channel.id
    channel_access_hash = channel.access_hash

    chanal=InputPeerChannel(channel_id, channel_access_hash)
    #user = client(ResolveUsernameRequest('Z'))
    for user in user_list:
        print(user)
        try:
            if user['username'] == '':
                continue
            input_user = client.get_entity(user['username'])

            if(input_user):
                result = client(InviteToChannelRequest(chanal,[input_user]))
            else:
                input_user = InputUser(user['ID'],user['access_hash'])
                result = client(InviteToChannelRequest(chanal,[input_user]))
            # print(result)
            print("Waiting for 60-180 Seconds...")
            time.sleep(random.randrange(0, 5))
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            print("Waiting {} seconds".format(20))
            time.sleep(20)
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
            print("Waiting for 5 Seconds...")
            time.sleep(random.randrange(0, 5))
        except FloodWaitError as fwe:
            p = re.search("[0-9]{1,6}", str(fwe))
            if p:
                print(p.group())
                print("Sleeping for {}".format(str(p.group())))
                time.sleep(int(p.group()))
                continue
        except Exception as e:
            print("Unexpected Error", e)
            continue