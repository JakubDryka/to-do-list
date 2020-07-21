from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print('4) Missed tasks')
    print("5) Add task")
    print('6) Delete task')
    print('0) Exit')

def add_task():
    task_add = input("Enter task")
    deadline_add = input('Enter deadline')
    new_row = Table(task=task_add,
                    deadline=datetime.strptime(deadline_add, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def print_all_tasks():
    print('All tasks:')
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print('Nothing to do!')
    else:
      i = 1
      for row in rows:
        print(i, '.', row.task, row.deadline.strftime('%d %b').lstrip('0'))
        i += 1
    print()


def missed_tasks():
    today = datetime.today().date()
    print('Missed tasks:')
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    if len(rows) == 0:
        print('Nothing is missed!')
    else:
      i = 1
      for row in rows:
        print(i, '.', row.task, row.deadline.strftime('%d %b').lstrip('0'))
        i += 1
    print()


def delete_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print('Nothing to delete')
    else:
        print('Chose the number of the task you want to delete:')
        i = 1
        for row in rows:
            print(i, '.', row.task, row.deadline.strftime('%d %b').lstrip('0'))
            i += 1
        num_delete = int(input())
        session.delete(rows[num_delete])
        session.commit()
        print('The task has been deleted!')


def print_daily_tasks():
    today = datetime.today().date()
    print('Today', today.day, today.strftime('%b'), ':')
    rows = session.query(Table).filter(Table.deadline == today).all()
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in range(len(rows)):
            print(rows[i].id, '.', rows[i].task)
    print()


def print_weekly_tasks():
    today = datetime.today().date()
    weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    start_weekday = today.weekday()
    task_num = 1
    for i in range(7):
        actual_day = start_weekday % 7
        print(weekDays[actual_day], today.day, today.strftime('%b'), ':')
        rows = session.query(Table).filter(Table.deadline == today).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for i in range(len(rows)):
                print(task_num, '.', rows[i].task)
                task_num += 1
        print()
        today += timedelta(days=1)
        start_weekday += 1


def use_input(user_input):
    if user_input == '1':
        print_daily_tasks()
        return
    elif user_input == '2':
        print_weekly_tasks()
        return
    elif user_input == '3':
        print_all_tasks()
        return
    elif user_input == '4':
        missed_tasks()
        return
    elif user_input == '5':
        add_task()
        return
    elif user_input == '6':
        delete_tasks()
        return
    elif user_input == '0':
        print('Bye!')
        sys.exit()


def start():
    while True:
        print_menu()
        user_input = input()
        use_input(user_input)


start()
