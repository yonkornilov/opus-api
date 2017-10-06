# -*- coding: utf-8 -*-

"""Console script for opus_api."""


from util import minint, maxint
import click
import opus_api
import pkg_resources
from exceptions import InvalidSrcException, InvalidTrgException


class MainGroup(click.Group):
    def parse_args(self, ctx, args):
        if len(args) == 1 and args[0] == '--version':
            version = pkg_resources.require("opus_api")[0].version
            click.echo(version)
            exit(0)
        else:
            super(MainGroup, self).parse_args(ctx, args)


@click.group(cls=MainGroup)
@click.option('--version', is_flag=True, help="Get version")
def main(version, args=None):
    """
    \b
                /$$$$$$            /$$$$$$$  /$$   /$$  /$$$$$$
               /$$__  $$          | $$__  $$| $$  | $$ /$$__  $$
      /$$$$$$$| $$  \ $$  /$$$$$$ | $$  \ $$| $$  | $$| $$  \__/
     /$$_____/| $$  | $$ /$$__  $$| $$$$$$$/| $$  | $$|  $$$$$$
    | $$      | $$  | $$| $$  \__/| $$____/ | $$  | $$ \____  $$
    | $$      | $$  | $$| $$      | $$      | $$  | $$ /$$  \ $$
    |  $$$$$$$|  $$$$$$/| $$      | $$      |  $$$$$$/|  $$$$$$/
     \_______/ \______/ |__/      |__/       \______/  \______/


    OPUS (opus.lingfil.uu.se) Command Line Interface
    """


@main.command()
@click.argument('src')
@click.argument('target')
@click.option('--minimum', default=minint(),
              help="Minimum sentences (src + target tokens) in millions")
@click.option('--maximum', default=maxint(),
              help="Maximum sentences (src + target tokens) in millions")
def get(src, target, minimum, maximum):
    """
    Get src-target corpora
    """
    if minimum < 0 and minimum != minint():
        raise click.UsageError('minimum cannot be negative')
    if maximum < 0:
        raise click.UsageError('maximum cannot be negative')
    if minimum > maximum:
        raise click.UsageError('minimum cannot be greater than maximum')
    try:
        click.echo(opus_api.get(src, target, minimum, maximum))
    except InvalidSrcException as e:
        raise(click.UsageError('invalid source: ' + e.lang))
    except InvalidTrgException as e:
        raise(click.UsageError('invalid target: ' + e.lang))


@main.command()
def langs():
    """
    Get list of available languages
    """
    click.echo(opus_api.langs())


if __name__ == "__main__":
    main()
