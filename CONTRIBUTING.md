# Contributing to CompanyHunter 🚀

Thank you for your interest in contributing to CompanyHunter! This document provides guidelines and instructions for contributing to our project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Testing](#testing)
- [Documentation](#documentation)

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/CompanyHunter.git
   cd CompanyHunter
   ```

2. **Set Up Development Environment**
   ```bash
   # Backend setup
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend setup
   cd client
   npm install
   ```

3. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🔄 Development Workflow

1. **Keep Your Fork Updated**
   ```bash
   git remote add upstream https://github.com/original-owner/CompanyHunter.git
   git fetch upstream
   git pull upstream main
   ```

2. **Make Your Changes**
   - Follow the [Style Guide](#style-guide)
   - Write tests for new features
   - Update documentation

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

## 🔍 Pull Request Process

1. **Create a Pull Request**
   - Use the PR template
   - Link related issues
   - Provide a clear description

2. **PR Checklist**
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] Code follows style guide
   - [ ] All tests pass
   - [ ] No merge conflicts

3. **Review Process**
   - Address review comments
   - Update PR as needed
   - Wait for approval

## 📝 Style Guide

### Python (Backend)
```python
# Use type hints
def process_job(job: Dict[str, Any]) -> Job:
    """Process a job listing.
    
    Args:
        job: Raw job data dictionary
        
    Returns:
        Processed Job object
    """
    pass
```

### JavaScript/React (Frontend)
```javascript
// Use functional components with hooks
const JobCard = ({ job, onSave }) => {
  const [isSaved, setIsSaved] = useState(false);
  
  return (
    <div className="job-card">
      {/* Component content */}
    </div>
  );
};
```

### Git Commit Messages
- Use conventional commits
- Format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore

## 🧪 Testing

### Backend Tests
```bash
cd server
pytest
```

### Frontend Tests
```bash
cd client
npm test
```

## 📚 Documentation

- Update README.md for major changes
- Add JSDoc/Python docstrings
- Update API documentation if needed
- Keep CHANGELOG.md updated

## 🤝 Need Help?

- Open an issue
- Join our [Discord community](https://discord.gg/your-server)
- Check our [FAQ](FAQ.md)

---

Thank you for contributing to CompanyHunter! 🎉 