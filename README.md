# Obearon

A Discord bot to verify and link Discord accounts to Warframe accounts.

## Requirements
- [Python 3.12](https://www.python.org/downloads/)
- An Email account on a platform that supports IMAP.
- A Warframe account registered through that email that is at least MR2.
- After MR2, you must choose in the forum settings to be notified via mail upon receiving messages. 

## Setup

Make sure you only install after being in a virtual environment.

```bash
pip install .
```

## Environment variables

Copy [the example env file](.env.example) into a file called `.env` and fill in the values like this:

| Environment variable | Description                                               |
|----------------------|-----------------------------------------------------------|
| EMAIL_USERNAME       | The email username                                        |
| EMAIL_PASSWORD       | The email password                                        |
| USER_ID              | The Forum ID of the Warframe account you created.         |
| DISCORD_TOKEN        | The Discord token for the Discord bot                     |

## Running

To run this application, execute

```bash
python main.py
```

### Running from Docker

Build the docker image with:
```bash
docker build -t obearon:latest .
```

If you haven't run the docker image before, make sure the data folder exists:
```bash
mkdir data
```

Run the docker image with:
```bash
docker run -d --name obearon --mount type=bind,src="$(pwd)"/data,dst=/data --env-file=.env obearon:latest
```

## Database

This project uses alembic for database version management.

To check whether you have pending changes that need to be migrated:
```bash
alembic check
```

To create a migration with pending changes:
```bash
alembic revision --autogenerate
```

## Linting

There are several automatic code formatting tools available.

```bash
black .
isort .
flake8
pylint .
```
