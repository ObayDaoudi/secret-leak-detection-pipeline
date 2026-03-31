pipeline {
    agent any

    environment {
        GITLEAKS_VERSION = "8.18.2"
        REPORT_DIR       = "reports"
        REPORT_FILE      = "reports/gitleaks-report.json"
        HTML_REPORT      = "reports/security-report.html"
        SCAN_EXIT_CODE   = "0"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Install Gitleaks') {
            steps {
                sh '''
                    if ! command -v gitleaks &> /dev/null; then
                        echo "Installing Gitleaks v${GITLEAKS_VERSION}..."
                        curl -sSL https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz \
                            -o /tmp/gitleaks.tar.gz
                        tar -xzf /tmp/gitleaks.tar.gz -C /tmp
                        sudo mv /tmp/gitleaks /usr/local/bin/gitleaks
                        chmod +x /usr/local/bin/gitleaks
                        echo "Gitleaks installed successfully."
                    else
                        echo "Gitleaks already installed: $(gitleaks version)"
                    fi
                '''
            }
        }

        stage('Prepare Report Directory') {
            steps {
                sh 'mkdir -p ${REPORT_DIR}'
            }
        }

        stage('Secret Leak Scan') {
            steps {
                script {
                    echo "Running Gitleaks secret scan..."
                    def exitCode = sh(
                        script: """
                            gitleaks detect \
                                --source . \
                                --report-format json \
                                --report-path ${REPORT_FILE} \
                                --redact \
                                --no-git \
                                --verbose || true
                        """,
                        returnStatus: true
                    )
                    env.SCAN_EXIT_CODE = exitCode.toString()
                    echo "Gitleaks scan exit code: ${exitCode}"
                }
            }
        }

        stage('Generate HTML Report') {
            steps {
                script {
                    def reportJson = "{}"
                    def findings = []
                    def scanStatus = "CLEAN"
                    def statusColor = "#28a745"

                    if (fileExists(env.REPORT_FILE)) {
                        reportJson = readFile(env.REPORT_FILE).trim()
                        if (reportJson && reportJson != "null" && reportJson != "[]") {
                            try {
                                findings = readJSON(text: reportJson)
                                if (findings && findings.size() > 0) {
                                    scanStatus = "SECRETS DETECTED"
                                    statusColor = "#dc3545"
                                }
                            } catch (e) {
                                echo "Could not parse JSON report: ${e.message}"
                            }
                        }
                    }

                    def findingsRows = ""
                    if (findings && findings.size() > 0) {
                        findings.each { f ->
                            def rule      = f.RuleID     ?: f.ruleId     ?: "N/A"
                            def file      = f.File       ?: f.file       ?: "N/A"
                            def line      = f.StartLine  ?: f.startLine  ?: "N/A"
                            def secret    = f.Secret     ?: f.secret     ?: "[REDACTED]"
                            def commit    = f.Commit     ?: f.commit     ?: "N/A"
                            def author    = f.Author     ?: f.author     ?: "N/A"
                            def severity  = "HIGH"
                            def badgeColor = "#dc3545"

                            findingsRows += """
                            <tr>
                                <td><span class='badge' style='background:${badgeColor}'>${severity}</span></td>
                                <td><code>${rule}</code></td>
                                <td><code>${file}</code></td>
                                <td>${line}</td>
                                <td><code class='redacted'>${secret}</code></td>
                                <td><code>${commit.take(8)}</code></td>
                                <td>${author}</td>
                            </tr>
                            """
                        }
                    } else {
                        findingsRows = """
                        <tr>
                            <td colspan='7' style='text-align:center; color:#28a745; font-weight:600;'>
                                ✅ No secrets detected. Repository is clean.
                            </td>
                        </tr>
                        """
                    }

                    def htmlContent = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Secret Leak Detection Report</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; color: #333; }
        .header { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 30px 40px; }
        .header h1 { font-size: 26px; font-weight: 700; margin-bottom: 6px; }
        .header p { font-size: 13px; opacity: 0.75; }
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 30px; }
        .card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); border-left: 4px solid #ccc; }
        .card.status { border-color: ${statusColor}; }
        .card.info   { border-color: #007bff; }
        .card-label  { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 8px; }
        .card-value  { font-size: 22px; font-weight: 700; }
        .status-badge { display: inline-block; padding: 6px 16px; border-radius: 20px; font-size: 13px;
                        font-weight: 600; background: ${statusColor}; color: white; margin-top: 4px; }
        .section { background: white; border-radius: 10px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); margin-bottom: 24px; }
        .section h2 { font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #1a1a2e; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th { background: #f8f9fa; padding: 10px 12px; text-align: left; font-weight: 600; color: #555; border-bottom: 2px solid #e9ecef; }
        td { padding: 10px 12px; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }
        tr:hover td { background: #fafafa; }
        .badge { padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; color: white; }
        code { background: #f1f3f5; padding: 2px 6px; border-radius: 4px; font-size: 12px; color: #d63384; }
        .redacted { color: #6c757d !important; font-style: italic; }
        .footer { text-align: center; font-size: 12px; color: #aaa; padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔐 Secret Leak Detection Report</h1>
        <p>Generated by Jenkins CI/CD Pipeline &nbsp;|&nbsp; Powered by Gitleaks</p>
    </div>
    <div class="container">
        <div class="summary-grid">
            <div class="card status">
                <div class="card-label">Scan Status</div>
                <div><span class="status-badge">${scanStatus}</span></div>
            </div>
            <div class="card info">
                <div class="card-label">Total Findings</div>
                <div class="card-value">${findings ? findings.size() : 0}</div>
            </div>
            <div class="card info">
                <div class="card-label">Scan Date</div>
                <div class="card-value" style="font-size:14px;">${new Date().format('yyyy-MM-dd HH:mm')}</div>
            </div>
            <div class="card info">
                <div class="card-label">Branch</div>
                <div class="card-value" style="font-size:14px;">${env.GIT_BRANCH ?: env.BRANCH_NAME ?: 'N/A'}</div>
            </div>
        </div>

        <div class="section">
            <h2>📋 Findings Detail</h2>
            <table>
                <thead>
                    <tr>
                        <th>Severity</th>
                        <th>Rule</th>
                        <th>File</th>
                        <th>Line</th>
                        <th>Secret (Redacted)</th>
                        <th>Commit</th>
                        <th>Author</th>
                    </tr>
                </thead>
                <tbody>
                    ${findingsRows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🛡️ Remediation Steps</h2>
            <ol style="padding-left:20px; line-height:2;">
                <li>Immediately revoke and rotate any exposed credentials or API keys.</li>
                <li>Remove the secret from the codebase and all Git history using <code>git filter-repo</code>.</li>
                <li>Add the secret pattern to <code>.gitleaks.toml</code> allowlist if it is a false positive.</li>
                <li>Use environment variables or a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager).</li>
                <li>Re-run the pipeline to confirm the issue is resolved.</li>
            </ol>
        </div>
    </div>
    <div class="footer">Secret Leak Detection Pipeline &mdash; Jenkins + Gitleaks</div>
</body>
</html>"""

                    writeFile file: env.HTML_REPORT, text: htmlContent
                    echo "HTML report generated: ${env.HTML_REPORT}"
                }
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    allowMissing         : false,
                    alwaysLinkToLastBuild: true,
                    keepAll              : true,
                    reportDir            : 'reports',
                    reportFiles          : 'security-report.html',
                    reportName           : 'Secret Leak Detection Report'
                ])
            }
        }

        stage('Fail-Fast Gate') {
            steps {
                script {
                    if (env.SCAN_EXIT_CODE == "1") {
                        error("""
                        ============================================================
                        ❌ SECURITY GATE FAILED — Secrets detected in the codebase!
                        Review the HTML report for full details and remediation steps.
                        Build blocked to prevent secret exposure.
                        ============================================================
                        """)
                    } else {
                        echo "✅ Security gate passed. No secrets detected."
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
        failure {
            echo "❌ Pipeline failed. Check the Secret Leak Detection Report for details."
        }
        success {
            echo "✅ Pipeline completed successfully. Repository is clean."
        }
    }
}
