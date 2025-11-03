import json
import io
import os

# Set your fine-tuning file name here.  The script assumes it lives in the same
# folder.  Feel free to point it at a different JSONL file exported from your
# own training dataset.
FILE_PATH = "5 fine tuning.jsonl"


def check_bom(path):
    """Check if file starts with UTF-8 BOM."""

    # Azure requires JSONL training files to include the UTF-8 BOM marker.  We
    # open the file in binary mode and read the first three bytes to confirm the
    # marker is present.
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

    # ``io.open`` with ``encoding='utf-8'`` guarantees we read text correctly on
    # every platform.  Each line in a JSONL file is a self-contained JSON object.
    with io.open(path, "r", encoding="utf-8") as f:
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


