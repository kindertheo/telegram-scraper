import click
from click_default_group import DefaultGroup
from config import config_manager

import inquirer
from inquirer.themes import GreenPassion
from csv_manager import get_csv_files, read_csv

from telegram import telegram

def interactive_select_config(choices, message: str = "Choose one"):
    q = [
        inquirer.List('config',
                    message=message,
                    choices=choices,
                    default='no'),
    ]

    return inquirer.prompt(q, theme=GreenPassion())


@click.group()
def main():
    pass

@main.command()
@click.option("--api_id", prompt=" Enter api_id", type=str)
@click.option("--api_hash", prompt=" Enter api_hash", type=str)
@click.option("--phone", prompt=" Enter phone number with prefix (+33)", type=str)
def create_config(api_id, api_hash, phone):
    config_manager().write_conf(api_id=api_id, api_hash=api_hash, phone=phone)
    click.echo("""
    api_id : {}
    api_hash :  {}
    phone :  {}""".format(api_id, api_hash, phone))


@main.command()
def select_config():
    choices = config_manager().select_section()
    response = interactive_select_config(choices) 
    conf = config_manager().select_section_from_number(response['config'])
    print(conf)
    return conf

@main.command()
@click.pass_context
def scrape_all(ctx):
    conf = ctx.forward(select_config)
    ids = config_manager().get_datas_from_config(conf)
    telegram(api_id=ids['api_id'],
            api_hash=ids['api_hash'],
            phone=ids['phone']
    ).get_users()

@main.command()
@click.pass_context
def scrape_one(ctx):
    conf = ctx.forward(select_config)
    ids = config_manager().get_datas_from_config(conf)
    tlg = telegram(api_id=ids['api_id'],
            api_hash=ids['api_hash'],
            phone=ids['phone']) #.get_users_by_channel()
    channels = tlg.get_channels()
    print(channels)
    response = interactive_select_config(channels)
    tlg.get_users_from_channel(response['config'])

@main.command()
@click.pass_context
def invit(ctx):
    conf = ctx.forward(select_config)
    ids = config_manager().get_datas_from_config(conf)
    tgm = telegram(api_id=ids['api_id'],
            api_hash=ids['api_hash'],
            phone=ids['phone'])
    channels = tgm.get_channels()
    files = get_csv_files()
    response = interactive_select_config(files, message="Choose a CSV file to import in your Channel/Group")
    users = read_csv(response['config'])
    channel_response = interactive_select_config(channels, message="Choose a channel to invit")
    # print(users)
    tgm.invit_users(channel_response['config'], users)

if __name__ == "__main__":
    main()

