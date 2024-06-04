from flask.cli import AppGroup
from .users import seed_users, undo_users
from .companies import seed_companies, undo_companies
from .creators import seed_creators, undo_creators
from .opportunities import seed_opportunities, undo_opportunities
from .genres import seed_genres, undo_genres
from .types import seed_types, undo_types

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_opportunities()
        undo_creators()
        undo_companies()
        undo_users()
        undo_types()
        undo_genres()
    seed_genres()
    seed_types()
    seed_users()
    seed_companies()
    seed_creators()
    seed_opportunities()



# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_opportunities()
    undo_creators()
    undo_companies()
    undo_users()
    undo_types()
    undo_genres()
    # Add other undo functions here
