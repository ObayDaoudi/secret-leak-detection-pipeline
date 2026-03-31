# demo/unsafe-config.py
# ❌ UNSAFE EXAMPLE — hardcoded secrets (triggers Gitleaks)
# This file exists purely to DEMONSTRATE the scanner catching secrets.
# Never do this in real code!
 
# Fake AWS credentials (will be caught by Gitleaks)
AWS_ACCESS_KEY_ID     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
 
# Fake GitHub token (will be caught by Gitleaks)
GITHUB_TOKEN = "ghp_exampleFakeToken1234567890abcdef"
 
# Fake generic API key
API_KEY = "sk-examplefakeapikey1234567890abcdef"
