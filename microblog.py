from app import cli, create_app, db

from app.models import Post, User


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Post': Post,
        'User': User
    }
