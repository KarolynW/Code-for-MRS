"""Script 5: Fine-Tuning JSONL File Validator.

This script checks whether a JSONL (JSON Lines) file is correctly formatted for
upload to Azure AI Foundry's fine-tuning service.  It catches common mistakes
before you waste time uploading a broken dataset.

Market research use case
------------------------
Fine-tuning lets you train a model on your own examples so it learns to respond
in a particular style or domain — for instance, answering market research
methodology questions in the voice of your brand or team.  Before Azure will
accept a training file it must meet strict formatting requirements.  Running
this validator first saves time and avoids frustrating upload errors.

What you will learn from this script
-------------------------------------
* What a JSONL file is and why it is used for fine-tuning.
* How Python reads and validates structured data line-by-line.
* What ``UTF-8 with BOM`` encoding means and why Azure requires it.
* How to write a validation loop that collects all errors before stopping,
  so you can see and fix every problem at once.

How to install dependencies
----------------------------
No extra packages are needed — this script uses only Python's built-in
``json``, ``io``, and ``os`` modules, which are available without ``pip install``.

How to run the script
---------------------
1. Open this repository folder in VS Code.
2. Click ``5_check_ft.py`` in the Explorer panel.
3. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) to run without debugging.
4. The output will tell you whether the file is ready to upload to Azure.

What the script checks
-----------------------
1. **File encoding** — Azure requires UTF-8 with BOM (Byte Order Mark).
2. **JSON validity** — every line must be parseable as valid JSON.
3. **Message structure** — each example must have a ``messages`` list.
4. **Required roles** — each example must include ``system``, ``user``, and
   ``assistant`` messages.
5. **Content types** — all message content must be plain strings, not nested
   objects or numbers.

TEACHING NOTE: What is a JSONL file?
--------------------------------------
A regular JSON file wraps everything in a single object or array.
A JSONL (JSON Lines) file stores one complete JSON object on each line, with
no commas between lines.  This makes it easy to process huge datasets one row
at a time without loading everything into memory at once.

Example of one valid training example in JSONL format::

    {"messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is a sample size?"},
        {"role": "assistant", "content": "A sample size is the number of people..."}
    ]}

TEACHING NOTE: What is a BOM?
-------------------------------
BOM stands for Byte Order Mark.  It is an invisible marker at the very start of
a text file that tells software "this file is encoded in UTF-8".  Some tools
add it automatically; others do not.  Azure AI Foundry requires it.  In
Notepad on Windows you can save a file with BOM by choosing "UTF-8 with BOM"
from the encoding dropdown.  In VS Code, use the "Save with Encoding" command
from the Command Palette (Ctrl+Shift+P).

Note: Scripts 4 and 5 are legacy examples from an earlier version of the
course that used Azure AI Foundry.  They are kept for reference.
"""


import json
import io
import os

# -----------------------------------------------------------------------
# CONFIGURATION
# Set the path to the JSONL file you want to validate.  By default the
# script checks the sample training file that ships with the course.
# Change this path to point at your own dataset when you are ready.
# -----------------------------------------------------------------------
FILE_PATH = "5_fine_tuning.jsonl"


def check_bom(path: str) -> bool:
    """Check whether a file begins with a UTF-8 Byte Order Mark (BOM).

    Azure AI Foundry requires fine-tuning files to be encoded as UTF-8 with
    BOM.  The BOM is a special three-byte sequence at the very beginning of the
    file: ``0xEF 0xBB 0xBF``.  We open the file in binary mode so we can
    inspect the raw bytes before any text decoding happens.

    Args:
        path (str): Path to the file to check.

    Returns:
        bool: ``True`` if the file starts with a UTF-8 BOM, ``False`` otherwise.

    Example:
        >>> has_bom = check_bom("5_fine_tuning.jsonl")
        >>> print("BOM found:" , has_bom)
        BOM found: True
    """

    # Open in binary ("rb") mode so Python doesn't strip or alter the raw bytes.
    with open(path, "rb") as f:
        start = f.read(3)            # read exactly the first three bytes
        if start == b"\xef\xbb\xbf":
            return True
        else:
            return False


def load_jsonl(path: str) -> tuple:
    """Validate each line of a JSONL file for Azure fine-tuning requirements.

    Reads the file line by line and checks every example against five rules:
    valid JSON, a ``messages`` list, the required roles (system, user, assistant),
    and string-typed content fields.  All errors are collected before returning
    so you can see and fix every problem in one go.

    Args:
        path (str): Path to the ``.jsonl`` file to validate.

    Returns:
        tuple: A two-element tuple ``(valid_count, errors)`` where:
            - ``valid_count`` (int): Number of examples that passed all checks.
            - ``errors`` (list): A list of ``(line_number, message)`` tuples
              describing every problem found.

    Example:
        >>> valid, errors = load_jsonl("5_fine_tuning.jsonl")
        >>> print(f"{valid} valid examples, {len(errors)} errors")
        73 valid examples, 0 errors
    """

    valid = 0
    errors = []

    # ``utf-8-sig`` automatically strips the UTF-8 BOM from the first line if
    # one is present.  Using plain ``utf-8`` would leave the BOM character inside
    # the first JSON string and cause a spurious parse error on line 1.
    with io.open(path, "r", encoding="utf-8-sig") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                # Skip blank lines quietly—they are allowed but contain no data.
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                # If the JSON structure is broken we record which line failed so
                # the analyst can fix it quickly.
                errors.append((i, f"JSON decode error: {e}"))
                continue

            msgs = obj.get("messages")
            if not isinstance(msgs, list):
                errors.append((i, "missing or invalid 'messages' list"))
                continue

            # Convert roles into a set so we can check all required roles are
            # present, regardless of order or duplicates.
            roles = {m.get("role") for m in msgs if isinstance(m, dict)}
            if not {"system", "user", "assistant"}.issubset(roles):
                errors.append((i, f"missing one of required roles, found: {roles}"))
                continue

            # Azure expects plain-text ``content`` fields.  This test catches
            # accidental nested objects or numbers.
            if not all(isinstance(m.get("content"), str) for m in msgs):
                errors.append((i, "non-string content detected"))
                continue

            valid += 1

    return valid, errors


if __name__ == "__main__":
    print(f"🔍 Checking file: {FILE_PATH}\n")

    # --- Encoding & BOM check ---
    # ``os.path.getsize`` lets us report the overall file size, which is helpful
    # when you need to stay within Azure's upload limits.
    size_bytes = os.path.getsize(FILE_PATH)
    size_mb = size_bytes / (1024 * 1024)
    has_bom = check_bom(FILE_PATH)

    print(f"File size: {size_mb:.2f} MB")
    print(f"BOM present: {'✅ Yes (UTF-8 with BOM)' if has_bom else '❌ No (save with UTF-8 BOM required)'}")

    # --- JSONL validation ---
    valid, errors = load_jsonl(FILE_PATH)
    print(f"\n✅ Valid examples: {valid}")
    if errors:
        print(f"\n❌ {len(errors)} issues found:")
        for ln, msg in errors[:15]:
            print(f"  Line {ln}: {msg}")
    else:
        print("\n🎉 All examples are valid JSONL.")

    # --- Recommendation ---
    if not has_bom:
        print("\n⚠️ Recommendation: Re-save the file using UTF-8 with BOM encoding before uploading to Azure Foundry.")
    elif valid < 10:
        print("\n⚠️ Warning: Fewer than 10 examples; Azure will reject this for fine-tuning.")
    else:
        print("\n✅ File passes validation and is suitable for Azure fine-tuning upload.")


