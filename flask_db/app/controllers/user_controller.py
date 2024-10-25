from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..connectors.db import db
from flask_login import login_user, logout_user

class UserController:
    @staticmethod
    def register(username, email, password, role='User'):
        try:
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                return {'message': 'Email already registered'}, 400

            # Create new user
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=role
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return {'message': 'User registered successfully'}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error during registration: {str(e)}'}, 500

    @staticmethod
    def login(email, password):
        try:
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                return {'message': 'Login successful'}, 200
            
            return {'message': 'Invalid email or password'}, 401
            
        except Exception as e:
            return {'message': f'Error during login: {str(e)}'}, 500

    @staticmethod
    def get_all_users():
        try:
            users = User.query.all()
            user_list = []
            for user in users:
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
                user_list.append(user_data)
            return {'users': user_list}, 200
            
        except Exception as e:
            return {'message': f'Error fetching users: {str(e)}'}, 500

    @staticmethod
    def logout():
        try:
            logout_user()
            return {'message': 'Logged out successfully'}, 200
        except Exception as e:
            return {'message': f'Error during logout: {str(e)}'}, 500