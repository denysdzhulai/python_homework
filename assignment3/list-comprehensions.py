# Task 3
import csv


def read_csv_to_list(filename):
    """Read CSV file and return as list of lists"""
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)


if __name__ == "__main__":
    print("=== List Comprehensions Practice ===")

    try:
        employees_data = read_csv_to_list('../csv/employees.csv')
        print(
            f"Successfully read {len(employees_data)} rows from employees.csv")

        if employees_data:
            print(f"Header: {employees_data[0]}")

        full_names = [f"{row[0]} {row[1]}" for row in employees_data[1:]]

        print(f"\nFull names list ({len(full_names)} employees):")
        for name in full_names:
            print(f"  {name}")

        # List comprehension to filter names containing the letter "e"
        names_with_e = [name for name in full_names if 'e' in name.lower()]

        print(f"\nNames containing 'e' ({len(names_with_e)} employees):")
        for name in names_with_e:
            print(f"  {name}")

    except FileNotFoundError:
        print("Error: Could not find '../csv/employees.csv'")
        print("Creating sample data for demonstration purposes...")

        # Sample data for demonstration
        sample_employees = [
            ['first_name', 'last_name', 'department'],
            ['John', 'Doe', 'Engineering'],
            ['Jane', 'Smith', 'Marketing'],
            ['Alice', 'Johnson', 'Sales'],
            ['Bob', 'Wilson', 'Engineering'],
            ['Carol', 'Brown', 'HR'],
            ['David', 'Davis', 'Finance'],
            ['Eve', 'Miller', 'Marketing']
        ]

        print(f"Sample data: {sample_employees[0]}")

        # List comprehension for full names (skip header)
        full_names = [f"{row[0]} {row[1]}" for row in sample_employees[1:]]

        print(f"\nFull names list:")
        for name in full_names:
            print(f"  {name}")

        # List comprehension for names with 'e'
        names_with_e = [name for name in full_names if 'e' in name.lower()]

        print(f"\nNames containing 'e':")
        for name in names_with_e:
            print(f"  {name}")
