import click
from click_default_group import DefaultGroup
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
def scrape(ctx):
    print("hello world")
    conf = ctx.forward(select_config)
    ids = config_manager().get_datas_from_config(conf)
    telegram.run(ids)

@main.command()
def hello():
    print("hello")

# @main.command()
# @click.option("config")

if __name__ == "__main__":
    main()

