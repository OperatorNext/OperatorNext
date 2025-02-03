# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of OperatorNext seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- Primary: hi@operatornext.com
- Alternative: Please contact us on Telegram [@HaiPro_2025](https://t.me/HaiPro_2025)

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue:

* Type of issue
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit the issue

We prefer all communications to be in English or Chinese.

## Security Best Practices for Users

1. **API Keys & Secrets**
   - Never commit API keys or secrets directly to the repository
   - Use environment variables for sensitive information
   - Regularly rotate your API keys

2. **Browser Automation Security**
   - Always run browser automation in a controlled environment
   - Be cautious with user-provided scripts and URLs
   - Monitor resource usage and implement proper rate limiting

3. **Data Privacy**
   - Do not store sensitive user data
   - Clear browser data after automation tasks
   - Follow data protection regulations in your region

## Acknowledgments

We would like to thank the following security researchers who have helped us:

*(This section will be updated as we receive security contributions)* 