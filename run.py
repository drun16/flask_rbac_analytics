# run.py
from app import create_app, db
from app.models import User, Role
import click

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Makes these items available in the `flask shell` for easy testing.
    """
    return {'db': db, 'User': User, 'Role': Role}

@app.cli.command("seed-roles")
def seed_roles():
    """Seeds the database with initial User and Admin roles."""
    roles = ['User', 'Admin']
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
            db.session.add(role)
            print(f"Adding role: {r}")
    db.session.commit()
    print("Roles seeded.")