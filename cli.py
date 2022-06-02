import click
from config import config_manager

import inquirer
from inquirer.themes import GreenPassion

def interactive_select_config(choices):
    q = [
        inquirer.List('config',
                    message='Choose a number',
                    choices=choices,
                    default='no'),
    ]

    return inquirer.prompt(q, theme=GreenPassion())


@click.group()
def main():
    choices= [1,2,3]
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
    


# @main.command()
# @click.option("config")

if __name__ == "__main__":
    main()

