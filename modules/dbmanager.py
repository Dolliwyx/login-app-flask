import csv

# Define the CSV file path
csv_file = "users.csv"


def create_record(record):
    """
    Create a new record in the CSV file.
    Args:
        record (dict): A dictionary representing a record with keys corresponding to the CSV headers.
    """
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=record.keys())
        writer.writerow(record)


def read_records():
    """
    Read all records from the CSV file.
    Returns:
        list: A list of dictionaries representing all records in the CSV file.
    """
    records = []
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    return records


def update_record(record_to_update, updated_record):
    """
    Update a record in the CSV file.
    Args:
        record_to_update (dict): A dictionary representing the record to be updated.
        updated_record (dict): A dictionary representing the updated record.
    """
    records = read_records()
    updated_records = []

    for record in records:
        if record == record_to_update:
            updated_records.append(updated_record)
        else:
            updated_records.append(record)

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=updated_records[0].keys())
        writer.writeheader()
        writer.writerows(updated_records)


def delete_record(record_to_delete):
    """
    Delete a record from the CSV file.
    Args:
        record_to_delete (dict): A dictionary representing the record to be deleted.
    """
    records = read_records()
    updated_records = [
        record for record in records if record != record_to_delete]

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=updated_records[0].keys())
        writer.writeheader()
        writer.writerows(updated_records)
