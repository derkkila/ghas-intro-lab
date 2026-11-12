# GitHub Advanced Security intro lab

A tiny, intentionally insecure Python web app. Use it to see GitHub Advanced
Security (GHAS) work in about 10 minutes, using only your browser.

Everything in this lab uses features that are **free on public repositories**,
so you do not need a paid plan, a license, or a credit card. You do need a
GitHub account.

> Do not deploy this app anywhere. It is broken on purpose.

## Before you start (3 minutes, do this first)

The first CodeQL scan takes a few minutes, so kick it off before anything else.

1. At the top of this page click **Use this template**, then **Create a new repository**.
2. Owner: your personal account. Repository name: `ghas-lab`. Visibility: **Public** (this is what makes the security features free).
3. Click **Create repository**.
4. In your new repository open **Settings**, then **Advanced Security** in the left sidebar (under Security).
   - Under **Code scanning**, next to **CodeQL analysis**, click **Set up**, choose **Default**, then **Enable CodeQL**.
   - Under **Dependabot**, make sure **Dependabot alerts** is enabled. Click **Enable** if it is not.
   - Under **Secret Protection**, make sure **Secret Protection** and **Push protection** are both enabled. Click **Enable** on each if it is not. (Your account already blocks secrets on public repos, but the repository setting is what records the alert you will look for in Exercise 1.)

You can watch the CodeQL run under the **Actions** tab. Carry on with the
exercises while it runs.

## Exercise 1: push protection stops a leaked token (3 minutes)

1. Open the **Code** tab. Click **Add file**, then **Create new file**.
2. Name the file `config/credentials.yml`.
3. Paste the line below. It is an inactive token that GitHub publishes for
   training. Delete the `<REMOVE_ME>` text so the token is one unbroken string.

   ```yaml
   github_token: github_pat_<REMOVE_ME>11A4YXR6Y0v36CYFkuT5I1_ZRWX91c8k0waSN6x7AiVJ6zZ9ZHUQXBblBqFQpKd23V6CL7MWMPopnmBxzn
   ```

4. Click **Commit changes...** and commit directly to `main`.
   Instead of saving, GitHub shows a push protection dialog. Read it: it names
   the secret type and the exact file and line.
5. Pretend you have a legitimate reason. Choose **It's used in tests**, click
   **Allow secret**, then commit again. This time it goes through.
6. Open the **Security** tab, then **Secret scanning**. Switch the filter from
   Open to **Closed**. The alert is there, resolved as "used in tests", with your
   name on the bypass.

What you saw: detection at push time, a forced decision with a reason, and an
audit trail a security team can review. In a company, that bypass can also
require approval from someone else (delegated bypass).

## Exercise 2: Dependabot finds vulnerable packages (3 minutes)

1. Open **Security**, then **Dependabot**. You should see several alerts for
   packages pinned in `requirements.txt`. If the list is still empty, GitHub is
   still indexing the new repository; do Exercise 3 first and come back.
2. Open the **Critical** alert for `PyYAML`. Notice the severity, the CVE, the
   patched version, and the file it came from.
3. Click **Create Dependabot security update**. Dependabot opens a pull request
   that bumps the version. Open the **Pull requests** tab to see it.

What you saw: GitHub already knows what your app depends on, matches it against
a curated advisory database, and can write the fix as a pull request.

## Exercise 3: CodeQL finds a SQL injection and Copilot proposes a fix (4 minutes)

1. Open **Security**, then **Code scanning**. If it is empty, the scan is still
   running. Check the **Actions** tab, then come back.
2. Open the alert **SQL query built from user-controlled sources**.
3. Click **Show paths**. Follow the flow: text from the URL (`request.args`)
   is pasted into a database query. That is a SQL injection.
4. Click **Generate fix**. Copilot Autofix reads the code and proposes a
   change, usually a parameterized query, with an explanation.
5. Click **Commit to new branch**, then open the pull request. CodeQL runs again
   on the pull request and confirms the alert is gone.
6. Look at the other alerts: a path traversal in `/notes` and Flask running in
   debug mode.

What you saw: the scanner understands data flow, not just text patterns, and
the fix arrives as a pull request instead of a line in a report.

## Clean up

Delete the repository when you are done: **Settings**, scroll to the bottom,
**Delete this repository**. Or keep it and explore.

## What is in this repository

| Path | Purpose |
| --- | --- |
| `app/app.py` | Flask app with three deliberate flaws: SQL injection, path traversal, debug mode |
| `requirements.txt` | Old versions of popular packages with published CVEs |

## Going further

- [GitHub Skills: Introduction to secret scanning](https://github.com/skills/introduction-to-secret-scanning)
- [GitHub Skills: Introduction to CodeQL](https://github.com/skills/introduction-to-codeql)
- [GitHub Skills: Secure your repository supply chain](https://github.com/skills/secure-repository-supply-chain)
- [Docs: About GitHub Advanced Security](https://docs.github.com/enterprise-cloud@latest/get-started/learning-about-github/about-github-advanced-security)
