# tests/conftest.py
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import User, Role
from config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    """Create a test client for the application."""
    app = create_app(config_class=TestConfig)
    
    with app.test_client() as testing_client:
        with app.app_context():
            # Create the database and tables
            db.create_all()
            # Seed roles for tests
            role_user = Role(name='User')
            role_admin = Role(name='Admin')
            db.session.add_all([role_user, role_admin])
            db.session.commit()
            
            yield testing_client # this is where the testing happens
            
            db.drop_all() # Clean up the database