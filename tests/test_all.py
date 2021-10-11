import pytest

import portfolio_balancer as pb


def test_load_config(config):
    assert len(config) > 0


def test_total_worth(config):
    assert pb.total_worth(config) == 230000


def test_check_allocation_ok(config):
    pb.check_allocation(config)


@pytest.mark.parametrize("percentages", [[98, 1], [100, 1]])
def test_check_allocation_error(config, percentages):
    config = {f"fund_{p}": {"percentage": p} for p in percentages}
    with pytest.raises(Exception):
        pb.check_allocation(config)


def test_dollar_allocation(config):
    allocation = pb.dollar_allocation(config)
    assert sum(allocation.values()) == pb.total_worth(config)


def test_placement(config):
    placement = pb.placement(config)

    for account, total in config["account"].items():
        assert sum(placement[account].values()) == total

    for fund, total in pb.dollar_allocation(config).items():
        assert sum(v.get(fund, 0) for v in placement.values()) == total
