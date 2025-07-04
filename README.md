# Portfolio Website

A modern, responsive portfolio website built with Flask, featuring automated CI/CD deployment with GitHub Actions.

## 🚀 Features

- **Modern Design**: Clean, responsive design with dark/light theme toggle
- **Full-Stack Architecture**: Flask backend with SQLite/PostgreSQL database
- **Portfolio Management**: Dynamic project showcase with admin interface
- **Contact System**: Functional contact form with email notifications
- **Blog Platform**: Built-in blog system for sharing insights
- **CI/CD Pipeline**: Automated testing, building, and deployment
- **Performance Optimized**: Lazy loading, caching, and optimized assets
- **SEO Friendly**: Meta tags, sitemap, and structured data
- **Security**: CSRF protection, input validation, and security headers

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 2.3+
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Forms**: Flask-WTF
- **Server**: Gunicorn

### Frontend
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Animations**: AOS (Animate On Scroll)
- **JavaScript**: Vanilla ES6+

### DevOps & Deployment
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Reverse Proxy**: Nginx
- **Caching**: Redis

## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Git
- Node.js 16+ (for development tools)

## 🏗️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/khanarnab/portfolio2025.git
   cd portfolio2025
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   flask init-db
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

Visit `http://localhost:5000` to see your portfolio!

### Docker Development

1. **Clone and navigate to project**
   ```bash
   git clone https://github.com/khanarnab/portfolio2025.git
   cd portfolio
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Initialize database**
   ```bash
   docker-compose exec web flask init-db
   ```

Services will be available at:
- Portfolio: http://localhost:5000
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Kibana: http://localhost:5601

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1

# Database
DATABASE_URL=sqlite:///portfolio.db
# For production: postgresql://user:password@host:port/database

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Social Media Links
GITHUB_URL=https://github.com/khanarnab
LINKEDIN_URL=https://linkedin.com/in/arnab-khan
```

### Database Configuration

The application supports both SQLite and PostgreSQL:

- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

To use PostgreSQL, set the `DATABASE_URL` environment variable:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio_db
```

## 🚀 Deployment

### GitHub Actions CI/CD

The repository includes a comprehensive CI/CD pipeline that automatically:

1. **Code Quality**: Runs Black, flake8, and security checks
2. **Testing**: Executes test suite with coverage reporting
3. **Building**: Creates Docker images and pushes to registry
4. **Deployment**: Deploys to staging and production environments
5. **Monitoring**: Runs performance tests and security scans

### Manual Deployment

#### Heroku
```bash
# Install Heroku CLI
heroku create your-portfolio-app
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
git push heroku main
```

#### DigitalOcean App Platform
```bash
# Use the included app.yaml for configuration
doctl apps create --spec app.yaml
```

#### AWS ECS
```bash
# Build and push Docker image
docker build -t your-portfolio .
docker tag your-portfolio:latest your-account.dkr.ecr.region.amazonaws.com/your-portfolio:latest
docker push your-account.dkr.ecr.region.amazonaws.com/your-portfolio:latest

# Deploy using ECS service
aws ecs update-service --cluster your-cluster --service your-service --force-new-deployment
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── conftest.py          # Test configuration
├── test_app.py          # Application tests
├── test_forms.py        # Form validation tests
├── test_models.py       # Database model tests
└── test_routes.py       # Route/endpoint tests
```

## 📊 Monitoring

### Application Metrics

The application includes built-in monitoring:

- **Health Check**: `/api/health` endpoint
- **Metrics**: Prometheus metrics collection
- **Logging**: Structured logging with ELK stack
- **Performance**: Response time and error tracking

### Available Dashboards

1. **Grafana**: Application metrics and system monitoring
2. **Kibana**: Log analysis and search
3. **Flower**: Celery task monitoring (if using background tasks)

## 🔒 Security

### Implemented Security Measures

- **CSRF Protection**: All forms include CSRF tokens
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Template auto-escaping enabled
- **Security Headers**: Configured via Flask-Talisman
- **Dependency Scanning**: Automated security checks in CI/CD

### Security Best Practices

1. **Environment Variables**: Never commit secrets to version control
2. **Database**: Use strong passwords and restrict access
3. **HTTPS**: Always use HTTPS in production
4. **Updates**: Keep dependencies updated regularly
5. **Backup**: Regular database backups

## 🎨 Customization

### Changing Theme Colors

Edit `static/css/style.css`:

```css
:root {
    --primary-color: #007bff;      /* Your primary color */
    --secondary-color: #6c757d;    /* Your secondary color */
    --accent-color: #28a745;       /* Your accent color */
}
```

### Adding New Sections

1. Create a new template in `templates/`
2. Add the route in `app.py`
3. Update navigation in `templates/base.html`
4. Add any required database models

### Customizing Content

1. **Profile Information**: Update personal details in templates
2. **Projects**: Add/edit projects via the admin interface or database
3. **Skills**: Modify skills data in the `/skills` route
4. **Social Links**: Update social media URLs in templates

## 📁 Project Structure

```
portfolio/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Development environment
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Homepage
│   ├── about.html             # About page
│   ├── projects.html          # Projects listing
│   ├── contact.html           # Contact form
│   └── errors/                # Error pages
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── js/
│   │   └── main.js            # JavaScript functionality
│   ├── images/                # Image assets
│   └── downloads/             # Downloadable files
├── tests/                     # Test files
├── logs/                      # Application logs
└── docs/                      # Documentation
```

## 🔄 Development Workflow

### Git Flow

1. **Feature Development**
   ```bash
   git checkout -b feature/new-feature
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

2. **Create Pull Request**
   - Target the `develop` branch
   - Include description and screenshots
   - Wait for CI/CD checks to pass

3. **Code Review**
   - Address reviewer feedback
   - Ensure all tests pass
   - Merge to `develop`

4. **Release**
   - Merge `develop` to `main`
   - Tag release version
   - Deploy to production

### Code Quality Standards

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Use ES6+ features
- **HTML/CSS**: Semantic markup and BEM methodology
- **Git**: Conventional commit messages
- **Testing**: Minimum 80% code coverage

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check database configuration
   echo $DATABASE_URL
   
   # Recreate database
   flask db drop
   flask db create
   flask init-db
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill process
   kill -9 <PID>
   ```

3. **Docker Build Issues**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild containers
   docker-compose build --no-cache
   ```

4. **CSS/JS Not Loading**
   ```bash
   # Clear Flask cache
   rm -rf __pycache__
   
   # Hard refresh browser (Ctrl+Shift+R)
   ```

### Debug Mode

Enable debug mode for detailed error messages:

```bash
export FLASK_DEBUG=1
python app.py
```

## 📈 Performance Optimization

### Backend Optimizations

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Query Optimization**: Use SQLAlchemy query profiling
3. **Caching**: Implement Redis caching for static data
4. **Compression**: Enable gzip compression in production

### Frontend Optimizations

1. **Image Optimization**: Compress images and use WebP format
2. **CSS/JS Minification**: Minify assets in production
3. **Lazy Loading**: Implement lazy loading for images
4. **CDN**: Use CDN for static assets

### Monitoring Performance

```bash
# Monitor application performance
docker-compose exec web python -m flask profiler

# Check database performance
docker-compose exec db psql -U portfolio_user -d portfolio_db -c "SELECT * FROM pg_stat_activity;"
```

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include type hints where appropriate
- Write tests for new functionality

## 📚 Resources

### Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Docker Documentation](https://docs.docker.com/)

### Learning Resources

- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [AOS](https://michalsnik.github.io/aos/) - Animations
- [GitHub Actions](https://github.com/features/actions) - CI/CD

## 📞 Support

If you have any questions or need help with setup, please:

1. Check the [Issues](https://github.com/yourusername/portfolio/issues) page
2. Create a new issue if your problem isn't already listed
3. Contact me directly via the portfolio contact form

## 🔄 Changelog



**Built with ❤️ using Flask and modern web technologies**