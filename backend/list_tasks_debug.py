from sqlmodel import Session, select
from db import engine
from models import User, Task

with Session(engine) as session:
    users = session.exec(select(User)).all()
    print("Users:")
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}")
        tasks = session.exec(select(Task).where(Task.user_id == u.id)).all()
        print(f"  Tasks ({len(tasks)}):")
        for t in tasks:
            print(f"    - [{t.status}] {t.title}")
