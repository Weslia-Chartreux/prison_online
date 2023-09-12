import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from db.models import User, Base, Group, Message_group

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


async def db_start():
    global db_sess
    global_init("src/db/info.db")
    db_sess = create_session()


async def add_user(tg_id: str, first_name: str, username: str):
    user = db_sess.query(User).filter(User.tg_id == tg_id).one_or_none()
    if user is not None:
        return user.id
    try:
        user = User(tg_id=tg_id, first_name=first_name, username=username)
        db_sess.add(user)
        db_sess.commit()
        user_id = user.id
    except Exception as error:
        print('Error', error)
        db_sess.rollback()
        user_id = -1
    return user_id


async def add_group(tg_id: str, type_group: str, title: str):
    group = db_sess.query(Group).filter(Group.tg_id == tg_id).one_or_none()
    if group is not None:
        return group.id
    try:
        group = Group(tg_id=tg_id, type_group=type_group, title=title)
        db_sess.add(group)
        db_sess.commit()
        group_id = group.id
    except Exception as error:
        print('Error', error)
        db_sess.rollback()
        group_id = -1
    return group_id


async def add_message(tg_id: str, user_id: int, group_id: int, text: str):
    try:
        message = Message_group(tg_id=tg_id, user_id=user_id, group_id=group_id, text=text)
        db_sess.add(message)
        db_sess.commit()
    except Exception as error:
        print('Error', error)
        db_sess.rollback()
    return 1


async def count_message_in_group(tg_id: str) -> int:
    group = db_sess.query(Group).filter(Group.tg_id == tg_id).one_or_none()
    if group is None:
        return 0
    return len(group.messages_group)


async def clean_form_database_group(tg_id: str) -> list:
    group = db_sess.query(Group).filter(Group.tg_id == tg_id).one_or_none()
    if group is None:
        return []
    message_author = []
    try:
        for m in group.messages_group:
            message_author.append((m.users.username, m.text))
            db_sess.delete(m)
        db_sess.commit()
        return message_author
    except Exception as error:
        print('Error', error)
        db_sess.rollback()
    return []