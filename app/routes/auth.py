from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_admin,
                'is_super_admin': user.is_super_admin
            }
        }), 200
    
    return jsonify({'message': 'Credenciais inválidas'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

@auth_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_super_admin:
        return jsonify({'message': 'Acesso negado'}), 403
        
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Usuário já existe'}), 400
        
    user = User(
        username=username,
        is_admin=is_admin,
        is_super_admin=False
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'user': {
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin
        }
    }), 201

@auth_bp.route('/users', methods=['GET'])
@login_required
def list_users():
    if not current_user.is_super_admin:
        return jsonify({'message': 'Acesso negado'}), 403
        
    users = User.query.all()
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin,
            'is_super_admin': user.is_super_admin
        } for user in users]
    }), 200

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if not current_user.is_super_admin:
        return jsonify({'message': 'Acesso negado'}), 403
        
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.set_password(data['password'])
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
        
    db.session.commit()
    
    return jsonify({
        'message': 'Usuário atualizado com sucesso',
        'user': {
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin,
            'is_super_admin': user.is_super_admin
        }
    }), 200

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_super_admin:
        return jsonify({'message': 'Acesso negado'}), 403
        
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200 