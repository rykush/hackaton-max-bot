from app.database.models import Parser_data, User_setting
from app.database.session import get_db
from app.parser.parser_regulation import parsing_project
from app import get_bot
import asyncio


def user_db():
    db = next(get_db())
    users = db.query(User_setting).all()
    for u in users:
        print(u.id, u.max_id, u.on_off)

def parser_db():
    db = next(get_db())
    parsers_data = db.query(Parser_data).all()
    for p in parsers_data:
        print(p.id, p.document_id, p.document_send)

def delete_user(id: int):
    db = next(get_db())
    user = db.query(User_setting).filter_by(id=id).first()
    db.delete(user)
    db.commit()

def parser_db_edit():
    db = next(get_db())
    parsers_data = db.query(Parser_data).limit(3).all()
    for p in parsers_data:
        p.document_send = False
        db.commit()
        print(p.id, p.document_id, p.document_send)

if __name__ == '__main__':
    # delete_user(2)
    user_db()
    parser_db()
    # parser_db_edit()
