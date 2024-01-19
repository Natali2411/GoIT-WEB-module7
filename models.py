from __future__ import annotations

import asyncio
import logging
import os
from typing import Any, Tuple, Sequence, List

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy import Integer, String, select, func, and_, Row, inspect
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from dotenv import load_dotenv

from enums import GENDER, SUBJECT

load_dotenv()

engine = create_async_engine(os.getenv("SQLALCHEMY_URL"), echo=True)
AsyncDBSession = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()
Base.metadata.bind = engine


class Student(Base):
    __tablename__ = "students" # !!!
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[str] = mapped_column(DateTime, nullable=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationship to StudentGrade with back_populates 'student'
    grades = relationship("StudentGrade", back_populates="student",
                          cascade="all, delete")
    # Relationship to StudentGroup with back_populates 'student'
    group = relationship("StudentGroup", back_populates="student",
                          cascade="all, delete")



class Grade(Base):
    __tablename__ = "grades" # !!!
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationship to StudentGrade with back_populates 'student'
    students_grades = relationship("StudentGrade", back_populates="grade",
                                   cascade="all, delete")


class Group(Base):
    __tablename__ = "groups" # !!!
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationship to StudentGroup with back_populates 'groups'
    student_group = relationship("StudentGroup", back_populates="groups",
                                 cascade="all, delete")


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    teacher_subjects = relationship("TeacherSubject", back_populates="subject",
                                    cascade="all, delete")
    # Relationship to Subject with back_populates 'students_grades'
    students_grades_subjects = relationship("StudentGrade",
                                            back_populates="student_grades",
                                            cascade="all, delete")


class StudentGrade(Base):
    __tablename__ = "students_grades" # !!!
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"))
    grade_id: Mapped[int] = mapped_column(Integer, ForeignKey("grades.id"))
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationship to Student with back_populates 'grades'
    student = relationship("Student", back_populates="grades")

    # Relationship to Grade with back_populates 'students_grades'
    grade = relationship("Grade", back_populates="students_grades")

    # Relationship to Subject with back_populates 'students_grades'
    student_grades = relationship("Subject", back_populates="students_grades_subjects")

class Teacher(Base):
    __tablename__ = "teachers" # !!!
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[str] = mapped_column(DateTime, nullable=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    subjects = relationship("TeacherSubject", back_populates="teacher",
                            cascade="all, delete-orphan")


class TeacherSubject(Base):
    __tablename__ = "teachers_subjects" # !!!
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.id"))
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"))
    subject: Mapped["Subject"] = relationship(Subject, back_populates="teacher_subjects",
                                              single_parent=True)
    teacher: Mapped["Teacher"] = relationship(Teacher, back_populates="subjects",
                                              single_parent=True)


class StudentGroup(Base):
    __tablename__ = "students_groups" # !!!
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))

    # Relationship to Student with back_populates 'group'
    student = relationship("Student", back_populates="group")
    # Relationship to Group with back_populates 'student_group'
    groups = relationship("Group", back_populates="student_group")


MODELS = {
    Student.__name__: Student,
    Teacher.__name__: Teacher,
    Subject.__name__: Subject,
    Grade.__name__: Grade,
    Group.__name__: Group,
    StudentGroup.__name__: StudentGroup,
    TeacherSubject.__name__: TeacherSubject,
    StudentGrade.__name__: StudentGrade,
}


async def find_all_rows(model: Base) -> list[dict]:
    async with AsyncDBSession() as session:
        rows = await session.execute(
            select(model).order_by(model.id)
        )
        rows = rows.all()
        formatted_rows = []
        inst = inspect(model)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        for row in rows:
            formatted_rows.append({k: getattr(row[0], k) for k in attr_names})
        return formatted_rows


async def get_row_by_id(model: Base, row_id: int) -> Base:
    async with AsyncDBSession() as session:
        row = await session.execute(
            select(model).where(model.id == row_id)
        )
        row = row.scalar()
        return row


async def delete_db_row_by_id(model: Base, row_id: int) -> bool:
    async with AsyncDBSession() as session:
        row = await get_row_by_id(model=model, row_id=row_id)
        if row:
            await session.delete(row)
            await session.commit()
            return True
        else:
            logging.info(f"Row with id '{row_id}' doesn't exist in the table "
                         f"'{model.__table__}'")
            return False


async def find_teacher_by_name(full_name: str) -> Teacher:
    first_name, last_name = full_name.split()
    async with AsyncDBSession() as session:
        teacher = await session.execute(
            select(Teacher).where(
                and_(Teacher.first_name == first_name, Teacher.last_name == last_name)
            )
        )
        teacher = teacher.one_or_none()
        return teacher


async def find_grade_by_code(grade_code: str) -> Grade:
    async with AsyncDBSession() as session:
        grade = await session.execute(select(Grade).where(Grade.code == grade_code))
        grade = grade.one_or_none()
        return grade


async def find_group_by_name(group_name: str) -> Group:
    async with AsyncDBSession() as session:
        group = await session.execute(select(Group).where(Group.code == group_name))
        group = group.one_or_none()
        return group


async def find_subject_by_name(subject_name: SUBJECT) -> Subject:
    async with AsyncDBSession() as session:
        subject = await session.execute(
            select(Subject).where(Subject.name == subject_name)
        )
        subject = subject.one_or_none()
        return subject


async def find_student_by_name(full_name: str) -> Student:
    first_name, last_name = full_name.split()
    async with AsyncDBSession() as session:
        student = await session.execute(
            select(Student).where(
                and_(Student.first_name == first_name, Student.last_name == last_name)
            )
        )
        student = student.one_or_none()
        return student


async def create_teacher(
        first_name: str, last_name: str, gender: GENDER | str, birthdate: str = None
):
    async with AsyncDBSession() as session:
        async with session.begin():
            teacher = Teacher(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birthdate=birthdate,
            )
            session.add(teacher)


async def update_teacher(
        _id: int, first_name: str = None, last_name: str = None,
        gender: GENDER | str = None, birthdate: str = None):
    teacher = await get_row_by_id(model=Teacher, row_id=_id)
    teacher.first_name = first_name if first_name else teacher.first_name
    teacher.last_name = last_name if first_name else teacher.last_name
    teacher.gender = gender if gender else teacher.gender
    teacher.birthdate = birthdate if birthdate else teacher.birthdate
    async with AsyncDBSession() as session:
        async with session.begin():
            session.add(teacher)
            await session.commit()


async def create_student(
        first_name: str, last_name: str, gender: GENDER | str, birthdate: str = None
):
    async with AsyncDBSession() as session:
        async with session.begin():
            student = Student(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birthdate=birthdate,
            )
            session.add(student)


async def update_student(
        _id: int, first_name: str = None, last_name: str = None,
        gender: GENDER | str = None, birthdate: str = None):
    student = await get_row_by_id(model=Student, row_id=_id)
    student.first_name = first_name if first_name else student.first_name
    student.last_name = last_name if first_name else student.last_name
    student.gender = gender if gender else student.gender
    student.birthdate = birthdate if birthdate else student.birthdate
    async with AsyncDBSession() as session:
        async with session.begin():
            session.add(student)
            await session.commit()


async def create_group(name: str, code: str):
    async with AsyncDBSession() as session:
        async with session.begin():
            group = Group(
                name=name,
                code=code,
            )
            session.add(group)


async def update_group(
        _id: int, name: str = None, code: str = None):
    group = await get_row_by_id(model=Group, row_id=_id)
    group.name = name if name else group.name
    group.code = code if code else group.code
    async with AsyncDBSession() as session:
        async with session.begin():
            session.add(group)
            await session.commit()


async def create_grade(value: str, code: str):
    async with AsyncDBSession() as session:
        async with session.begin():
            grade = Grade(
                value=value,
                code=code,
            )
            session.add(grade)


async def update_grade(
        _id: int, value: str = None, code: str = None):
    grade = await get_row_by_id(model=Grade, row_id=_id)
    grade.value = value if value else grade.name
    grade.code = code if code else grade.code
    async with AsyncDBSession() as session:
        async with session.begin():
            session.add(grade)
            await session.commit()


async def create_subject(name: str, description: str):
    async with AsyncDBSession() as session:
        async with session.begin():
            subject = Subject(
                name=name,
                description=description,
            )
            session.add(subject)


async def update_subject(
        _id: int, name: str = None, description: str = None):
    subject = await get_row_by_id(model=Subject, row_id=_id)
    subject.name = name if name else subject.name
    subject.description = description if description else subject.description
    async with AsyncDBSession() as session:
        async with session.begin():
            session.add(subject)
            await session.commit()


async def create_teacher_subject(teacher_name: str, subject_name: SUBJECT):
    teacher_id = find_teacher_by_name(full_name=teacher_name).id
    subject_id = find_subject_by_name(subject_name=subject_name).id
    async with AsyncDBSession() as session:
        async with session.begin():
            teacher_subject = TeacherSubject(
                teacher_id=teacher_id,
                subject_id=subject_id,
            )
            session.add(teacher_subject)


async def create_student_grade(grade_code: str, student_name: str, subject_name:
SUBJECT):
    student_id = find_teacher_by_name(full_name=student_name).id
    grade_id = find_grade_by_code(grade_code=grade_code).id
    subject_id = find_subject_by_name(subject_name=subject_name).id
    async with AsyncDBSession() as session:
        async with session.begin():
            teacher_subject = StudentGrade(
                grade_id=grade_id, subject_id=subject_id, student_id=student_id
            )
            session.add(teacher_subject)


async def create_student_group(student_name: str, group_name: str):
    student_id = find_teacher_by_name(full_name=student_name).id
    group_id = find_group_by_name(group_name=group_name).id
    async with AsyncDBSession() as session:
        async with session.begin():
            student_group = StudentGroup(
                student_id=student_id, group_id=group_id
            )
            session.add(student_group)


async def insert_objects(rows: list[Any]) -> None:
    async with AsyncDBSession() as session:
        async with session.begin():
            session.add_all(rows)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())
