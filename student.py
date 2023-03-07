"""
Written by Ryan O'Callaghan on 05/03/2022
1: Student Class to represent a student at a university

{Student}:
    - student_id : string of student id
    - name : string of student name
    - is_sick : boolean representation of students health
"""

import json


class Student:

    def __init__(self, student_id: str, name: str, is_sick: bool) -> None:

        if not self.is_valid_id(student_id):
            raise ValueError(f'The student ID {student_id} is not a valid ID')
        else:
            self.student_id = student_id

        self.name = name
        self.is_sick = is_sick

    def __str__(self) -> str:
        return f'{self.name} ({self.student_id})'

    def __repr__(self) -> str:
        return f'{self.name} ({self.student_id})'

    # Purpose: Reads a string in JSON format and converts it into a Student object.
    @classmethod
    def from_JSON(cls, JSON_string: str):
        """
        from_JSON :: Using a string representation of an object from a JSON file (one line in the file), create a
        student object.

        :param JSON_string: One line of JSON file, or one object. I.e. '{"id": "260111111", "name": "Larry"}'
        :return: Student object
        """

        student_dict = json.loads(JSON_string)
        try:
            student = Student(student_dict['id'], student_dict['name'], False)
        except KeyError:
            print("The key(s) are incorrect for type: Student")
        else:
            return student

    # A valid student id is one that is 9 digits in length and the first three digits are 2, 6, 0.
    @staticmethod
    def is_valid_id(student_id: str) -> bool:
        """
        is_valid_id :: Validates given string by making sure it follows the formatting of a student ID. '260xxxxxx'

        :param student_id: Student id that you wish to validate.
        :return: Boolean value based on if the id given is valid based on school guidelines.
        """

        _loopCount = 0  # Count the amount of iterations of the for loop as it will be needed after the for loop.

        for char in student_id:
            # Initial check to determine if the first three characters are 2, 6, 0.
            if _loopCount == 0 and char != '2':
                return False
            elif _loopCount == 1 and char != '6':
                return False
            elif _loopCount == 2 and char != '0':
                return False
            elif not char.isdigit():
                return False

            if _loopCount > 9:
                break

            _loopCount += 1

        # Check the loop counter after the loop is exhausted. If _loopCount == 9, then the number of characters == 9.
        if _loopCount == 9:
            return True
        else:
            return False
