# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of our project seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not** disclose the vulnerability publicly until it has been addressed by our team
2. Submit a detailed report to our security team at [security@companyhunter.com](mailto:security@companyhunter.com)
3. Include the following information in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fixes (if any)

### What to Expect

- We will acknowledge receipt of your report within 48 hours
- We will provide a more detailed response within 7 days
- We will keep you informed about our progress
- We will publicly acknowledge your responsible disclosure (if you wish)

## Security Measures

### API Security
- All API keys are stored securely in environment variables
- Rate limiting is implemented to prevent abuse
- Input validation is performed on all API endpoints
- HTTPS is enforced for all API communications

### Data Security
- User data is encrypted at rest
- Sensitive information is never logged
- Regular security audits are performed
- Dependencies are regularly updated for security patches

### Authentication
- Secure password hashing using bcrypt
- JWT tokens for API authentication
- Session management with secure cookies
- OAuth2 integration for third-party services

## Best Practices for Users

1. **API Keys**
   - Never commit API keys to version control
   - Rotate keys regularly
   - Use the principle of least privilege

2. **Environment Variables**
   - Keep .env files out of version control
   - Use different keys for development and production
   - Regularly audit environment variables

3. **Dependencies**
   - Keep all dependencies up to date
   - Use `npm audit` and `pip-audit` regularly
   - Review dependency changes before updating

## Security Updates

Security updates are released as patches to the current version. We recommend always running the latest version of CompanyHunter.

## Contact

For security-related inquiries, please contact:
- Email: [security@companyhunter.com](mailto:security@companyhunter.com)
- PGP Key: [Available upon request]

---

*Last updated: March 20, 2023*