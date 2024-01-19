import asyncio
from pprint import pprint

from sqlalchemy import select, func, desc, and_

from models import (
    Student,
    Group,
    StudentGrade,
    StudentGroup,
    Grade,
    Teacher,
    TeacherSubject,
    Subject,
    AsyncDBSession,
)


async def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    async with AsyncDBSession() as session:
        students = await session.execute(
            select(
                func.round(func.avg(Grade.value), 2),
                StudentGrade.student_id,
                Student.first_name,
                Student.last_name,
            )
            .join(StudentGrade, StudentGrade.grade_id == Grade.id)
            .join(Student, Student.id == StudentGrade.student_id)
            .group_by(StudentGrade.student_id)
            .group_by(Student.first_name)
            .group_by(Student.last_name)
            .order_by(desc(func.round(func.avg(Grade.value), 2)))
            .limit(5)
        )
        students = students.all()
        return students


async def select_2(subject_name: str):
    # Знайти студента із найвищим середнім балом з певного предмета.
    async with AsyncDBSession() as session:
        students = await session.execute(
            select(
                func.round(func.avg(Grade.value), 2),
                StudentGrade.student_id,
                Student.first_name,
                Student.last_name,
            )
            .join(StudentGrade, StudentGrade.grade_id == Grade.id)
            .join(Student, Student.id == StudentGrade.student_id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
            .where(Subject.name == subject_name)
            .group_by(StudentGrade.student_id)
            .group_by(Student.first_name)
            .group_by(Student.last_name)
            .order_by(desc(func.round(func.avg(Grade.value), 2)))
            .limit(1)
        )
        students = students.one_or_none()
        return students


async def select_3(subject_name: str):
    # Знайти середній бал у групах з певного предмета.
    async with AsyncDBSession() as session:
        grades = await session.execute(
            select(
                func.round(func.avg(Grade.value), 2),
                Subject.name
            )
            .join(StudentGrade, StudentGrade.grade_id == Grade.id)
            .join(Student, Student.id == StudentGrade.student_id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
            .where(Subject.name == subject_name)
            .group_by(Subject.name)
        )
        avg_grades = grades.all()
        return avg_grades

async def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок).
    async with AsyncDBSession() as session:
        grades = await session.execute(
            select(
                func.round(func.avg(Grade.value), 2)
            )
            .join(StudentGrade, StudentGrade.grade_id == Grade.id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
        )
        avg_grades = grades.one_or_none()
        return avg_grades

async def select_5(teacher_id: int):
    # Знайти які курси читає певний викладач.
    async with AsyncDBSession() as session:
        teachers_subjects = await session.execute(
            select(
                Subject.name, Teacher.first_name, Teacher.last_name
            )
            .join(TeacherSubject, TeacherSubject.subject_id == Subject.id)
            .join(Teacher, Teacher.id == TeacherSubject.teacher_id)
            .where(Teacher.id == teacher_id)
        )
        teachers_subjects = teachers_subjects.all()
        return teachers_subjects


async def select_6(group_code: str):
    # Знайти список студентів у певній групі.
    async with AsyncDBSession() as session:
        students = await session.execute(
            select(
                Group.name, Group.code, Student.first_name, Student.last_name
            )
            .join(StudentGroup, StudentGroup.group_id == Group.id)
            .join(Student, Student.id == StudentGroup.student_id)
            .where(Group.code == group_code)
        )
        students = students.all()
        return students

async def select_7(group_code: str, subject_name: str):
    # Знайти оцінки студентів у окремій групі з певного предмета.
    async with AsyncDBSession() as session:
        grades = await session.execute(
            select(
                Student.first_name, Student.last_name, Grade.value.label("grade_value"),
                Group.code.label("group_code"), Subject.name.label("subject_name")
            )
            .join(StudentGrade, Student.id == StudentGrade.student_id)
            .join(StudentGroup, Student.id == StudentGroup.student_id)
            .join(Group, Group.id == StudentGroup.group_id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
            .join(Grade, Grade.id == StudentGrade.grade_id)
            .where(and_(Group.code == group_code, Subject.name == subject_name))
        )
        grades = grades.all()
        return grades

async def select_8():
    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    async with AsyncDBSession() as session:
        avg_grades = await session.execute(
            select(
                func.round(func.avg(Grade.value), 2).label("avg_grade"),
                Teacher.first_name, Teacher.last_name
            )
            .join(StudentGrade, Grade.id == StudentGrade.grade_id)
            .join(TeacherSubject, TeacherSubject.subject_id == StudentGrade.subject_id)
            .join(Teacher, Teacher.id == TeacherSubject.teacher_id)
            .group_by(Teacher.first_name)
            .group_by(Teacher.last_name)
        )
        avg_grades = avg_grades.all()
        return avg_grades

async def select_9(student_id: int):
    # Знайти список курсів, які відвідує студент.
    async with AsyncDBSession() as session:
        courses = await session.execute(
            select(
                func.count(Student.id).label("rows_count"), Subject.name,
                Student.first_name, Student.last_name
            )
            .join(StudentGrade, Student.id == StudentGrade.student_id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
            .where(Student.id == student_id)
            .group_by(Subject.name)
            .group_by(Student.first_name)
            .group_by(Student.last_name)
        )
        courses = courses.all()
        return courses

async def select_10(teacher_id: int, student_id: int):
    # Список курсів, які певному студенту читає певний викладач.
    async with AsyncDBSession() as session:
        courses = await session.execute(
            select(
                func.count(Student.id).label("rows_count"), Subject.name,
                Student.first_name, Student.last_name, Teacher.first_name,
                Teacher.last_name
            )
            .join(StudentGrade, Student.id == StudentGrade.student_id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
            .join(TeacherSubject, TeacherSubject.subject_id == Subject.id)
            .join(Teacher, Teacher.id == TeacherSubject.teacher_id)
            .where(and_(Teacher.id == teacher_id, Student.id == student_id))
            .group_by(Subject.name)
            .group_by(Teacher.first_name)
            .group_by(Teacher.last_name)
            .group_by(Student.first_name)
            .group_by(Student.last_name)
        )
        courses = courses.all()
        return courses

async def select_1_additional(teacher_id: int, student_id: int):
    # Середній бал, який певний викладач ставить певному студентові.
    async with AsyncDBSession() as session:
        avg_grade = await session.execute(
            select(
                func.round(func.avg(Grade.value), 2).label("avg_grade"),
                Student.first_name, Student.last_name, Teacher.first_name,
                Teacher.last_name
            )
            .join(StudentGrade, Grade.id == StudentGrade.grade_id)
            .join(Student, Student.id == StudentGrade.student_id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
            .join(TeacherSubject, TeacherSubject.subject_id == Subject.id)
            .join(Teacher, Teacher.id == TeacherSubject.teacher_id)
            .where(and_(Teacher.id == teacher_id, Student.id == student_id))
            .group_by(Teacher.first_name)
            .group_by(Teacher.last_name)
            .group_by(Student.first_name)
            .group_by(Student.last_name)
        )
        avg_grade = avg_grade.one_or_none()
        return avg_grade

async def select_2_additional(subject_name: str, group_code: str):
    # Оцінки студентів у певній групі з певного предмета на останньому занятті.
    async with AsyncDBSession() as session:
        avg_grade = await session.execute(
            select(
                func.max(StudentGrade.id).label("max_student_grade_id"),
                func.max(StudentGrade.created_at).label("max_student_created_at"),
                Student.first_name, Student.last_name,
                Group.code, Subject.name.label("subject_name")
            )
            .join(Student, Student.id == StudentGrade.student_id)
            .join(Subject, Subject.id == StudentGrade.subject_id)
            .join(StudentGroup, StudentGroup.student_id == Student.id)
            .join(Group, Group.id == StudentGroup.group_id)
            .where(and_(Subject.name == subject_name, Group.code == group_code))
            .group_by(Student.first_name)
            .group_by(Student.last_name)
            .group_by(Group.code)
            .group_by(Subject.name)
            .group_by(Student.id)
            .group_by(Subject.id)
        )
        avg_grade = avg_grade.all()
        return avg_grade

if __name__ == "__main__":
    rows = asyncio.run(select_2_additional(subject_name="LITERATURE", group_code="Johnson"))
    print(len(rows))
    pprint(rows)
