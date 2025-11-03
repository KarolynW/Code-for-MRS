import json
import io
import os

# Set your fine-tuning file name here
FILE_PATH = "5 fine tuning.jsonl"

def check_bom(path):
    """Check if file starts with UTF-8 BOM."""
    with open(path, "rb") as f:
        start = f.read(3)
        if start == b"\xef\xbb\xbf":
            return True
        else:
            return False

def load_jsonl(path):
    """Validate each JSON line for structure and content."""
    valid = 0
    errors = []
    with io.open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append((i, f"JSON decode error: {e}"))
                continue

            msgs = obj.get("messages")
            if not isinstance(msgs, list):
                errors.append((i, "missing or invalid 'messages' list"))
                continue

            roles = {m.get("role") for m in msgs if isinstance(m, dict)}
            if not {"system", "user", "assistant"}.issubset(roles):
                errors.append((i, f"missing one of required roles, found: {roles}"))
                continue

            if not all(isinstance(m.get("content"), str) for m in msgs):
                errors.append((i, "non-string content detected"))
                continue

            valid += 1
    return valid, errors

if __name__ == "__main__":
    print(f"🔍 Checking file: {FILE_PATH}\n")

    # --- Encoding & BOM check ---
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


