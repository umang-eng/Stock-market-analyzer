# Contributing to Fintech AI News Platform

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## 🤝 How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Commit your changes** (`git commit -m 'Add some amazing feature'`)
5. **Push to the branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

## 📋 Code Style Guidelines

### Frontend (React)
- Use functional components with hooks
- Follow ESLint configuration
- Use Tailwind CSS for styling
- Maintain responsive design (mobile-first)
- Keep components small and focused

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints where applicable
- Add docstrings to functions
- Use Pydantic for data validation
- Keep functions under 100 lines when possible

### Git Commit Messages
- Use clear, descriptive messages
- Start with a verb (Add, Fix, Update, Remove)
- Reference issue numbers if applicable
- Keep the first line under 72 characters

Example:
```
Add Redis caching to market data API

Implements high-performance caching using Google Cloud Memorystore
to reduce API costs and improve response times. Resolves #42.
```

## 🧪 Testing

### Frontend Testing
```bash
npm run test
```

### Backend Testing
```bash
# Navigate to the backend directory
cd serverless/pipeline
python -m pytest tests/
```

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Browser/OS information (for frontend issues)
- Relevant error messages or logs

## 💡 Feature Requests

For feature requests, please:
- Check if it's already requested
- Describe the use case clearly
- Explain how it benefits users
- Consider implementation complexity

## 🔍 Pull Request Process

1. Ensure your code follows style guidelines
2. Add/update tests as needed
3. Update documentation
4. Ensure all tests pass
5. Request review from maintainers

## 📝 Documentation

- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update API documentation for endpoint changes
- Include examples when adding new features

## 🔐 Security

- Never commit API keys or secrets
- Report security vulnerabilities privately
- Follow secure coding practices
- Review dependency updates for vulnerabilities

## ✅ Checklist Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No console.log statements left behind
- [ ] No commented-out code
- [ ] Environment variables properly handled
- [ ] No hardcoded credentials
- [ ] Responsive design maintained
- [ ] Cross-browser compatibility checked

## 📞 Getting Help

- Open an issue for bug reports or questions
- Check existing issues and documentation
- Join discussions in the issues section
- Contact maintainers for sensitive matters

## 🙏 Thank You

Thank you for contributing to this project! Your efforts help make this platform better for everyone.

