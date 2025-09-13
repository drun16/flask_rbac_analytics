# tests/test_auth.py
from app import db
from app.models import User, Role

def test_home_page(test_client):
    """Test that the home page loads correctly."""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Flask Auth & RBAC Project!" in response.data

def test_auth_flow(test_client):
    """Test the full registration, logout, and login flow."""
    # Test Registration
    response = test_client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Congratulations, you are now a registered user!" in response.data

    # Test Logout (first need to be logged in, but we start logged out)
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the Flask Auth & RBAC Project!" in response.data

    # Test Login
    response = test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Hello, testuser!" in response.data
    assert b"Welcome to your dashboard" in response.data

def test_rbac_access_control(test_client):
    """Test that only admins can access the analytics page."""
    # Create an admin user
    admin_role = Role.query.filter_by(name='Admin').first()
    admin_user = User(username='adminuser', email='admin@test.com', role=admin_role)
    admin_user.set_password('adminpass')
    
    # Create a regular user
    user_role = Role.query.filter_by(name='User').first()
    regular_user = User(username='regularuser', email='user@test.com', role=user_role)
    regular_user.set_password('userpass')

    db.session.add_all([admin_user, regular_user])
    db.session.commit()

    # Log in as regular user and try to access analytics
    test_client.post('/login', data={'username': 'regularuser', 'password': 'userpass'})
    response = test_client.get('/analytics')
    assert response.status_code == 403 # Forbidden

    # Log out
    test_client.get('/logout')

    # Log in as admin user and access analytics
    test_client.post('/login', data={'username': 'adminuser', 'password': 'adminpass'})
    response = test_client.get('/analytics', follow_redirects=True)
    assert response.status_code == 200
    assert b"Admin Analytics" in response.data# tests/test_auth.py

