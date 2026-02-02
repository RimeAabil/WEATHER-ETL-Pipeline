#!/usr/bin/env python3
"""Create Airflow admin user if it doesn't exist."""

from airflow.www.app import create_app
import sys

def create_admin_user():
    app = create_app()
    with app.app_context():
        from airflow.www.app import appbuilder
        
        try:
            # Check if admin user exists
            user = appbuilder.sm.find_user(username='admin')
            if not user:
                # Get the Admin role
                role_admin = appbuilder.sm.find_role("Admin")
                if not role_admin:
                    print('Admin role not found, creating...')
                    # This shouldn't happen, but just in case
                    sys.exit(1)
                
                # Create the admin user
                user = appbuilder.sm.add_user(
                    username='admin',
                    first_name='Admin',
                    last_name='User',
                    email='admin@example.com',
                    role=role_admin,
                    password='admin'
                )
                print('Admin user created successfully')
            else:
                print('Admin user already exists')
        except Exception as e:
            print(f'Error creating user: {e}')
            import traceback
            traceback.print_exc()
            sys.exit(0)

if __name__ == '__main__':
    create_admin_user()