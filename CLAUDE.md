# CLAUDE.md — Instructions for Claude Code

This file tells Claude Code everything it needs to know about this codebase.
Read this file before making any changes, suggestions, or improvements.

---

## What this project is

This repository contains Python scripts used in the **MRS Advanced AI Course** — a professional
training course for market researchers learning to use Python and AI APIs for personal automation.

**Audience:** Intelligent, professionally experienced people who are not necessarily programmers.
Some have basic Python familiarity; many have none at all.

**Purpose of the code:** To teach. Every script is a learning artefact, not just a working tool.
The code must be readable by a non-programmer. Comments are as important as the code itself.

**Instructor:** Karolyn Webb

---

## Repository structure

```
Code-for-MRS/
│
├── CLAUDE.md                        ← You are reading this
├── README.md                        ← Overview for participants
├── requirements.txt                 ← All dependencies
├── .env.example                     ← Template for API keys (no real keys)
│
├── 1_http_api_demo.py               ← Unauthenticated HTTP API, requests library
├── 2_openai_responses_api.py        ← First OpenAI API call
├── 3_openai_with_system_prompt.py   ← System prompts and parameters
├── 4_azure_agent.py                 ← Azure AI Foundry (legacy — see note below)
├── 5_check_ft.py                    ← Fine-tuning data validator (legacy)
├── 5_fine_tuning.jsonl              ← Example fine-tuning data
├── 5_validation_data.jsonl          ← Validation dataset
├── 6_qualitative_theming.py         ← Theme extraction from survey data
├── 6_Example_Qualitative.xlsx       ← Sample survey responses
├── 6_Example_Qualitative_Themed.xlsx← Output with themes added
│
├── 7_claude_api_demo.py             ← Claude API equivalent of Script 2
├── 8_open_text_categoriser.py       ← Categorisation + sentiment, OpenAI or Claude
│
└── USING_AI_CODING_AGENTS.md        ← Guide for participants using Claude Code / Codex
```

### Notes on legacy scripts

Scripts 4 and 5 were written for an earlier version of the course that used Azure AI Foundry.
They are kept in the repository for reference but are not part of the current course flow.
When suggesting improvements, treat them as lower priority than Scripts 1–3 and 6–8.

---

## Core principle: documentation is the product

For this codebase, **documentation is not optional and it is not secondary**.
The comments explain what the code does, why each decision was made, and what a
market researcher can learn from it.

When you improve or extend any script, apply these documentation rules without exception:

### Every script must have

1. **A module docstring at the top** — at least 15 lines covering:
   - What the script does
   - The market research use case it demonstrates
   - What a participant will learn from running it
   - How to install dependencies
   - How to run the script
   - Where to get API keys

2. **Section comments** — every logical group of code should have a comment block
   using this format:
   ```python
   # -----------------------------------------------------------------------
   # SECTION TITLE
   # Two or three lines explaining what this section does and why,
   # in plain English suitable for a non-programmer.
   # -----------------------------------------------------------------------
   ```

3. **Inline comments on anything non-obvious** — if a line of code might confuse
   a beginner, add a comment. This includes: list comprehensions, dictionary access,
   string formatting, any API-specific syntax.

4. **Parameter explanations** — wherever an API or function call uses named parameters,
   add a comment explaining what each parameter does. Example:
   ```python
   response = client.messages.create(
       model="claude-haiku-4-5",             # The model to use — Haiku is fast and cheap
       max_tokens=256,                       # Maximum length of the response
       system=system_prompt,                 # The AI's briefing / role
       messages=[{"role": "user", "content": user_message}]  # The conversation history
   )
   ```

5. **A "what just happened" comment after each major operation** — help the reader
   understand the flow:
   ```python
   # At this point, 'response' is a Python object containing the AI's reply,
   # usage statistics, and some metadata. We only need the text content.
   ```

6. **Teaching notes where relevant** — for concepts that participants often find confusing
   (JSON, environment variables, tokens, rate limits), add a teaching note:
   ```python
   # TEACHING NOTE: A "token" is roughly 0.75 words. The model charges per token,
   # so max_tokens controls both the response length and the cost of each API call.
   ```

### Functions and classes

Every function must have a docstring using this format:
```python
def categorise_response(response_text: str, provider: str) -> dict:
    """
    Send a single survey response to an AI model and receive a structured categorisation.

    This function handles the API call for both OpenAI and Claude. It sends the
    response text as a user message with a system prompt that instructs the model
    to return JSON in a specific format.

    Args:
        response_text (str): The raw survey response to categorise.
        provider (str): Which AI provider to use — either "openai" or "claude".

    Returns:
        dict: A dictionary with keys:
            - "category"  (str): One of the predefined category labels
            - "sentiment" (str): "Positive", "Neutral", or "Negative"
            - "reason"    (str): One sentence explaining the categorisation

    Raises:
        ValueError: If an unrecognised provider is specified.
        json.JSONDecodeError: If the AI returns a response that cannot be parsed as JSON.

    Example:
        >>> result = categorise_response("The pricing is too high", "claude")
        >>> result["category"]
        'Pricing & Value'
        >>> result["sentiment"]
        'Negative'
    """
```

---

## Code style guide

### Formatting
- Use 4-space indentation (no tabs)
- Maximum line length: 90 characters
- One blank line between logical sections within a function
- Two blank lines between functions
- Two blank lines between the docstring and the first import

### Naming
- Variables: `snake_case` (e.g. `response_text`, `api_key`, `survey_responses`)
- Constants (things that don't change): `ALL_CAPS` (e.g. `PROVIDER`, `CATEGORIES`, `MAX_TOKENS`)
- Functions: `snake_case` verbs (e.g. `load_responses()`, `call_claude_api()`, `export_to_excel()`)

### Error handling
Every API call must be wrapped in a try/except block with a helpful error message.
The error message should tell the user what went wrong and what to do about it.
```python
try:
    result = call_api(prompt)
except anthropic.AuthenticationError:
    print("❌  Your API key was rejected. Check that ANTHROPIC_API_KEY is set correctly in your .env file.")
    exit()
except anthropic.RateLimitError:
    print("⚠️  You've hit the rate limit. Wait a moment and try again.")
    exit()
```

### API keys and secrets
- API keys must NEVER appear in script files — always load from `.env` via `python-dotenv`
- Always check that the key was loaded and print a clear, friendly error if it wasn't
- The `.env` file must be in `.gitignore` — never commit real keys

### Output formatting
Scripts should print clear, formatted output so participants can see what's happening:
```python
print("=" * 60)
print("  Script Name — What it does")
print("=" * 60)
print(f"\nProcessing {len(items)} items...\n")
# ... work ...
print("✅  Done!")
```

Use emoji sparingly and consistently: ✅ for success, ❌ for errors, ⚠️ for warnings, 📊 for stats.

---

## Improvement priorities

When Claude Code is asked to improve this codebase, work through these priorities in order.

### Priority 1 — Documentation completeness
Check every script against the documentation rules above. Fill gaps.
- Every script needs a full module docstring
- Every function needs a complete docstring with Args, Returns, Raises, Example
- Every section needs a comment block
- All API parameters need inline explanations

### Priority 2 — Robustness and error handling
- All API calls should handle common errors (auth, rate limit, network, JSON parse)
- Scripts that load files should handle FileNotFoundError gracefully
- Scripts that write files should confirm success and print the output path

### Priority 3 — Beginner accessibility
- Remove or explain any advanced Python constructs (list comprehensions, `*args`, decorators)
- Replace one-liners that are hard to read with multi-line equivalents
- Add "TEACHING NOTE" comments wherever a concept might be new to participants

### Priority 4 — Alignment across scripts
- Scripts 2 and 7 should use parallel structure (same sections, same variable names where possible)
  so participants can compare OpenAI and Claude side-by-side
- Scripts that produce Excel output should use the same formatting and column naming conventions
- All scripts should load environment variables the same way (via `load_dotenv()` + `os.getenv()`)

### Priority 5 — New features (only if specifically requested)
Do not add new features without being asked. The scripts are intentionally simple.
Complexity is the enemy of teaching. If you are asked to add a feature, add it
in the simplest possible way and document it fully.

---

## What not to do

- **Do not refactor into classes** unless specifically asked. Classes add cognitive overhead
  for beginners. Keep scripts procedural (top-to-bottom flow) wherever possible.

- **Do not add type annotations throughout** — a few on function signatures is fine
  (it helps readability), but annotating every variable makes the code look intimidating.

- **Do not use advanced libraries** without checking first. The requirements list is
  intentionally minimal. Adding libraries increases setup complexity for participants.

- **Do not remove comments** — even if you think a comment is obvious. What is obvious
  to you may not be obvious to a market researcher reading Python for the first time.

- **Do not use f-strings with complex expressions inside** — break them into variables first.
  ```python
  # ❌ Hard to read
  print(f"Processed {len([r for r in results if r['status'] == 'ok'])} responses.")

  # ✅ Easy to read
  successful = [r for r in results if r["status"] == "ok"]
  print(f"Processed {len(successful)} responses.")
  ```

- **Do not rename existing files** without discussing it first. Participants may have
  these filenames in their notes.

---

## Market research context

The scripts in this repository deal with the following market research tasks.
Understanding this context helps you write better comments and suggest relevant improvements.

**Qualitative analysis:** Open-ended survey responses (verbatims) are a core output of
qual research. Researchers spend hours reading, grouping, and theming these responses.
AI can do a first pass in seconds, dramatically accelerating the workflow.

**Quantitative coding:** Survey data often contains open-text questions alongside
structured responses. Coding (assigning categories) is traditionally done manually
and is time-consuming and inconsistent. AI categorisation is faster and more consistent
(though it should always be reviewed).

**Reporting:** Researchers write similar reports repeatedly — summarising findings,
drafting executive summaries, pulling key quotes. AI can generate drafts that researchers
then refine, saving significant time.

**The human role:** AI does not replace the researcher's judgement, domain knowledge,
or relationship with the client. It handles the repetitive, time-consuming parts so the
researcher can focus on insight, interpretation, and storytelling.

---

## Working with GitHub in this project

This repository is hosted at: **https://github.com/KarolynW/Code-for-MRS**

Participants clone or download the repository to get the scripts onto their machine.
GitHub is also used during the course to demonstrate:
- How to clone a repository
- How to use GitHub Copilot for code review
- How to commit changes and push them back

### When making improvements via Claude Code

If you are running inside a local clone of this repository:

1. Work in a new branch, not directly on `main`:
   ```bash
   git checkout -b improve/documentation
   ```

2. Make your changes in small, logical commits:
   ```bash
   git add 7_claude_api_demo.py
   git commit -m "docs: add full module docstring and section comments to Script 7"
   ```

3. When done, push the branch and open a pull request so Karolyn can review
   the changes before they are merged:
   ```bash
   git push origin improve/documentation
   ```

### Commit message format

Use this format for all commits in this repository:
```
<type>: <short description>

Types:
  docs    — documentation improvements
  fix     — bug fixes
  feat    — new features
  style   — formatting, no logic changes
  refactor — restructuring without changing behaviour
```

---

## Suggested improvement tasks

These are ready-to-go tasks you can be asked to carry out. Each is scoped to be
achievable in a single Claude Code session.

### Task A — Full documentation pass on Script 7
```
Review 7_claude_api_demo.py against the documentation standards in CLAUDE.md.
Add any missing section comments, improve the module docstring, and add inline
comments on every API parameter. Do not change any logic.
```

### Task B — Add error handling to all scripts
```
Review all scripts (1–3, 6–8) and add proper try/except blocks for API errors,
file errors, and JSON parse errors. Follow the error handling style in CLAUDE.md.
Print helpful, friendly error messages. Do not change the core logic.
```

### Task C — Make Scripts 2 and 7 structurally parallel
```
Compare 2_openai_responses_api.py and 7_claude_api_demo.py.
Make sure they have the same section structure (same headings, same order),
the same variable names where the concepts are equivalent, and the same
output formatting. This makes it easy for participants to compare them side-by-side.
```

### Task D — Add a requirements check to every script
```
Add a short function at the top of each script that checks whether the required
libraries are installed before trying to import them. If a library is missing,
print a clear install instruction and exit cleanly. Example:
  "❌  Missing library: anthropic. Run: pip install anthropic"
```

### Task E — Create a new script: automated reporting
```
Create a new script called 9_report_generator.py.
It should load the output of Script 8 (categorised responses Excel file),
call the Claude API to generate a short executive summary report,
and save the report as a text file.
Follow all documentation standards in CLAUDE.md.
The script should work as a standalone tool for market researchers.
```

### Task F — Update the README
```
Update README.md to reflect the current state of the repository.
Include: what each script does, how to get set up, where to get API keys,
and a note about Scripts 4 and 5 being legacy. Follow the same friendly,
non-intimidating tone as the rest of the course materials.
```

---

## Quick reference: API client setup

Use these patterns consistently across all scripts.

### Claude (Anthropic)
```python
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-haiku-4-5",             # Fast, cost-effective — good for classification
    # model="claude-opus-4-7",           # More powerful — good for complex analysis
    max_tokens=1024,
    system="Your system prompt here.",
    messages=[
        {"role": "user", "content": "Your user message here."}
    ]
)

result_text = response.content[0].text
```

### OpenAI
```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4.1-mini",           # Cost-effective — good for classification
    # model="gpt-4.1",              # More powerful — good for complex analysis
    instructions="Your system prompt here.",
    input="Your user message here.",
)

result_text = response.output_text
```

---

*This file was created for the MRS Advanced AI Course.*
*Tutor: Karolyn Webb | Repository: https://github.com/KarolynW/Code-for-MRS*

