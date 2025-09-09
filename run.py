# run.py
from app import create_app, db
from app.models import User, Role

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Makes these items available in the `flask shell` for easy testing.
    """
    return {'db': db, 'User': User, 'Role': Role}