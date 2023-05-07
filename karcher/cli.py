# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

import asyncio
import click
import dataclasses
import json
import logging
from functools import wraps

from karcher.exception import KarcherHomeException
from karcher.karcher import KarcherHome
from karcher.consts import Region

try:
    from rich import print as echo
except ImportError:
    echo = click.echo


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class GlobalContextObject:
    def __init__(
            self,
            debug: int = 0,
            output: str = 'json',
            country: str = 'GB'):
        self.debug = debug
        self.output = output
        self.country = country

    def print(self, result):
        data_variable = getattr(result, 'data', None)
        if data_variable is not None:
            result = data_variable
        if self.output == 'json_pretty':
            echo(json.dumps(result, cls=EnhancedJSONEncoder, indent=4))
        else:
            echo(json.dumps(result, cls=EnhancedJSONEncoder))


@click.group()
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode.')
@click.option(
    '-o',
    '--output',
    type=click.Choice(['json', 'json_pretty']),
    default='json',
    help='Output format. Default: "json"')
@click.option(
    '-c',
    '--country',
    default='GB',
    help='Country of the server to query. Default: "GB"')
@click.pass_context
def cli(ctx: click.Context, debug: int, output: str, country: str):
    """Tool for connectiong and getting information from Kärcher Home Robots."""
    level = logging.INFO
    if debug > 0:
        level = logging.DEBUG

    logging.basicConfig(level=level)

    ctx.obj = GlobalContextObject(debug=debug, output=output, country=country.upper())


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
@coro
async def urls(ctx: click.Context):
    """Get URL information."""

    kh = await KarcherHome.create(country=ctx.obj.country)
    d = await kh.get_urls()

    ctx.obj.print(d)


@cli.command()
@click.option('--username', '-u', help='Username to login with.')
@click.option('--password', '-p', help='Password to login with.')
@click.pass_context
@coro
async def login(ctx: click.Context, username: str, password: str):
    """Get user session tokens."""

    kh = await KarcherHome.create(country=ctx.obj.country)
    ctx.obj.print(kh.login(username, password))


@cli.command()
@click.option('--username', '-u', default=None, help='Username to login with.')
@click.option('--password', '-p', default=None, help='Password to login with.')
@click.option('--auth-token', '-t', default=None, help='Authorization token.')
@click.pass_context
@coro
async def devices(ctx: click.Context, username: str, password: str, auth_token: str):
    """List all devices."""

    kh = await KarcherHome.create(country=ctx.obj.country)
    if auth_token is not None:
        kh.login_token(auth_token, '')
    elif username is not None and password is not None:
        await kh.login(username, password)
    else:
        raise click.BadParameter(
            'Must provide either token or username and password.')

    devices = await kh.get_devices()

    # Logout if we used a username and password
    if auth_token is None:
        await kh.logout()

    ctx.obj.print(devices)


@cli.command()
@click.option('--username', '-u', default=None, help='Username to login with.')
@click.option('--password', '-p', default=None, help='Password to login with.')
@click.option('--auth-token', '-t', default=None, help='Authorization token.')
@click.option('--mqtt-token', '-m', default=None, help='MQTT authorization token.')
@click.option('--device-id', '-d', required=True, help='Device ID.')
@click.pass_context
@coro
async def device_properties(
        ctx: click.Context,
        username: str,
        password: str,
        auth_token: str,
        mqtt_token: str,
        device_id: str):
    """Get device properties."""

    kh = await KarcherHome.create(country=ctx.obj.country)
    if auth_token is not None:
        kh.login_token(auth_token, mqtt_token)
    elif username is not None and password is not None:
        await kh.login(username, password)
    else:
        raise click.BadParameter(
            'Must provide either token or username and password.')

    dev = None
    for device in await kh.get_devices():
        if device.device_id == device_id:
            dev = device
            break

    if dev is None:
        raise click.BadParameter('Device ID not found.')

    props = kh.get_device_properties(dev)

    # Logout if we used a username and password
    if auth_token is None:
        await kh.logout()

    ctx.obj.print(props)
