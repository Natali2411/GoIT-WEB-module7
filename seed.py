import asyncio
from datetime import datetime

import faker
from random import randint, choice

from enums import GENDER, GRADE, SUBJECT
from models import (
    insert_objects,
    Student,
    Group,
    StudentGrade,
    StudentGroup,
    Grade,
    Teacher,
    TeacherSubject,
    Subject,
)

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_STUDENTS_IN_GROUPS = 20
NUMBER_SUBJECTS = len(SUBJECT)
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20


def generate_fake_data() -> dict[str, list]:
    fake_students = []
    fake_groups = []
    fake_students_groups = []
    fake_teachers = []
    fake_subjects = []
    fake_grades = []
    fake_students_grades = []
    fake_teachers_subjects = []

    fake_data = faker.Faker()
    genders = (GENDER.MALE.value, GENDER.FEMALE.value)

    for _ in range(NUMBER_STUDENTS):
        first_name, last_name = fake_data.name().split()[:2]
        fake_students.append(
            Student(
                first_name=first_name,
                last_name=last_name,
                birthdate=datetime.strptime(fake_data.date(), "%Y-%m-%d"),
                gender=choice(genders),
            )
        )

    for _ in range(NUMBER_GROUPS):
        name, code = fake_data.name().split()[:2]
        fake_groups.append(Group(name=name, code=code))

    for _ in range(NUMBER_STUDENTS_IN_GROUPS * NUMBER_GROUPS):
        fake_students_groups.append(
            StudentGroup(
                student_id=randint(1, NUMBER_STUDENTS),
                group_id=randint(1, NUMBER_GROUPS),
            )
        )

    for _ in range(NUMBER_TEACHERS):
        first_name, last_name = fake_data.name().split()[:2]
        fake_teachers.append(
            Teacher(
                first_name=first_name,
                last_name=last_name,
                birthdate=datetime.strptime(fake_data.date(), "%Y-%m-%d"),
                gender=choice(genders),
            )
        )

    for subject in SUBJECT:
        fake_subjects.append(
            Subject(
                name=subject.value, description=f"'{subject.value}' " f"description"
            )
        )

    for _ in range(NUMBER_SUBJECTS * NUMBER_TEACHERS):
        fake_teachers_subjects.append(
            TeacherSubject(
                teacher_id=randint(1, NUMBER_TEACHERS),
                subject_id=randint(1, NUMBER_SUBJECTS),
            )
        )

    for grade in GRADE:
        fake_grades.append(
            Grade(code=grade.value.get("code"), value=grade.value.get("value"))
        )

    for _ in range(NUMBER_GRADES * NUMBER_STUDENTS * NUMBER_SUBJECTS):
        fake_students_grades.append(
            StudentGrade(
                student_id=randint(1, NUMBER_STUDENTS),
                grade_id=randint(1, len(GRADE)),
                subject_id=randint(1, NUMBER_SUBJECTS),
            )
        )

    return {
        "students": fake_students,
        "groups": fake_groups,
        "students_groups": fake_students_groups,
        "teachers": fake_teachers,
        "subjects": fake_subjects,
        "teachers_subjects": set(fake_teachers_subjects),
        "grades": fake_grades,
        "students_grades": fake_students_grades,
    }


async def insert_data_to_db():
    fake_data = generate_fake_data()
    for table_name, table_data in fake_data.items():
        await insert_objects(rows=table_data)


if __name__ == "__main__":
    asyncio.run(insert_data_to_db())
