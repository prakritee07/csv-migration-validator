
import argparse
import csv
import json
import sys
from pathlib import Path


def load_csv(file_path: Path, id_column: str):
    """Read a CSV file and validate its headers and record IDs."""
    records = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(f"{file_path}: CSV file is empty or has no header.")

        headers = [header.strip() for header in reader.fieldnames]

        if any(not header for header in headers):
            raise ValueError(f"{file_path}: Column names cannot be empty.")

        if len(headers) != len(set(headers)):
            raise ValueError(f"{file_path}: Duplicate column names found.")

        if id_column not in headers:
            raise ValueError(
                f"{file_path}: Required ID column '{id_column}' was not found."
            )

        for row in reader:
            if None in row:
                raise ValueError(
                    f"{file_path}: Too many columns near line {reader.line_num}."
                )

            record = {
                key.strip(): (value or "").strip()
                for key, value in row.items()
            }

            record_id = record.get(id_column, "")

            if not record_id:
                raise ValueError(
                    f"{file_path}: Missing ID near line {reader.line_num}."
                )

            records.append(record)

    return headers, records


def index_records(records, id_column):
    """Index records by ID and report duplicate IDs."""
    indexed = {}
    duplicates = set()

    for record in records:
        record_id = record[id_column]

        if record_id in indexed:
            duplicates.add(record_id)
        else:
            indexed[record_id] = record

    return indexed, sorted(duplicates)


def compare_csv_files(old_path: Path, new_path: Path, id_column="id"):
    """Compare two CSV files and return a structured migration report."""
    old_headers, old_rows = load_csv(old_path, id_column)
    new_headers, new_rows = load_csv(new_path, id_column)

    old_records, old_duplicates = index_records(old_rows, id_column)
    new_records, new_duplicates = index_records(new_rows, id_column)

    old_ids = set(old_records)
    new_ids = set(new_records)

    added_ids = sorted(new_ids - old_ids)
    removed_ids = sorted(old_ids - new_ids)
    matched_ids = sorted(old_ids & new_ids)

    old_columns = set(old_headers)
    new_columns = set(new_headers)

    added_columns = sorted(new_columns - old_columns)
    removed_columns = sorted(old_columns - new_columns)

    comparison_columns = sorted(
        (old_columns | new_columns) - {id_column}
    )

    changed_records = []
    unchanged_count = 0

    for record_id in matched_ids:
        old_record = old_records[record_id]
        new_record = new_records[record_id]
        field_changes = {}

        for column in comparison_columns:
            old_value = old_record.get(column, "")
            new_value = new_record.get(column, "")

            if old_value != new_value:
                field_changes[column] = {
                    "old": old_value,
                    "new": new_value,
                }

        if field_changes:
            changed_records.append({
                "id": record_id,
                "changes": field_changes,
            })
        else:
            unchanged_count += 1

    return {
        "old_file": str(old_path),
        "new_file": str(new_path),
        "id_column": id_column,
        "summary": {
            "old_rows": len(old_rows),
            "new_rows": len(new_rows),
            "old_unique_ids": len(old_ids),
            "new_unique_ids": len(new_ids),
            "matched_ids": len(matched_ids),
            "added_ids": len(added_ids),
            "removed_ids": len(removed_ids),
            "changed_ids": len(changed_records),
            "unchanged_ids": unchanged_count,
            "duplicate_ids_in_old": old_duplicates,
            "duplicate_ids_in_new": new_duplicates,
        },
        "schema_changes": {
            "columns_added_in_new": added_columns,
            "columns_removed_in_new": removed_columns,
        },
        "added_records": [
            {"id": record_id, "values": new_records[record_id]}
            for record_id in added_ids
        ],
        "removed_records": [
            {"id": record_id, "values": old_records[record_id]}
            for record_id in removed_ids
        ],
        "changed_records": changed_records,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compare old and new CSV exports for migration issues."
    )
    parser.add_argument("old_csv", type=Path, help="Path to the old CSV file")
    parser.add_argument("new_csv", type=Path, help="Path to the new CSV file")
    parser.add_argument(
        "--id-column",
        default="id",
        help="Column used to identify records (default: id)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("migration_report.json"),
        help="Where to save the JSON report",
    )

    args = parser.parse_args()

    try:
        report = compare_csv_files(
            args.old_csv,
            args.new_csv,
            args.id_column,
        )

        args.output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        summary = report["summary"]

        print("CSV Migration Validation Report")
        print("=" * 34)
        print(f"Old rows:       {summary['old_rows']}")
        print(f"New rows:       {summary['new_rows']}")
        print(f"Added IDs:      {summary['added_ids']}")
        print(f"Removed IDs:    {summary['removed_ids']}")
        print(f"Changed IDs:    {summary['changed_ids']}")
        print(f"Unchanged IDs:  {summary['unchanged_ids']}")
        print(f"Duplicate IDs in old file: {summary['duplicate_ids_in_old']}")
        print(f"Duplicate IDs in new file: {summary['duplicate_ids_in_new']}")
        print(f"Report saved to: {args.output}")

    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
