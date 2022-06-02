import configparser
import os

config = configparser.ConfigParser()
FILE_NAME = 'config.ini'
PATH = os.getcwd() + '/' + FILE_NAME;

class config_manager:
    # Just a small function to write the file
    def write_file(self, *args):
        config.write(open(PATH, 'w'))

    def conf_exists(self):
        return os.path.exists(PATH)

    def write_conf(self, api_id: str, api_hash: str, phone: str, config_number: str = None):
        if self.conf_exists():
            if config_number == None:
                config_number = self.count_config() + 1
            config['conf' + str(config_number)] = {'api_id': api_id, 'api_hash': api_hash, 'phone': phone}
            self.write_file(config)

    def count_config(self):
        if self.conf_exists():
            config.read(PATH)
            return len(config.sections())

    def read_conf(self):
        if not self.conf_exists:
            print("No configuration files")
            exit()
        config.read(PATH)
        print(config.items())
        return config.items()
    
    def select_section(self):
        config.read(PATH)
        phones = []
        for section in config.sections():
            phones.append(config[section]['phone'])
        return phones
    
    def select_section_from_number(self, phone):
        config.read(PATH)
        for section in config.sections():
            if phone in config[section]['phone']:
                return section

# if __name__ == '__main__':

#     read_conf()
#     write_conf('123','45687','78946', '1')
#     write_conf('123','456855555557','78946', '2')
#     write_conf('123','45687','78946', '3')
#     write_conf('123','45687','78946', '90')
#     read_conf()
#     if not conf_exists():
#         print("Please configurate the script with the --config")

    

