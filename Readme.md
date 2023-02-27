
# SWAPI People explorer

Small project to explore people of Star Wars universum.

First generate `.env` file based on `.env_example`

Then start application with:

`docker-compose up`

## Requirements
- Docker & Docker-compose

## Dependecy management
- Poetry

## Application dependencies:
- Python ^3.11
- Django ^4.1.7
- requests ^2.28.2
- petl ^1.7.12
- psycopg2 ^2.9.5
- numpy ^1.24.2

## Git hooks:
- black
- isort
- flake8

## Code style:
Black - default settings

Flake8 - max-line=99



# Views:
## Collections
View of all collected data with timestamps and filenames

## Collection
View of data in file, it is people or planets (not parsed).

## Value counter
Count occurences of values or combination of values in selected dataset.
