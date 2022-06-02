from telethon.sync import TelegramClient
class telegram:

    def __init__(self, api_id, api_hash, phone) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        print(self.phone)
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)


    def _connect(self):
        self.client.connect()
        print("connect")
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone)
            print(self.phone)
            self.client.sign_in(self.phone, input('Enter the code: '))

    def run(self):
        self._connect()