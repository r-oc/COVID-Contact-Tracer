"""
Written by Ryan O'Callaghan on 05/04/2022

{ContactTracker}:
    - students: list of students registered
    - cases_with_contacts: dictionary mapping sick students to the students they have made contact with
"""

import copy
from typing import List, Dict, Any
from student import Student


def verify_student_id(student_id: str) -> bool:
    """
    verify_student_id :: Verify that given ID is a registered student.

    :param student_id: Student ID as string.
    :return: Bool representation of the validity of the student_id given.
    """
    for student in ContactTracker.students:
        if student_id == student.student_id:
            return True

    return False


def getStudent(student_id: str) -> Student:
    """
    getStudent :: Returns the student object with given string student ID.

    :param student_id: String representation of student ID.
    :return: Student object matching student ID :param.
    """
    for student in ContactTracker.students:
        if student_id == student.student_id:
            return student


class ContactTracker:
    students = []

    # [1] Input dictionary has the same structure as cases_with_contacts
    def __init__(self, students: List[Student], cases_with_contacts: Dict[str, List[str]]):

        # [4] The initializations of the cases_with_contacts attribute is done by deep copying.
        self.cases_with_contacts = copy.deepcopy(cases_with_contacts)

        # [2] List of students is only to be initialized once (because the students don't change throughout the
        # semester) type(self) will return: ContractTracker
        if not self.students:
            type(self).students = students

        # [3] Check: All student IDs appearing in 'cases_with_contacts' can be found in the student list.
        for key in cases_with_contacts:

            if not verify_student_id(key):
                raise ValueError(f'A student with id {key} either does not exist or is not reported sick.')

            # At this point, all keys have been verified as enrolled students. Now to check their contacts...
            for contact_id in cases_with_contacts[key]:

                if not verify_student_id(contact_id):
                    raise ValueError(f'A student with id {contact_id} either does not exist or is not reported sick.')

    def get_contacts_by_student_id(self, sick_student_id: str) -> List[Student]:
        """
        get_contacts_by_student_id :: Given a student ID, return a list of students that the given student made contact
        with.

        :param sick_student_id: Sick student's ID
        :return: List of students that the sick student made contact with.
        """
        list_of_students = []  # The list of students that we will return.

        # Retrieve the list value with key (sick_student_id)
        _str_contact_list = self.cases_with_contacts.get(sick_student_id)

        # If the list is empty, the student does not exist or is not sick.
        if _str_contact_list is None:
            raise ValueError(f'A student with id {sick_student_id} either does not exist or is not reported as sick.')

        # The student_id is coming from the dictionary within the class, so they have already been verified.
        # Therefore, search_students_list will always return a student.
        for student_id in _str_contact_list:
            list_of_students.append(getStudent(student_id))

        return list_of_students

    def get_all_contacts(self) -> Dict[str, List[Student]]:
        """
        get_all_contacts :: Creates dictionary using cases_with_contacts dictionary.

        :return: A dictionary mapping student ID's with a list of students they made contact with.
        """
        contact_dict = {}

        for key in self.cases_with_contacts:
            _temp_list = []

            for student_id in self.cases_with_contacts[key]:
                _temp_list.append(getStudent(student_id))

            contact_dict[key] = _temp_list

        return contact_dict

    # A patient zero: A student that did not contract the virus through another student. I.e. They do not appear on
    # any other student's contact list.
    def patient_zeros(self) -> List[Student]:
        """
        patient_zeros :: A patient zero is a student that did not contract the virus from any other student.

        :return: A list of patient zero student(s).
        """
        patient_zero_list = []  # List of patient zeros
        contact_dict = self.get_all_contacts()  # Dictionary containing student ID as key and Student list as value.

        # For every sick student ID in the contact dictionary, we need to cross-reference this ID with every other
        # contact list.
        for sick_student_id in contact_dict:

            # By default, assume the student is a patient zero unless they appear in the list.
            is_patient_zero = True

            # Loop through all the sick students again, then traverse through the list of contacts to see if there are
            # any matches. To cross-reference every sick student with every sick students list.
            for sick_student in contact_dict:
                for student_contact in contact_dict[sick_student]:

                    # If the initial sick student ID that we are analyzing matches any student contacts ID, then they
                    # appear in another student's contact list, meaning they likely contracted from another student and
                    # are not patient zeros.
                    if sick_student_id == student_contact.student_id:
                        is_patient_zero = False

            if is_patient_zero:
                patient_zero_list.append(getStudent(sick_student_id))

        return patient_zero_list

    def isPatientZero(self, student_id: str) -> bool:
        """
        isPatientZero :: Given student_id, verify if this student is a patient zero (defined in patient_zeros() func.).

        :param student_id: String representation of student ID to check.
        :return: Bool value representing if student is patient zero or not.
        """
        for patient_zero in self.patient_zeros():
            if patient_zero.student_id == student_id:
                return True

        return False

    # TODO Make algorithm better, no triple for loops. With large values of input = n :: O(n^3) (maybe not possible)
    # TODO or at least just make helper functions to improve readability and complexity.
    def potential_sick_students(self) -> List[Student]:
        """
        potential_sick_students :: A potentially sick student is a student that is not sick, but may be sick as they
        appear in another sick students contact list.

        :return: Returns a list of potentially sick students.
        """
        potential_sick_students = []
        contact_dict = self.get_all_contacts()

        for key in contact_dict:
            for contact in contact_dict[key]:

                # Default == True, meaning that the student is potentially sick, not definitively.
                potentially_sick = True

                for sick_student in contact_dict:

                    # I.e. If this contact is (==) already a sick student.
                    if contact.student_id == sick_student:
                        potentially_sick = False  # False because they are already SICK, not potentially.

                # Append if potentially sick and not a duplicate.
                if potentially_sick and contact not in potential_sick_students:
                    potential_sick_students.append(contact)

        return potential_sick_students

    # Return of list of students that are SICK and appear in another students contact list.
    # I.e. These students are not patient zeros or potentially sick students.
    def sick_from_another_student(self) -> List[Student]:
        """
        sick_from_another_student :: Sick student(s) that is/are not a patient zero and appear(s) in another students
        contact list.

        :return: A list of students that got sick from another student.
        """
        patient_zeros = self.patient_zeros()
        potential_sick_students = self.potential_sick_students()

        sick_from_another_student = []

        for sick_student in self.cases_with_contacts:
            _temp_student = getStudent(sick_student)
            if _temp_student not in patient_zeros:
                if _temp_student not in potential_sick_students:
                    sick_from_another_student.append(_temp_student)

        return sick_from_another_student

    def most_viral_students(self) -> List[Student]:
        """
        most_viral_students :: Student(s) that contacted the largest number of other students. (i.e. longest contact
        list).

        :return: Student(s) with the most contacts (maybe more than one if they are equal).
        """
        most_viral_students = []
        contact_dict = self.get_all_contacts()

        # [1] Find the student with the largest amount of contacts.
        most_contacts = -1
        for sick_student_id in contact_dict:
            if len(contact_dict[sick_student_id]) > most_contacts:
                most_contacts = len(contact_dict[sick_student_id])
                most_contact_student = getStudent(sick_student_id)

        # most_contact_student variable will only not be initialized if the dictionary is empty since any entry would
        # constitute a larger amount of contacts than -1.
        try:
            most_viral_students.append(most_contact_student)

            # [2] Check for any that are equal
            for sick_student_id in contact_dict:
                if len(contact_dict[sick_student_id]) == most_contacts:
                    if getStudent(sick_student_id) not in most_viral_students:
                        most_viral_students.append(getStudent(sick_student_id))

        except UnboundLocalError:
            raise ValueError("Error: No sick students listed in cases_with_contact dictionary.")

        return most_viral_students

    def is_sick(self, student_id: str) -> bool:
        for sick_student_id in self.cases_with_contacts:
            if student_id == sick_student_id:
                return True

        return False

    # todo :: MORE EXTENSIVE ERROR CHECKING
    # Student that is NOT sick and appears in most contact lists.
    def most_contacted_student(self) -> List[Student]:
        """
        most_contacted_student :: Student(s) that are not sick, but have been in contact with the most amount of
        students.

        :return: List of the most contacted students.
        """
        most_contacted_students = []
        contact_dict = self.get_all_contacts()

        student_appearances = {}  # Dict[str, int]
        most_appearances = 0

        for student in self.students:

            if not self.is_sick(student.student_id):
                # print(f'\nChecking non sick student {student} contacts::')

                # The contact appearances the non-sick student has.
                _contact_appearances = 0

                for sick_student_id, contacts in contact_dict.items():
                    # print(f'{sick_student_id}, {contacts}')

                    for contact in contacts:
                        # print(f'Checking contact... {contact}')
                        if student.student_id == contact.student_id:
                            _contact_appearances += 1

                student_appearances[student.student_id] = _contact_appearances

        for student_id, appearances in student_appearances.items():
            if appearances > most_appearances:
                most_appearances = appearances
                most_appeared_student = getStudent(student_id)

        try:
            most_contacted_students.append(most_appeared_student)

            # Check for duplicates.
            for student_id, appearances in student_appearances.items():
                if appearances == most_appearances and getStudent(student_id) not in most_contacted_students:
                    most_contacted_students.append(getStudent(student_id))

        except UnboundLocalError:
            print("All students are already sick or non sick students do not appear in any contact lists.")

        return most_contacted_students

    def ultra_spreaders(self) -> List[Student]:
        """
        ultra_spreaders :: The student(s) that have been in contact with the most amount of students that were not
        already sick. (i.e. they spread the virus to the most amount of people that were not already sick)

        :return: List of student(s) that are ultra_spreaders.
        """
        ultra_spreaders = []

        contact_dict = self.get_all_contacts()

        for sick_student_id, contacts in contact_dict.items():
            _has_sick_contact = False

            for contact in contacts:
                if self.is_sick(contact.student_id):
                    _has_sick_contact = True

            # Only append if the sick student does not have any sick contacts and has at least 1 contact.
            if (not _has_sick_contact) and len(contacts) > 0:
                ultra_spreaders.append(getStudent(sick_student_id))

        return ultra_spreaders

    def non_spreaders(self) -> List[Student]:
        """
        non_spreaders :: The student(s) that are sick and have only been in contact with other sick students. (i.e. they
        could not have potentially spread the virus to anyone as everyone they contacted was already sick)

        :return: List of student(s) that are non_spreaders.
        """
        non_spreaders = []

        contact_dict = self.get_all_contacts()

        for sick_student_id, contacts in contact_dict.items():
            _all_contacts_sick = True

            for contact in contacts:
                if not self.is_sick(contact.student_id):
                    _all_contacts_sick = False

            if _all_contacts_sick:
                non_spreaders.append(getStudent(sick_student_id))

        return non_spreaders

    # Return the list of sick students that have contacted given student id
    def sick_students_contacted(self, student_id) -> List[Student]:
        """
        sick_students_contacted :: Will return a list of sick students that given student_id has had contact with.

        :param student_id: Student ID you wish to check has contacted any sick students.
        :return: List of sick students contacted.
        """
        sick_students_contacted = []

        for sick_student_id, contacts in self.get_all_contacts().items():
            for contact in contacts:
                if contact.student_id == student_id:
                    sick_students_contacted.append(getStudent(sick_student_id))

        return sick_students_contacted

    def min_distance_from_patient_zeros(self, student_id: str) -> int:
        """
        min_distance_from_patient_zeros :: The purpose of this function is to recursively calculate the distance from
        a given student id to a patient zero.

        Checks if the student is a patient zero, and return 0 accordingly. Otherwise, calculates the distance for every
        sick student that the given id has contacted, and returning the minimum distance plus one.

        NOTE: No cycles of any length is assumed AND each student is a patient zero or has a path to one is assumed.

        :param student_id: Student ID string of the student you wish to find the minimum distance to a patient zero.
        :return: The distance between given student and a patient zero.
        """

        list_of_distances = []

        if getStudent(student_id) is None:
            raise ValueError(f'A student with id {student_id} either does not exist or is not reported as sick.')

        if self.isPatientZero(student_id):
            return 0
        else:
            sick_students_contacted = self.sick_students_contacted(student_id)
            for student in sick_students_contacted:
                list_of_distances.append(self.min_distance_from_patient_zeros(student.student_id))

            return 1 + min(list_of_distances)

    def all_min_distances_from_patient_zeros(self) -> Dict[str, int]:
        """
        all_min_distances_from_patient_zeros :: Get the minimum distance for each student.

        :return: Dictionary with student ID's mapping their distance from patient zero.
        """
        all_min_distances = {}

        for student in self.students:
            all_min_distances[student.student_id] = self.min_distance_from_patient_zeros(student.student_id)

        return all_min_distances


"""
###############
### TESTING ###
###############
DEBUG = False

if DEBUG:
    # Load JSON file
    data = load_file("all_students.json")
    stu_list = JSON_to_students(data)

    # Load CSV File
    data1 = load_file("cases.csv")
    stu_dict = csv_to_dictionary(data1)

    # Create ContactTracker instance
    contactTracker1 = ContactTracker(stu_list, stu_dict)

    # print("\nContact Dictionary: ")
    # print(contactTracker1.cases_with_contacts)

    # print("\nList of students: ")
    # print(contactTracker1.students)

    #
    # Verify Student ID by string_id
    #
    # student_id = "260840155"
    # print(f'\nStudent id {student_id} is valid: {verify_student_id(student_id)}')

    #
    # Return list of student's contacts by string_id
    #
    # student_id = "260561504"
    # print(f'\nContacts of student {getStudent(student_id)}: {contactTracker1.get_contacts_by_student_id(student_id)}')

    ########################
    ##### Method Tests #####
    ########################

    # print(contactTracker1.get_all_contacts())

    # print(contactTracker1.patient_zeros())

    # print(contactTracker1.potential_sick_students())

    # print(contactTracker1.sick_from_another_student())

    # print(contactTracker1.most_viral_students())

    # print(contactTracker1.is_sick("260248711"))

    # print(contactTracker1.most_contacted_student())

    # print(contactTracker1.ultra_spreaders())

    # print(contactTracker1.non_spreaders())

    # print(contactTracker1.min_distance_from_patient_zeros("260970944"))
    # print(contactTracker1.isPatientZero("260386543"))

    # print(contactTracker1.sick_students_contacted("260970944"))

    # print(contactTracker1.all_min_distances_from_patient_zeros())
"""
