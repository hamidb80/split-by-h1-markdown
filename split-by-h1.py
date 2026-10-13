import sys
from pathlib import Path
from pathvalidate import sanitize_filename


input_path = Path(sys.argv[1])
output_dir = input_path.parent
output_dir.mkdir(parents=True, exist_ok=True)

suffix = input_path.suffix  # e.g. ".md"

current_filename = None
current_lines = []


def flush():
    if current_filename is None:
        return

    safe_name = sanitize_filename(current_filename.strip())
    out_file = output_dir / f"{safe_name}{suffix}"

    with open(out_file, "w", encoding="utf-8") as out:
        content = "\n".join(current_lines).rstrip() + "\n"
        out.write(content)


with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

for line in text.splitlines():
    if line.startswith("# "):
        flush()
        current_filename = line[2:].strip()
        current_lines = []
    else:
        current_lines.append(line)

flush()