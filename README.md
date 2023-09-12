# rent-or-buy
A tool assisting the decision whether to rent or to buy

## Setup
```shell
poetry install
```

## Running
```shell
poetry run gunicorn rent_or_buy:server
```

## Development setup
```shell
poetry install --with dev,test
```

## Running in debug mode
```shell
poetry run rent-or-buy
```
