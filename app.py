#!/usr/bin/env python3
"""
AutoGob - Plataforma de colas para el registro de requerimientos sociales
Social Requirements Registry Application
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///social_requirements.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class SocialRequirement(db.Model):
    """Model for social requirements"""
    id = db.Column(db.Integer, primary_key=True)
    citizen_name = db.Column(db.String(100), nullable=False)
    citizen_email = db.Column(db.String(120), nullable=False)
    citizen_phone = db.Column(db.String(20), nullable=True)
    requirement_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(10), default='normal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SocialRequirement {self.id}: {self.citizen_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'citizen_name': self.citizen_name,
            'citizen_email': self.citizen_email,
            'citizen_phone': self.citizen_phone,
            'requirement_type': self.requirement_type,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Routes
@app.route('/')
def index():
    """Home page showing the queue and registration form"""
    requirements = SocialRequirement.query.order_by(
        SocialRequirement.created_at.desc()
    ).limit(10).all()
    
    # Queue statistics
    total_requirements = SocialRequirement.query.count()
    pending_requirements = SocialRequirement.query.filter_by(status='pending').count()
    
    return render_template('index.html', 
                         requirements=requirements,
                         total_requirements=total_requirements,
                         pending_requirements=pending_requirements)

@app.route('/register', methods=['GET', 'POST'])
def register_requirement():
    """Register a new social requirement"""
    if request.method == 'POST':
        # Basic validation
        citizen_name = request.form.get('citizen_name', '').strip()
        citizen_email = request.form.get('citizen_email', '').strip()
        citizen_phone = request.form.get('citizen_phone', '').strip()
        requirement_type = request.form.get('requirement_type', '')
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'normal')
        
        # Validation
        errors = []
        if not citizen_name or len(citizen_name) < 2:
            errors.append('El nombre es obligatorio y debe tener al menos 2 caracteres')
        if not citizen_email or '@' not in citizen_email:
            errors.append('El email es obligatorio y debe ser válido')
        if not requirement_type:
            errors.append('El tipo de requerimiento es obligatorio')
        if not description or len(description) < 10:
            errors.append('La descripción es obligatoria y debe tener al menos 10 caracteres')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html', 
                                 citizen_name=citizen_name,
                                 citizen_email=citizen_email,
                                 citizen_phone=citizen_phone,
                                 requirement_type=requirement_type,
                                 description=description,
                                 priority=priority)
        
        # Create requirement
        requirement = SocialRequirement(
            citizen_name=citizen_name,
            citizen_email=citizen_email,
            citizen_phone=citizen_phone if citizen_phone else None,
            requirement_type=requirement_type,
            description=description,
            priority=priority
        )
        
        db.session.add(requirement)
        db.session.commit()
        
        flash('Requerimiento registrado exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/api/requirements', methods=['GET'])
def api_get_requirements():
    """API endpoint to get all requirements"""
    requirements = SocialRequirement.query.order_by(
        SocialRequirement.created_at.desc()
    ).all()
    
    return jsonify([req.to_dict() for req in requirements])

@app.route('/api/requirements', methods=['POST'])
def api_create_requirement():
    """API endpoint to create a new requirement"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['citizen_name', 'citizen_email', 'requirement_type', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    requirement = SocialRequirement(
        citizen_name=data['citizen_name'],
        citizen_email=data['citizen_email'],
        citizen_phone=data.get('citizen_phone'),
        requirement_type=data['requirement_type'],
        description=data['description'],
        priority=data.get('priority', 'normal')
    )
    
    db.session.add(requirement)
    db.session.commit()
    
    return jsonify(requirement.to_dict()), 201

@app.route('/api/requirements/<int:req_id>/status', methods=['PUT'])
def api_update_status(req_id):
    """API endpoint to update requirement status"""
    requirement = SocialRequirement.query.get_or_404(req_id)
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    requirement.status = data['status']
    requirement.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(requirement.to_dict())

@app.route('/queue')
def queue_status():
    """Show current queue status and management interface"""
    requirements = SocialRequirement.query.order_by(
        SocialRequirement.priority.desc(),
        SocialRequirement.created_at.asc()
    ).all()
    
    return render_template('queue.html', requirements=requirements)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)