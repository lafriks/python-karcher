# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

import click
import dataclasses
import json
import logging

from karcher.auth import Session
from karcher.exception import KarcherHomeException
from karcher.karcher import KarcherHome
from karcher.consts import Region

try:
    from rich import print as echo
except ImportError:
    echo = click.echo

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

class GlobalContextObject:
    def __init__(self, debug: int = 0, output: str = "json", region: Region = Region.EU):
        self.debug = debug
        self.output = output
        self.region = region

    def print(self, result):
        data_variable = getattr(result, "data", None)
        if data_variable is not None:
            result = data_variable
        if self.output == "json_pretty":
            echo(json.dumps(result, cls=EnhancedJSONEncoder, indent=4))
        else:
            echo(json.dumps(result, cls=EnhancedJSONEncoder))

@click.group()
@click.option("-d", "--debug", is_flag=True)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["json", "json_pretty"]),
    default="json",
    help="Output format. Default: 'json'")
@click.option(
    "-r",
    "--region", 
    type=click.Choice([Region.EU, Region.US, Region.CN]),
    default=Region.EU,
    help="Region of the server to query. Default: 'eu'")
@click.pass_context
def cli(ctx: click.Context, debug: int, output: str, region: Region):
    """Tool for connectiong and getting information from Kärcher Home Robots."""
    level = logging.INFO
    if debug > 0:
        level = logging.DEBUG

    logging.basicConfig(level=level)

    ctx.obj = GlobalContextObject(debug=debug, output=output, region=region)

def safe_cli():
    try:
        cli()
    except KarcherHomeException as ex:
        echo(json.dumps({
            'code': ex.code,
            'message': ex.message
        }))
        return

@cli.command()
@click.pass_context
def get_urls(ctx: click.Context):
    """Get region information."""

    kh = KarcherHome(region=ctx.obj.region)
    d = kh.get_urls()

    ctx.obj.print(d)

@cli.command()
@click.option('--username', '-u', help='Username to login with.')
@click.option('--password', '-p', help='Password to login with.')
@click.pass_context
def login(ctx: click.Context, username: str, password: str):
    """Get user session tokens."""

    kh = KarcherHome(region=ctx.obj.region)
    ctx.obj.print(kh.login(username, password))

@cli.command()
@click.option('--username', '-u', default=None, help='Username to login with.')
@click.option('--password', '-p', default=None, help='Password to login with.')
@click.option('--token', '-t', default=None, help='Authorization token.')
@click.pass_context
def devices(ctx: click.Context, username: str, password: str, token: str):
    """List all devices."""

    kh = KarcherHome(region=ctx.obj.region)
    sess = None
    if token != None:
        sess = Session.from_token(token, '')
    elif username != None and password != None:
        sess = kh.login(username, password)
    else:
        raise click.BadParameter('Must provide either token or username and password.')

    devices = kh.get_devices(sess)

    # Logout if we used a username and password
    if token == None:
        kh.logout(sess)

    ctx.obj.print(devices)
