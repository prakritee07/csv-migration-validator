
import pytest

from validator import compare_csv_files


def write_csv(path, content):
    path.write_text(content, encoding="utf-8")


def test_detects_added_removed_changed_and_unchanged_records(tmp_path):
    old_file = tmp_path / "old.csv"
    new_file = tmp_path / "new.csv"

    write_csv(
        old_file,
        "id,name,department,salary\n"
        "101,Asha,Finance,45000\n"
        "102,Bikash,IT,50000\n"
        "103,Nisha,HR,42000\n"
        "104,Rohan,Sales,40000\n",
    )

    write_csv(
        new_file,
        "id,name,department,salary\n"
        "101,Asha,Finance,47000\n"
        "102,Bikash,IT,50000\n"
        "104,Rohan,Sales,40000\n"
        "105,Sita,Legal,43000\n",
    )

    report = compare_csv_files(old_file, new_file)
    summary = report["summary"]

    assert summary["old_rows"] == 4
    assert summary["new_rows"] == 4
    assert summary["added_ids"] == 1
    assert summary["removed_ids"] == 1
    assert summary["changed_ids"] == 1
    assert summary["unchanged_ids"] == 2

    assert [record["id"] for record in report["added_records"]] == ["105"]
    assert [record["id"] for record in report["removed_records"]] == ["103"]

    changes = report["changed_records"][0]["changes"]
    assert changes["salary"] == {"old": "45000", "new": "47000"}


def test_detects_duplicate_ids(tmp_path):
    old_file = tmp_path / "old.csv"
    new_file = tmp_path / "new.csv"

    write_csv(
        old_file,
        "id,name\n"
        "101,Asha\n"
        "101,Another Asha\n",
    )

    write_csv(new_file, "id,name\n101,Asha\n")

    report = compare_csv_files(old_file, new_file)

    assert report["summary"]["duplicate_ids_in_old"] == ["101"]
    assert report["summary"]["duplicate_ids_in_new"] == []


def test_rejects_missing_id_column(tmp_path):
    old_file = tmp_path / "old.csv"
    new_file = tmp_path / "new.csv"

    write_csv(old_file, "name,department\nAsha,Finance\n")
    write_csv(new_file, "name,department\nAsha,Finance\n")

    with pytest.raises(ValueError, match="Required ID column"):
        compare_csv_files(old_file, new_file)


def test_rejects_blank_record_id(tmp_path):
    old_file = tmp_path / "old.csv"
    new_file = tmp_path / "new.csv"

    write_csv(old_file, "id,name\n,Asha\n")
    write_csv(new_file, "id,name\n101,Asha\n")

    with pytest.raises(ValueError, match="Missing ID"):
        compare_csv_files(old_file, new_file)


def test_reports_added_and_removed_columns(tmp_path):
    old_file = tmp_path / "old.csv"
    new_file = tmp_path / "new.csv"

    write_csv(old_file, "id,name,department\n101,Asha,Finance\n")
    write_csv(new_file, "id,name,location\n101,Asha,Kathmandu\n")

    report = compare_csv_files(old_file, new_file)

    assert report["schema_changes"]["columns_added_in_new"] == ["location"]
    assert report["schema_changes"]["columns_removed_in_new"] == ["department"]
