import os
import pathlib

import pytest

import portfolio_balancer as pb


@pytest.fixture
def config():
    def _config(name: str = 'test'):
        return pb.load_config(
            os.path.join(pathlib.Path(__file__).parent, 'config', f"{name}.yml")
        )

    return _config()
