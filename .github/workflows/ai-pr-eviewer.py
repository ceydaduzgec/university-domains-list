import os
import requests
import google.generativeai as genai

API_KEY = os.environ.get("AI_API_KEY")
PR_NUMBER = os.environ.get("PR_NUMBER")
REPO = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_pr_diff():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    return response.text

def post_comment(comment):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    requests.post(url, headers=headers, json={"body": comment})

def analyze_diff(diff_text):
    if "world_universities_and_domains.json" not in diff_text:
        return "No changes in the university database detected."

    prompt = f"""
    You are an expert maintainer for an open-source global university database.
    Review the following git diff for a Pull Request:

    ```diff
    {diff_text}
    ```

    Evaluate ONLY the newly added lines (starting with '+') against our STRICT rules:

    1. **Existence & Accuracy**: Is the institution a real, officially recognized higher education institution? Are the official website and domain correct?
    2. **Schema Completeness**: Does the added JSON block include all required fields exactly as named: `name`, `country`, `alpha_two_code` (must be a valid ISO 3166-1 alpha-2 code), `domains` (array), `web_pages` (array), and `state-province` (can be null)?
    3. **ROOT DOMAINS ONLY (CRITICAL)**: Ensure `domains` contain ONLY root domains (e.g., 'usc.edu', 'itu.edu.tr'). Any subdomains (e.g., 'cs.usc.edu', 'ogr.itu.edu.tr') must be heavily penalized.
    4. **Formatting**: Is it a valid JSON format?

    Format your output as a clear checklist. Conclude your review with either:
    "✅ PASSED" (if everything is perfect) OR
    "❌ FLAGGED: [Reason]" (if any rule is violated, schema is missing, or subdomains are used).
    """

    try:
        response = model.generate_content(prompt)
        report = f"🤖 **AIOps Comprehensive PR Review**\n\n{response.text}\n\n---\n*Note: This is an automated check enforcing the CONTRIBUTING.md guidelines. The maintainer has the final say.*"
        return report
    except Exception as e:
        return f"🤖 AI Reviewer encountered an error: {str(e)}"

if __name__ == "__main__":
    diff = get_pr_diff()
    if diff:
        review_comment = analyze_diff(diff)
        post_comment(review_comment)