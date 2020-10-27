from app import create_app
import os
from flask_script import Manager
from app import db
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
from flask_migrate import Migrate, MigrateCommand

from app.v1.models.user import User

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = create_app(os.environ['CONFIG_TYPE'])
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """Like a 'runserver' command but shorter, lol."""
    app.run()


@manager.command
def run_tests():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def run_seed():
    user = User(username="admin", password="abc1234", credits=0, administrator=True)
    db.session.add(user)
    db.session.commit()


@manager.command
def debug_fix():
    """
    I have trouble with hitting breakpoints in lask-RESTful class methods.
    This method help me.
    """
    app.config['DEBUG'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=False)


@manager.command
def db_init():
    migrate = Migrate()
    migrate.init_app(app, db)


if __name__ == '__main__':
    manager.run()
