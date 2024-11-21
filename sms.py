import inspect

import click
import argparse
from module.api import get_scripts, get_script
from typing import get_origin, get_args, Annotated


# 主命令行
@click.group()
def cli():
    """A Script Management System"""
    pass


@cli.command()
@click.argument("key")
def search(key):
    """search a script by name or description"""
    click.echo(f"Initialized the database {key}")
    script_list = get_scripts()
    for mod, scripts in script_list.items():
        for Script in scripts:
            script = Script()
            print(script)


# 使用脚本
@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("name")
@click.argument("params", nargs=-1)
@click.pass_context
def use(ctx, name, params):
    """use a script"""
    Script = get_script(name)
    if Script is None:
        return click.echo(f"{name} script is not found")
    # 解析 run 函数中的参数
    signature = inspect.signature(Script.run)
    parameters = signature.parameters
    # 将参数添加到 argparse 中
    parser = argparse.ArgumentParser()
    for key, attr in parameters.items():
        if key == "self":
            continue
        annotation = attr.annotation
        if attr.default is not inspect._empty:
            parser.add_argument(
                f"--{key}", f"-{key}", type=get_args(annotation)[0], default=attr.default
            )
        else:
            parser.add_argument(f"--{key}", f"-{key}", type=get_args(annotation)[0])
    args, unknown = parser.parse_known_args()
    script = Script()
    # 如果参数不完整
    if any(True for arg, val in vars(args).items() if val is None):
        script.help()
    else:
        result = script.do(**vars(args))
        click.echo(result)


if __name__ == "__main__":
    cli()
