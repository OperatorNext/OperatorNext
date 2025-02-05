# Contributing Guide

Thank you for your interest in contributing to OperatorNext! This guide will help you get started with contributing to our project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a healthy and welcoming community.

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm 10+
- Python 3.11+
- Docker & Docker Compose
- Git

### Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/OperatorNext.git
cd OperatorNext
```

3. Set up development environment:
```bash
# Install dependencies
pnpm install

# Set up pre-commit hooks
pre-commit install

# Copy environment files
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local

# Start development services
docker-compose up -d
```

## Development Workflow

### Branch Naming

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Performance: `perf/description`

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Tests
- `chore`: Maintenance

Example:
```
feat(auth): add Google OAuth support

Add Google OAuth authentication provider with proper error handling
and user profile synchronization.

Closes #123
```

### Pull Request Process

1. Create a new branch from `main`
2. Make your changes
3. Run tests and linting
4. Push your changes
5. Create a pull request
6. Wait for review

## Code Style

### TypeScript/JavaScript

Follow our ESLint and Prettier configurations:

```bash
# Check code style
pnpm lint

# Fix code style issues
pnpm format
```

Key rules:
- Use TypeScript
- 2 spaces for indentation
- Single quotes for strings
- Semicolons required
- Maximum line length: 100 characters

### Python

Follow our Ruff and Black configurations:

```bash
# Check code style
ruff check .

# Format code
black .
```

Key rules:
- Use type hints
- 4 spaces for indentation
- Double quotes for strings
- Maximum line length: 88 characters
- Follow PEP 8

## Testing

### Frontend Tests

```bash
# Run unit tests
pnpm test

# Run e2e tests
pnpm test:e2e

# Run specific test
pnpm test -t "test name"
```

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_file.py -k "test_name"

# Run with coverage
pytest --cov=app
```

## Documentation

### Writing Documentation

- Use clear and concise language
- Include code examples
- Provide step-by-step instructions
- Add screenshots for UI changes
- Keep documentation up to date

### Building Documentation

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## Submitting Changes

### Feature Requests

1. Check existing issues
2. Create a new issue using the feature request template
3. Discuss the feature with maintainers
4. Start implementation after approval

### Bug Reports

1. Check existing issues
2. Create a new issue using the bug report template
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
   - Screenshots if applicable

### Pull Requests

1. Reference related issues
2. Describe your changes
3. Include test coverage
4. Update documentation
5. Add to CHANGELOG.md
6. Request review from maintainers

## Review Process

### Code Review

We follow these principles:
- Be respectful and constructive
- Focus on code, not the person
- Explain the reasoning behind suggestions
- Link to relevant documentation

### Review Checklist

- [ ] Code follows style guide
- [ ] Tests are included
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Changes are appropriate in scope
- [ ] No security vulnerabilities
- [ ] Performance is considered

## Release Process

### Version Numbers

We use [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality
- PATCH version for bug fixes

### Release Steps

1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Run tests and checks
5. Create release tag
6. Deploy to staging
7. Deploy to production

## Community

### Getting Help

- [Discord Community](https://discord.gg/operatornext)
- [GitHub Discussions](https://github.com/OperatorNext/OperatorNext/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/operatornext)

### Communication Channels

- Technical discussions: GitHub Discussions
- Real-time chat: Discord
- Bug reports: GitHub Issues
- Feature requests: GitHub Issues

## Additional Resources

- [Development Guide](../guides/development.md)
- [Architecture Overview](../architecture/overview.md)
- [API Documentation](../api/reference.md)
- [Testing Guide](testing.md)
- [Style Guide](style-guide.md) 