import click


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option("--known", default="default", help="A known option")
@click.argument("args", nargs=-1)
@click.pass_context
def cli(ctx, known, args):
    # 获取所有传入的参数和选项
    parsed_options = ctx.params  # 包含所有定义的选项
    print("已定义的选项:", parsed_options)

    # 获取未定义的选项
    unprocessed_args = ctx.args  # 包含未定义的选项或参数
    print("未定义的选项:", unprocessed_args)


if __name__ == "__main__":
    cli()
