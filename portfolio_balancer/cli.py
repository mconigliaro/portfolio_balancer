import locale
import logging

import click
import rich.console
import rich.logging
import rich.table

import portfolio_balancer


locale.setlocale(locale.LC_ALL, "")


@click.command()
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode",
)
@click.argument("config_file")
def main(debug: str, config_file: str):
    handler_opts = {
        "console": rich.console.Console(stderr=True),
        "show_level": False,
        "show_path": False,
        "show_time": False,
    }
    if debug:
        handler_opts.update({"show_level": True})
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich.logging.RichHandler(**handler_opts)],
    )

    config = portfolio_balancer.load_config(config_file)
    placement = portfolio_balancer.placement(config)

    table = rich.table.Table()

    table.add_column()
    for fund in config["allocation"]:
        table.add_column(fund)
    table.add_column("Total")

    for account in config["account"]:
        amounts = [placement[account].get(f, 0) for f in config["allocation"]]
        amounts_str = [
            None if a == 0 else locale.currency(a, grouping=True) for a in amounts
        ]
        total = sum(amounts)
        total_str = None if total == 0 else locale.currency(total, grouping=True)
        table.add_row(f"[bold]{account}", *amounts_str, total_str)

    table.add_row()

    fund_totals = [
        sum(v.get(fund, 0) for v in placement.values()) for fund in config["allocation"]
    ]

    fund_totals_str = [
        None if total == 0 else locale.currency(total, grouping=True)
        for total in fund_totals
    ]

    table.add_row(
        "[bold]Total",
        *fund_totals_str,
        locale.currency(sum(fund_totals), grouping=True),
    )

    rich.console.Console().print(table)
