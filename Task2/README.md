# Task 2 — Poka-Yoke Automated CI/CD Build Gate

## Objective

This task implements a strict, fail-closed CI/CD security gate using GitHub Actions.

The purpose of the pipeline is to automatically validate code quality, run tests, detect hardcoded secrets, and identify vulnerable dependencies before a build can proceed.

The pipeline follows the Poka-Yoke principle by preventing known security and quality failures from progressing through the delivery process.

---

## Pipeline Checks

The GitHub Actions workflow performs the following checks:

1. **Automated Tests**
   - Runs the application's test suite using pytest.
   - A failed test causes the workflow to fail.

2. **Linting and Formatting**
   - Uses Ruff to detect Python code-quality issues.
   - Uses `ruff format --check .` to verify that Python files follow the expected formatting.
   - Linting or formatting failures cause the workflow to fail.

3. **Secret Scanning**
   - Uses Gitleaks to detect hardcoded API keys, access tokens, passwords, and other secrets.
   - If a secret is detected, the workflow fails immediately.

4. **Dependency Security Scanning**
   - Uses pip-audit to check Python dependencies for known security vulnerabilities.
   - Vulnerable dependencies cause the security gate to fail.

---

## Fail-Closed Security Gate

The workflow is designed so that security and quality checks must pass before the pipeline can be considered successful.

If any required check fails:

- The GitHub Actions job is marked as failed.
- The workflow does not report a successful build.
- Subsequent pipeline processing is blocked.
- A detected secret or security issue cannot silently pass through the gate.

This provides a fail-closed approach where the default behavior is to stop rather than allow a potentially unsafe build to continue.

---

## Secret Detection Demonstration

A test hardcoded secret was intentionally introduced into the application to verify the security gate.

Gitleaks detected the secret and reported:

- Secret type/rule: `stripe-access-token`
- Affected file: `app/app.py`
- GitHub Actions job: failed
- Leak detection result: failed

This demonstrates that the security gate is actively enforcing secret detection rather than only defining the scanner in the workflow.

Evidence:

`screenshots/task2-secret-detection-failed.png`

---

## Security Controls

The pipeline provides multiple layers of protection:

| Control | Tool | Failure Behavior |
|---|---|---|
| Automated testing | pytest | Pipeline fails |
| Code-quality checking | Ruff | Pipeline fails |
| Secret detection | Gitleaks | Pipeline fails |
| Dependency vulnerability scanning | pip-audit | Pipeline fails |

---

## Workflow

The security gate is defined in:

```text
.github/workflows/security-gate.yml
