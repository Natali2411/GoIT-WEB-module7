from __future__ import annotations

import argparse
import asyncio
import logging
from datetime import datetime

from enums import CLI_ACTIONS
from models import *

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()])

parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

parser.add_argument("-a", "--action", default="create")
parser.add_argument("-m", "--model")
parser.add_argument("-n", "--name")
parser.add_argument("-i", "--id", type=int)
parser.add_argument("-g", "--gender")
parser.add_argument("-gr", "--group")
parser.add_argument("-b", "--birthdate")
parser.add_argument("-c", "--code")
parser.add_argument("-v", "--value")
parser.add_argument("-d", "--description")
parser.add_argument("-s", "--subject")
parser.add_argument("-gd", "--grade")

args = parser.parse_args()
print(args)


def define_action(args_action: str) -> CLI_ACTIONS:
    actions = list(CLI_ACTIONS)
    for action in actions:
        if args_action == action.value:
            return action.value


def read_cli_param(
        name: str, value: str | datetime, is_required: bool
) -> str | None:
    if value:
        return value
    else:
        if is_required:
            raise Exception(f"'{name}' is required, but the value wasn't passed")


async def create_teacher_cli():
    name = read_cli_param(name="name", value=args.name, is_required=True)
    gender = read_cli_param(
        name="gender", value=args.gender, is_required=True
    )
    birthdate = None
    try:
        birthdate_value = datetime.strptime(args.birthdate, "%Y-%m-%d")
        birthdate = read_cli_param(
            name="birthdate", value=birthdate_value, is_required=False
        )
    except Exception:
        pass
    first_name, last_name = name.split()

    await create_teacher(
        first_name=first_name, last_name=last_name, birthdate=birthdate, gender=gender
    )
    logging.info(f"Teacher '{name}' was created in DB")


async def update_teacher_cli():
    _id = read_cli_param(name="id", value=args.id, is_required=True)
    name = read_cli_param(name="name", value=args.name, is_required=False)
    gender = read_cli_param(
        name="gender", value=args.gender, is_required=False
    )
    birthdate = None
    try:
        birthdate_value = datetime.strptime(args.birthdate, "%Y-%m-%d")
        birthdate = read_cli_param(
            name="birthdate", value=birthdate_value, is_required=False
        )
    except Exception:
        pass
    first_name, last_name = name.split()

    await update_teacher(
        _id=_id, first_name=first_name, last_name=last_name, birthdate=birthdate,
        gender=gender
    )
    logging.info(f"Teacher '{name}' was updated in DB")


async def create_student_cli():
    name = read_cli_param(
        name="name", value=args.name, is_required=True
    )
    gender = read_cli_param(
        name="gender", value=args.gender, is_required=True
    )
    birthdate = None
    try:
        birthdate_value = datetime.strptime(args.birthdate, "%Y-%m-%d")
        birthdate = read_cli_param(
            name="birthdate", value=birthdate_value, is_required=False
        )
    except Exception:
        pass
    first_name, last_name = name.split()

    await create_student(
        first_name=first_name, last_name=last_name, birthdate=birthdate, gender=gender
    )
    logging.info(f"Student '{name}' was created in DB")


async def update_student_cli():
    _id = read_cli_param(name="id", value=args.id, is_required=True)
    name = read_cli_param(name="name", value=args.name, is_required=False)
    gender = read_cli_param(
        name="gender", value=args.gender, is_required=False
    )
    birthdate = None
    try:
        birthdate_value = datetime.strptime(args.birthdate, "%Y-%m-%d")
        birthdate = read_cli_param(
            name="birthdate", value=birthdate_value, is_required=False
        )
    except Exception:
        pass
    first_name, last_name = name.split()

    await update_student(
        _id=_id, first_name=first_name, last_name=last_name, birthdate=birthdate,
        gender=gender
    )
    logging.info(f"Student '{name}' was updated in DB")


async def create_group_cli():
    name = read_cli_param(
        name="name", value=args.name, is_required=True
    )
    code = read_cli_param(
        name="code", value=args.code, is_required=True
    )

    await create_group(name=name, code=code)
    logging.info(f"Student group '{name}' was created in DB")


async def update_group_cli():
    _id = read_cli_param(name="id", value=args.id, is_required=True)
    name = read_cli_param(
        name="name", value=args.name, is_required=False
    )
    code = read_cli_param(
        name="code", value=args.code, is_required=False
    )

    await update_group(_id=_id, name=name, code=code)
    logging.info(f"Student group with id '{_id}' was updated in DB")


async def create_grade_cli():
    value = read_cli_param(
        name="value", value=args.value, is_required=True
    )
    code = read_cli_param(
        name="code", value=args.code, is_required=True
    )

    await create_grade(value=value, code=code)
    logging.info(f"Grade with value '{value}' and code '{code}' was created in DB")


async def update_grade_cli():
    _id = read_cli_param(name="id", value=args.id, is_required=True)
    value = read_cli_param(
        name="value", value=args.value, is_required=False
    )
    code = read_cli_param(
        name="code", value=args.code, is_required=False
    )

    await update_grade(_id=_id, value=value, code=code)
    logging.info(f"Grade with id {_id} was updated to the value '{value}'.")


async def create_subject_cli():
    name = read_cli_param(
        name="name", value=args.name, is_required=True
    )
    description = read_cli_param(
        name="description", value=args.description, is_required=True
    )

    await create_subject(name=name, description=description)
    logging.info(
        f"Subject with the name '{name}' and description '{description}' was "
        f"created in DB"
    )


async def update_subject_cli():
    _id = read_cli_param(name="id", value=args.id, is_required=True)
    description = read_cli_param(
        name="description", value=args.description, is_required=False
    )
    name = read_cli_param(
        name="name", value=args.name, is_required=False
    )

    await update_subject(_id=_id, name=name, description=description)
    logging.info(f"Subject with id {_id} was updated to the name '{name}' and "
                 f"description '{description}'.")


async def create_student_group_cli():
    name = read_cli_param(
        name="name", value=args.name, is_required=True
    )
    group = read_cli_param(
        name="group", value=args.group, is_required=True
    )

    await create_student_group(
        student_name=name, group_name=group
    )
    logging.info(f"Student '{name}' was added to group '{group}'")


async def create_teacher_subject_cli():
    name = read_cli_param(
        name="name", value=args.name, is_required=True
    )
    subject = read_cli_param(
        name="subject", value=args.subject, is_required=True
    )
    await create_teacher_subject(teacher_name=name, subject_name=subject)


async def create_student_grade_cli():
    name = read_cli_param(
        name="name", value=args.name, is_required=True
    )
    subject = read_cli_param(
        name="subject", value=args.subject, is_required=True
    )
    grade = read_cli_param(
        name="grade", value=args.grade, is_required=True
    )
    await create_student_grade(grade_code=grade, student_name=name, subject_name=subject)


async def list_all_cli(model: Base) -> list[dict]:
    rows = await find_all_rows(model=model)
    logging.info(f"Getting rows for the model '{model.__name__}'")
    return rows


async def delete_db_row_cli(model: Base) -> None:
    _id = read_cli_param(
        name="id", value=args.id, is_required=True
    )
    is_deleted = await delete_db_row_by_id(model=model, row_id=_id)
    if is_deleted:
        logging.info(f"Row with id {_id} for the model '{model.__name__}' was deleted")


METHODS = {
    CLI_ACTIONS.CREATE.value: {
        Teacher.__name__: create_teacher_cli,
        Subject.__name__: create_subject_cli,
        Student.__name__: create_student_cli,
        Grade.__name__: create_grade_cli,
        Group.__name__: create_group_cli,
        StudentGroup.__name__: create_student_group,
        TeacherSubject.__name__: create_teacher_subject_cli,
        StudentGrade.__name__: create_student_grade_cli,
    },
    CLI_ACTIONS.UPDATE.value: {
        Teacher.__name__: update_teacher_cli,
        Subject.__name__: update_subject_cli,
        Student.__name__: update_student_cli,
        Grade.__name__: update_grade_cli,
        Group.__name__: update_group_cli,
    }
}

if __name__ == "__main__":
    _model: str = read_cli_param(
        name="model", value=args.model, is_required=True
    )
    model: Base = MODELS.get(_model)
    action = read_cli_param(
        name="action", value=args.action, is_required=True
    )
    if action == CLI_ACTIONS.LIST.value:
        rows = asyncio.run(list_all_cli(model=model))
        print(rows)
    elif action == CLI_ACTIONS.REMOVE.value:
        asyncio.run(delete_db_row_cli(model=model))
    else:
        method = METHODS.get(action).get(_model)
        asyncio.run(method())
