# Red Team Console

A dual-model test harness for evaluating LLM resistance to jailbreaks and prompt injection.

## Team Structure & Ownership
This project is maintained by a team of 4 contributors split into two pairs:
- **Injection Pair:** Focuses on prompt injection vectors.
- **Jailbreak Pair:** Focuses on jailbreak attempts and persona overrides.

Folder ownership is defined in `CODEOWNERS`. The cross-pair review process ensures that the Jailbreak pair reviews Injection cases, and vice versa.

## Repository Layout
- `redteam_console.py`: The Streamlit app for testing prompts against models.
- `test_cases/`: JSON test cases organized by category (`injection/` and `jailbreak/`).
- `schema/`: JSON Schema definitions for our test cases.
- `docs/`: Documentation, including our scoring rubric.
- `.github/`: Issue templates, PR templates, and GitHub Actions workflows.

## Setup & Run Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit console:
   ```bash
   streamlit run redteam_console.py
   ```

## Configuration
Before running the console, copy `.env.example` to `.env` and fill in your real credentials. **Never commit the `.env` file or share it outside the team, including with AI coding tools.**
