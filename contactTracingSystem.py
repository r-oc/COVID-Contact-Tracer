"""
Written by Ryan O'Callaghan on 05/03/2022
"""

from ContactTracker import *
from student import Student


def load_file(file_name: str) -> str:
    # Open file and read into string to be returned.
    with open(file_name, "r") as file:
        file_contents = file.read()

    return file_contents


# Purpose: Return list of students in JSON string
def JSON_to_students(JSON_string: str) -> List[Student]:
    student_list = []  # List containing all students from JSON file.

    for line in JSON_string.splitlines():
        line = line.strip(',')  # Remove commas at the end of item so the data can be read by from_JSON

        # This condition is necessary so the function does not send '[]' characters to the JSON parser.
        if line != ']' and line != '[':
            student_list.append(Student.from_JSON(line))

    return student_list


# Purpose: Return dictionary with all sick students [key] to the students they made contact with [data]
def csv_to_dictionary(CSV_string: str) -> Dict[str, List[str]]:
    student_dict = {}  # Initialize empty dict.

    for line in CSV_string.splitlines():
        # Place all elements (student id's) into a list to parse
        line_items = line.split(', ')

        # Pop the initial element (sick student) to use as [key], while the rest of the list is saved as the [data]
        key = line_items.pop(0)
        student_dict[key] = line_items

    return student_dict


def build_report(tracker: ContactTracker) -> str:
    report = "Contact Records:"

    for sick_student, contacts in tracker.get_all_contacts().items():
        string_contacts = [str(element) for element in contacts]
        report += f'\n\t{getStudent(sick_student)} had contact with '
        report += ", ".join(string_contacts)

    report += f'\n\nPatient Zero(s): {str(tracker.patient_zeros()).strip("[]")}'

    report += f'\nPotentially sick student(s): {str(tracker.potential_sick_students()).strip("[]")}'

    report += f'\nSick student(s) who got infected from another student: {str(tracker.sick_from_another_student()).strip("[]")}'

    report += f'\nMost viral student(s): {str(tracker.most_viral_students()).strip("[]")}'

    report += f'\nMost contacted student(s): {str(tracker.most_contacted_student()).strip("[]")}'

    report += f'\nUltra spreader(s): {str(tracker.ultra_spreaders()).strip("[]")}'

    report += f'\nNon-spreader(s): {str(tracker.non_spreaders()).strip("[]")}'

    report += '\n\nFor bonus: \nMinimum distances of students from patient zeros:'

    all_min_distances = tracker.all_min_distances_from_patient_zeros()

    for student_id, distance in all_min_distances.items():
        report += f'\n\t{getStudent(student_id)}: {distance}'

    return report


def write_in_file(file_name: str, text: str) -> None:
    with open(file_name, "w") as file:
        file.write(text)


def main() -> None:
    output_file = "contact_tracing_report.txt"
    JSON_file = "all_students.json"
    CSV_file = "cases.csv"

    # Load JSON file and store its data into student list generator
    try:
        data = load_file(JSON_file)
        stu_list = JSON_to_students(data)
    except FileNotFoundError:
        print(f'Sorry, the file {JSON_file} could not be found.')
        return

    # Load CSV File and store its data in csv dictionary generator
    try:
        data = load_file(CSV_file)
        stu_dict = csv_to_dictionary(data)
    except FileNotFoundError:
        print(f'Sorry, the file {CSV_file} could not be found.')
        return

    contact_tracker = ContactTracker(stu_list, stu_dict)

    # Build and save the report to output to file.
    report = build_report(contact_tracker)
    write_in_file(output_file, report)


if __name__ == '__main__': main()
