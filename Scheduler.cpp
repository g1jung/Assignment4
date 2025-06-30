#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <random>

using namespace std;

const vector<string> days = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };
const vector<string> shifts = { "Morning", "Afternoon", "Evening" };
const int MAX_SHIFTS_PER_EMPLOYEE = 5;
const int MIN_EMPLOYEES_PER_SHIFT = 2;

struct Employee {
    string name;
    vector<string> preferences;
    int assignedDays = 0;
    map<string, string> assignedShifts;
};

map<string, vector<string>> shiftAssignments[7]; // per day: shift -> list of employee names

void readInput(vector<Employee>& employees, set<string>& existingNames) {
    ifstream file("input.csv");
    string line;
    getline(file, line); // skip header

    while (getline(file, line)) {
        stringstream ss(line);
        string cell, name;
        getline(ss, name, ',');
        if (name.empty()) continue;
        existingNames.insert(name);

        Employee emp;
        emp.name = name;
        for (int i = 0; i < 7; ++i) {
            getline(ss, cell, ',');
            emp.preferences.push_back(cell);
        }
        employees.push_back(emp);
    }
}

void assignShifts(vector<Employee>& employees) {
    random_device rd;
    mt19937 gen(rd());

    // Add backup staff at the beginning
    vector<string> extraNames = { "Chris", "Liz", "Ash", "Luna", "Beth", "Jeff", "Dave", "Joe" };
    for (const string& name : extraNames) {
        Employee newEmp;
        newEmp.name = name;
        newEmp.preferences = vector<string>(7, "None");
        employees.push_back(newEmp);
    }

    for (int day = 0; day < 7; ++day) {
        shuffle(employees.begin(), employees.end(), gen); // shuffle to mix daily order

        map<string, vector<Employee*>> shiftMap;
        for (const auto& shift : shifts)
            shiftMap[shift] = {};

        // Collect preferences (even if "None")
        for (auto& emp : employees) {
            if (emp.assignedDays >= MAX_SHIFTS_PER_EMPLOYEE ||
                emp.assignedShifts.count(days[day])) continue;

            string pref = emp.preferences[day];
            if (find(shifts.begin(), shifts.end(), pref) != shifts.end()) {
                shiftMap[pref].push_back(&emp);
            }
        }

        // Assign preferred shifts first
        for (const auto& shift : shifts) {
            auto& shiftList = shiftAssignments[day][shift];
            for (auto* emp : shiftMap[shift]) {
                if (emp->assignedDays < MAX_SHIFTS_PER_EMPLOYEE &&
                    emp->assignedShifts.count(days[day]) == 0 &&
                    shiftList.size() < MIN_EMPLOYEES_PER_SHIFT) {

                    shiftList.push_back(emp->name);
                    emp->assignedShifts[days[day]] = shift;
                    emp->assignedDays++;
                }
            }
        }

        // Fill shifts to at least 2 employees
        for (const auto& shift : shifts) {
            auto& shiftList = shiftAssignments[day][shift];
            while (shiftList.size() < MIN_EMPLOYEES_PER_SHIFT) {
                vector<Employee*> eligible;
                for (auto& emp : employees) {
                    if (emp.assignedDays < MAX_SHIFTS_PER_EMPLOYEE &&
                        emp.assignedShifts.count(days[day]) == 0 &&
                        find(shiftList.begin(), shiftList.end(), emp.name) == shiftList.end()) {

                        eligible.push_back(&emp);
                    }
                }

                if (eligible.empty()) break;
                shuffle(eligible.begin(), eligible.end(), gen);
                Employee* chosen = eligible.front();
                shiftList.push_back(chosen->name);
                chosen->assignedShifts[days[day]] = shift;
                chosen->assignedDays++;
            }
        }
    }
}


void writeOutput(const vector<Employee>& employees) {
    ofstream out("output.csv");
    out << "Employee";
    for (const auto& day : days)
        out << "," << day;
    out << endl;

    for (const auto& emp : employees) {
        out << emp.name;
        for (const auto& day : days) {
            if (emp.assignedShifts.count(day))
                out << "," << emp.assignedShifts.at(day);
            else
                out << ",";
        }
        out << endl;
    }
}

int main() {
    vector<Employee> employees;
    set<string> existingNames;
    readInput(employees, existingNames);
    assignShifts(employees);
    writeOutput(employees);
    cout << "Final schedule written to output.csv" << endl;
    return 0;
}
