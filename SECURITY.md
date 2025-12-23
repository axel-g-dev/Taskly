# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Taskly seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Please do not report security vulnerabilities through public GitHub issues.

### 2. Report Privately

Send a detailed report to:
- **GitHub Security Advisories**: [Report a vulnerability](https://github.com/axel-g-dev/Taskly/security/advisories/new)
- **Email**: (À définir - remplacer par votre email)

### 3. Include in Your Report

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)
- Your contact information

### 4. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-3 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release cycle

## Security Best Practices

### For Users

1. **Keep Taskly Updated**
   - Always use the latest version
   - Check for updates regularly

2. **Verify Downloads**
   - Only download from official GitHub repository
   - Verify checksums if provided

3. **Review Permissions**
   - Taskly only requires read access to system metrics
   - No network access required
   - No root/admin privileges needed

### For Developers

1. **Dependencies**
   - Keep dependencies up to date
   - Run `pip check` regularly
   - Use `safety` for vulnerability scanning

2. **Code Review**
   - All PRs require review
   - Security-sensitive changes require extra scrutiny

3. **Testing**
   - Run security tests before release
   - Use `bandit` for static analysis

## Known Security Considerations

### Data Privacy

- Taskly collects **system metrics only** (CPU, RAM, Network, Disk, Battery)
- **No personal data** is collected
- **No network communication** to external servers
- All data stays **local** on your machine

### File Permissions

- Configuration file: `~/Library/Application Support/Taskly/config.json`
- Export directory: `./exports/`
- Both use standard user permissions (no elevated privileges)

### Dependencies

Taskly uses minimal dependencies:
- `flet` - UI framework
- `psutil` - System metrics

Both are well-maintained and regularly audited.

## Security Audit

Last security audit: **2025-12-23**  
Audit score: **8.5/10**  
Status: **No critical vulnerabilities**

See [security_audit.md](security_audit.md) for details.

## Disclosure Policy

- We follow **responsible disclosure** practices
- Security researchers will be credited (if desired)
- We aim for transparency while protecting users

## Contact

For security-related questions:
- GitHub: [@axel-g-dev](https://github.com/axel-g-dev)
- Issues: [GitHub Issues](https://github.com/axel-g-dev/Taskly/issues) (for non-sensitive topics)

---

**Thank you for helping keep Taskly secure!** 🔒
