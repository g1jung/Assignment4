import csv
import random

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Morning", "Afternoon", "Evening"]
MAX_SHIFTS_PER_EMPLOYEE = 5
MIN_EMPLOYEES_PER_SHIFT = 2

# Employee class
class Employee:
    def __init__(self, name, preferences=None):
        self.name = name
        self.preferences = preferences if preferences else ["None"] * 7
        self.assigned_days = 0
        self.assigned_shifts = {}  # day -> shift

# Read input.csv
def read_input(file_path):
    employees = []
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Name"]
            preferences = [row[day] for day in DAYS]
            employees.append(Employee(name, preferences))
    return employees

# Write output.csv
def write_output(employees, output_path):
    with open(output_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Employee"] + DAYS)
        for emp in employees:
            row = [emp.name]
            for day in DAYS:
                row.append(emp.assigned_shifts.get(day, ""))
            writer.writerow(row)

# Assign shifts
def assign_shifts(employees):
    shift_assignments = [{shift: [] for shift in SHIFTS} for _ in range(7)]

    # Add extra employees at the beginning
    extra_names = ["Chris", "Liz", "Ash", "Luna", "Beth", "Jeff", "Dave", "Joe"]
    for name in extra_names:
        employees.append(Employee(name))

    for day_index, day in enumerate(DAYS):
        random.shuffle(employees)

        # Step 1: Collect preferences
        preferred_map = {shift: [] for shift in SHIFTS}
        for emp in employees:
            if emp.assigned_days >= MAX_SHIFTS_PER_EMPLOYEE or day in emp.assigned_shifts:
                continue
            pref = emp.preferences[day_index]
            if pref in SHIFTS:
                preferred_map[pref].append(emp)

        # Step 2: Assign preferred employees to their preferred shifts
        for shift in SHIFTS:
            shift_list = shift_assignments[day_index][shift]
            for emp in preferred_map[shift]:
                if emp.assigned_days < MAX_SHIFTS_PER_EMPLOYEE and day not in emp.assigned_shifts:
                    if len(shift_list) < MIN_EMPLOYEES_PER_SHIFT:
                        shift_list.append(emp.name)
                        emp.assigned_shifts[day] = shift
                        emp.assigned_days += 1

        # Step 3: Fill under-assigned shifts
        for shift in SHIFTS:
            shift_list = shift_assignments[day_index][shift]
            while len(shift_list) < MIN_EMPLOYEES_PER_SHIFT:
                eligible = [
                    emp for emp in employees
                    if emp.assigned_days < MAX_SHIFTS_PER_EMPLOYEE and
                    day not in emp.assigned_shifts and
                    emp.name not in shift_list
                ]
                if not eligible:
                    break
                chosen = random.choice(eligible)
                shift_list.append(chosen.name)
                chosen.assigned_shifts[day] = shift
                chosen.assigned_days += 1

    return employees

# Main execution
if __name__ == "__main__":
    input_path = "input.csv"          # Input file in same directory
    output_path = "output.csv"        # Output file

    employees = read_input(input_path)
    scheduled_employees = assign_shifts(employees)
    write_output(scheduled_employees, output_path)
    print("✅ Final schedule written to output.csv")
