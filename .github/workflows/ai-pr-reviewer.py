import os
import sys

import google.generativeai as genai
import requests

API_KEY = os.environ.get("AI_API_KEY")
PR_NUMBER = os.environ.get("PR_NUMBER")
REPO = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

print(f"🔍 DEBUG: PR: {PR_NUMBER}, REPO: {REPO}")

if not API_KEY:
    print("❌ CRITICAL: AI_API_KEY is missing! GitHub Secrets kontrol et.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_pr_diff():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
    }
    print(f"📥 Fetching diff from: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch diff: {response.status_code} - {response.text}")
        sys.exit(1)
    return response.text


def post_comment(comment):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    print(f"📤 Posting comment to: {url}")
    response = requests.post(url, headers=headers, json={"body": comment})
    if response.status_code != 201:
        print(f"❌ Failed to post comment: {response.status_code} - {response.text}")
        sys.exit(1)
    print("✅ Comment successfully posted!")


def analyze_diff(diff_text):
    if "world_universities_and_domains.json" not in diff_text:
        print(
            "⏭️ No changes in world_universities_and_domains.json detected. Skipping."
        )
        return None

    prompt = f"""
    You are an expert maintainer for an open-source global university database.
    Review the following git diff for a Pull Request:
    ```diff\n{diff_text}\n```
    Evaluate ONLY the newly added lines (starting with '+') against our STRICT rules:
    1. **Existence**: Is it a real university?
    2. **Schema**: Does it have `name`, `country`, `alpha_two_code`, `domains`, `web_pages`, `state-province`?
    3. **ROOT DOMAINS**: Ensure ONLY root domains are used.
    Format as a checklist. Conclude with "✅ PASSED" or "❌ FLAGGED".
    """
    try:
        print("🧠 Sending prompt to Gemini...")
        response = model.generate_content(prompt)
        print("✅ Gemini successfully responded.")
        return f"🤖 **AIOps Comprehensive PR Review**\n\n{response.text}\n\n---\n*Automated review check.*"
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    diff = get_pr_diff()
    if diff:
        report = analyze_diff(diff)
        if report:
            post_comment(report)
