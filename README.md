# Portfolio Balancer

A tool to help balance a portfolio tax-efficiently across a variety of accounts.

## Installation

    poetry install

## Use

1. Make a [configuration file](./tests/config/test.yml) with your investment accounts, desired portfolio allocation, and [tax-efficient placement order](https://www.bogleheads.org/wiki/Tax-efficient_fund_placement)
1. Run `pb <path to configuration file>`

## Development

    poetry install
    poetry shell
    ...

### Running Tests

    pytest
