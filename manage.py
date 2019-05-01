from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Blog, Comments


# app = create_app("development")
app = create_app('production')
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql+psycopg2://moringa:augustine@localhost/blogger"

manager = Manager(app)
manager.add_command("server", Server)



@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Blog=Blog, Comments=Comments)


migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    app.secret_key = 'warble'
 
    manager.run()