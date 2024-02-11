#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'),
        UniqueConstraint(
            'email',
            name = 'unique-email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name = 'grade_between_1_and_12')
    )

    Index('index_name','name')
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column (DateTime())
    enrolled_date = Column(DateTime(),default = datetime.now())
    
    #CRATING DATA
    
    def __repr__(self):
        return f"Student {self.id}" \
            + f"{self.name}" \
            + f"Grade {self.grade}"
    
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    #using our engine to configure a "Session class"
    Session = sessionmaker(bind=engine)
    #use "Session" class to create 'session' object 
    session = Session()
    
    albert_einstein=Student(
        name = 'Albert Einstein',
        email= 'albert.einstein@zurich.edu',
        grade=6,
        birthday = datetime(
            year=1879,
            month=3,
            day=14
        ),
    )
    
    alan_turing = Student(
        name = 'Alan Turing',
        email ='alan.turing@shereborne.edu',
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )
    
    
    session.bulk_save_objects([albert_einstein,alan_turing])
    session.commit()
    
    
    #MANIPULATING DATA 
    
    # different ways of representing output of objects in sqlalchemy
    
    #1. singular 
    # print(f"New student ID is {albert_einstein}.")
    # print(f"New student ID is {alan_turing}.")
    
    # 2. using query dot notation to loop over output 
    # students = session.query(Student)
    
    # print([student for student in students])
    
    # 3. using all()
    students = session.query(Student).all()
    print(students)
    
    # How to choose only certain columns
    names = [name for name in session.query(Student.name)]
    print(names)
    
    emails = [email for email in session.query(Student.email)]
    print (emails)
    
    #How to order your date 
    
    student_by_name = [student for student in session.query(
        Student.name).order_by(
            Student.name)]
    print (student_by_name)
    
    #descending order 
    
    students_by_grade_desc = [student for student in session.query(
        Student.name, Student.grade).order_by(
            desc(Student.grade
        )
    )]
    
    print (students_by_grade_desc)
    
    #limiting by using .limit(1)
    
    oldest_student=[student for student in session.query(
        Student.name,Student.birthday).order_by(
            desc(Student.grade)).limit(1)
        
    ]
    print(oldest_student)
    
    # using common functions such as sum() count()
    
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)
    
    #filtering using .filter()
    
    query = session.query(Student).filter(Student.name.like('%Alan%'),
    Student.grade == 11)
    
    for record in query:
        print (record.name)


#UPDATING DATA 

    #using python language to update data and persis with session.commit()
    # for student in session.query(Student):
    #     student.grade += 1
    
    # session.commit()

    # print ([(student.name,
    #     student.grade) for student in session.query(Student)])

    #using the update() method

    session.query(Student).update({
            Student.grade:Student.grade + 1
    })

    print ([(
        student.name,
        student.grade
    )for student in session.query(Student)])
    
#DELETING DATA

    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")
        
    #retrieve first matching record as object
    albert_einstein = query.first()
    
    #delete record
    session.delete(albert_einstein)
    session.commit()
    
    #try to retrieve deleted record 
    albert_einstein = query.first()
    
    print(albert_einstein)