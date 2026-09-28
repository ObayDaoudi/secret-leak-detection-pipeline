# Secret & Credential Leak Detection Pipeline
 
A **DevSecOps** CI/CD pipeline that automatically scans your repository for exposed secrets, API keys, and credentials — and blocks insecure builds before they reach production.
 
Built with **Jenkins** + **Gitleaks**, this project demonstrates a production-ready security gate with audit-ready HTML reporting.
 
---
 
## Pipeline Overview
 
```
Developer Push
      │
      ▼
┌─────────────────────┐
│  Checkout Code      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Install Gitleaks   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Secret Leak Scan   │  ◄── Scans all files & Git history
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Generate HTML Report│  ◄── Audit-ready report with findings
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Publish Report     │  ◄── Available in Jenkins UI
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Fail-Fast Gate     │  ◄── Blocks build if secrets found
└─────────────────────┘
```
 
---
 
## Features
 
| Feature | Description |
|---|---|
| **Multi-pattern scanning** | Detects AWS keys, GitHub tokens, DB passwords, private keys, and more |
| **Fail-fast security gate** | Blocks Jenkins build immediately if secrets are detected |
| **HTML security report** | Clean, audit-ready report with findings, severity, file locations |
| **Secret redaction** | Secrets are redacted in reports — safe to share with stakeholders |
| **Custom rules** | Extend default Gitleaks rules via `.gitleaks.toml` |
| **Allowlist support** | Skip known false positives (test fixtures, example files) |
| **Artifact archiving** | Reports archived in Jenkins for every build |
 
---
 
## Tech Stack
 
- **Jenkins** — CI/CD pipeline orchestration
- **Gitleaks** — Secret detection engine
- **Groovy** — Pipeline scripting (Jenkinsfile)
- **HTML/CSS** — Security report generation
 
---
 
## Getting Started
 
### Prerequisites
 
- Jenkins server (local or remote)
- Jenkins plugins:
  - `Pipeline`
  - `HTML Publisher`
  - `Git`
- Internet access (to download Gitleaks on first run) OR pre-install Gitleaks on the Jenkins agent
 
### Setup
 
**1. Clone this repository**
```bash
git clone https://github.com/<your-username>/secret-leak-detection-pipeline.git
```
 
**2. Create a Jenkins Pipeline job**
- Go to Jenkins → New Item → Pipeline
- Under *Pipeline*, select **Pipeline script from SCM**
- Set SCM to **Git** and point to this repository
- Set Script Path to `Jenkinsfile`
 
**3. Run the pipeline**
- Click **Build Now**
- View the **Secret Leak Detection Report** in the build's sidebar
 
---
 
## Project Structure
 
```
secret-leak-detection/
├── Jenkinsfile              # Main pipeline definition
├── .gitleaks.toml           # Custom rules & allowlist config
├── demo/
│   ├── safe-config.py       # Example of secure secret handling
│   └── unsafe-config.py     # Example that triggers the scanner
└── README.md
```
 
---
 
## Configuration
 
Edit `.gitleaks.toml` to:
- **Add custom rules** for patterns specific to your stack
- **Add allowlist paths** to skip test fixtures or example files
- **Add allowlist regexes** to suppress known false positives
 
```toml
[allowlist]
paths = [
    '''tests/fixtures/.*''',
    '''README\.md''',
]
regexes = [
    '''YOUR_API_KEY_HERE''',
]
```
 
---
 
## Report Example
 
The pipeline generates a clean HTML report for every build, including:
 
- **Scan status** (CLEAN / SECRETS DETECTED)
- **Total findings count**
- **Per-finding detail**: severity, rule, file, line number, redacted secret, commit, author
- **Remediation steps**
 
---
 
## Remediation Guide
 
If the pipeline fails due to detected secrets:
 
1. **Revoke** the exposed credential immediately
2. **Rotate** with a new secret from the provider (AWS, GitHub, etc.)
3. **Remove** from code — use `git filter-repo` to purge from Git history
4. **Use secrets managers** — environment variables, HashiCorp Vault, AWS Secrets Manager
5. **Re-run** the pipeline to confirm the issue is resolved
