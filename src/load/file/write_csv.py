import csv
from pathlib import Path

def write_csv(file_path: Path, data: list[dict]):
    if not data:
        print(f"⚠️ No data to write: {file_path}")
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing {len(data)} records to {file_path}")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=data[0].keys()
        )
        writer.writeheader()
        writer.writerows(data)
