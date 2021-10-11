import locale
import logging
import math
import yaml


log = logging.getLogger()
locale.setlocale(locale.LC_ALL, "")


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def total_worth(config: dict) -> float:
    return sum([float(v) for v in config["account"].values()])


def check_allocation(config: dict) -> None:
    total = sum(config["allocation"].values())
    if not math.isclose(total, 100):
        raise Exception(f"Allocation percentages add up to {total}")


def dollar_allocation(config: dict) -> dict:
    check_allocation(config)

    total = total_worth(config)
    dollar_allocation = {
        fund: total * (pct / 100) for fund, pct in config["allocation"].items()
    }

    return dollar_allocation


def placement(config: dict) -> dict:
    placement = {}
    left_to_allocate = dollar_allocation(config)
    left_in_account = config["account"].copy()

    for fund, accounts in config["placement"].items():
        if fund not in left_to_allocate:
            raise Exception(f"Unknown fund: {fund}")

        for acct in accounts:
            if acct not in left_in_account:
                raise Exception(f"Unknown account: {acct}")

            placement.setdefault(acct, {})[fund] = 0
            if left_to_allocate[fund] >= left_in_account[acct]:
                placement[acct][fund] = left_in_account[acct]
            else:
                placement[acct][fund] = left_to_allocate[fund]
            if placement[acct][fund]:
                left_in_account[acct] -= placement[acct][fund]
                left_to_allocate[fund] -= placement[acct][fund]
                log.debug(
                    f"Allocated {locale.currency(placement[acct][fund], grouping=True)} to '{fund}' in '{acct}'"
                )

        if left_to_allocate[fund] >= 0.01:
            log.warning(
                f"Unable to allocate '{fund}':"
                f" {locale.currency(left_to_allocate[fund], grouping=True)}"
            )

    return placement
