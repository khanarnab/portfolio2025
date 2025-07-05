#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField, EmailField, validators
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import logging

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    github_url = db.Column(db.String(200))
    live_url = db.Column(db.String(200))
    image_filename = db.Column(db.String(100))
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage from {self.name}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

# Forms
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

# Routes
@app.route('/')
def index():
    """Homepage with hero section and featured projects"""
    featured_projects = Project.query.filter_by(featured=True).limit(3).all()
    return render_template('index.html', featured_projects=featured_projects)

@app.route('/about')
def about():
    """About page with detailed background"""
    return render_template('about.html')

@app.route('/projects')
def projects():
    """Projects portfolio page"""
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=all_projects)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Individual project detail page"""
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/skills')
def skills():
    """Skills and technologies page"""
    skills_data = {
        'languages': [
            {'name': 'Python', 'level': 90},
            {'name': 'JavaScript', 'level': 85},
            {'name': 'HTML/CSS', 'level': 95},
            {'name': 'SQL', 'level': 80},
            {'name': 'Bash', 'level': 75}
        ],
        'frameworks': [
            {'name': 'Flask', 'level': 90},
            {'name': 'Django', 'level': 75},
            {'name': 'Bootstrap', 'level': 85},
            {'name': 'jQuery', 'level': 80}
        ],
        'tools': [
            {'name': 'Git/GitHub', 'level': 90},
            {'name': 'Docker', 'level': 85},
            {'name': 'AWS', 'level': 70},
            {'name': 'CI/CD', 'level': 80},
            {'name': 'Linux', 'level': 85}
        ]
    }
    return render_template('skills.html', skills=skills_data)

@app.route('/blog')
def blog():
    """Blog/articles listing page"""
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('blog_post.html', post=post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Save message to database
            message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            
            flash('Thank you for your message! I\'ll get back to you soon.', 'success')
            logger.info(f'New contact message from {form.name.data} ({form.email.data})')
            return redirect(url_for('contact'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error saving contact message: {str(e)}')
            flash('There was an error sending your message. Please try again.', 'error')
    
    return render_template('contact.html', form=form)

@app.route('/resume')
def resume():
    """Resume/CV page"""
    return render_template('resume.html')

@app.route('/download-resume')
def download_resume():
    """Download resume as PDF"""
    return send_from_directory('static/downloads', 'resume.pdf', as_attachment=True)

# API Routes
@app.route('/api/projects')
def api_projects():
    """API endpoint for projects data"""
    projects = Project.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'tech_stack': p.tech_stack,
        'github_url': p.github_url,
        'live_url': p.live_url,
        'featured': p.featured
    } for p in projects])

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# CLI Commands
@app.cli.command()
def init_db():
    """Initialize the database with sample data"""
    db.create_all()
    
    # Sample projects
    if not Project.query.first():
        sample_projects = [
            Project(
                title='Portfolio Website',
                description='A modern portfolio website built with Flask, featuring CI/CD automation with GitHub Actions.',
                tech_stack='Python, Flask, SQLite, Bootstrap, GitHub Actions, Docker',
                github_url='https://github.com/yourusername/portfolio',
                featured=True
            ),
            Project(
                title='Task Management API',
                description='RESTful API for task management with authentication and real-time updates.',
                tech_stack='Python, Flask, PostgreSQL, JWT, WebSockets',
                github_url='https://github.com/yourusername/task-api',
                featured=True
            ),
            Project(
                title='Data Visualization Dashboard',
                description='Interactive dashboard for visualizing business metrics and KPIs.',
                tech_stack='Python, Plotly, Dash, Pandas, PostgreSQL',
                github_url='https://github.com/yourusername/data-dashboard',
                featured=True
            )
        ]
        
        for project in sample_projects:
            db.session.add(project)
    
    # Sample blog post
    if not BlogPost.query.first():
        sample_post = BlogPost(
            title='Building a Modern Portfolio with Flask and CI/CD',
            content='In this post, I\'ll walk you through building a modern portfolio website using Flask and implementing CI/CD automation with GitHub Actions...',
            excerpt='Learn how to build a modern portfolio website with Flask and automate deployment with GitHub Actions.',
            slug='building-modern-portfolio-flask-cicd',
            published=True
        )
        db.session.add(sample_post)
    
    db.session.commit()
    print('Database initialized with sample data!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Run in development mode
    app.run(debug=True, host='0.0.0.0', port=5000)