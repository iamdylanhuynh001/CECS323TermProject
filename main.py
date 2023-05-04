# This is a sample Python script.
import pymongo
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pymongo import MongoClient
from pprint import pprint
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from dotenv import load_dotenv
import os

def add(db):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def add_department(db):
    '''
    i. name – String length 50.  This is the primary key for this table.
    ii. abbreviation – String length 6 – mandatory
    iii. chair_name – String length 80 – mandatory
    iv. building – String length 10 – mandatory
    v. office – Integer – mandatory
    vi. description – String length 80 – mandatory

    i. {abbreviation}
    ii. {chair_name} – No professor can chair > one department.
    iii. {building, office} – No two departments can occupy the same room.
    iv. {description} – No two departments can have the same description.
    '''
    try:
        collection = db["departments"]

        unique_abbreviation: bool = False
        unique_chair: bool = False
        unique_location: bool = False
        unique_description: bool = False

        name: str = ''
        abbreviation: str = ''
        chairName: str = ''
        building: str = ''
        office: int = -1
        description: str = ''
        while not unique_abbreviation or not unique_chair or not unique_location or not unique_description:
            name = input("Department full name--> ")
            abbreviation = input("Department abbreviation--> ")
            chairName = input("Department chair name--> ")
            building = input("Building name--> ")
            office = int(input("Office number--> "))
            description = input("Department description--> ")
            abbr_count: int = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbr_count == 0
            if not unique_abbreviation:
                print("We already have a department by that abbreviation.  Try again.")
            if unique_abbreviation:
                chair_count = collection.count_documents({"chair_name": chairName})
                unique_chair = chair_count == 0
                if not unique_chair:
                    print("That professor is already a chair of a department.  Try again.")
                if unique_chair:
                    location_count = collection.count_documents({"building": building, "office": office})
                    unique_location = location_count == 0
                    if not unique_location:
                        print("There is already a department in that room.  Try again.")
                    if unique_location:
                        description_count = collection.count_documents({"description": description})
                        unique_description = description_count == 0
                        if not unique_description:
                            print("A department already has that description.  Try again.")

        # Build a new departments document preparatory to storing it
        department = {
            "name": name,
            "abbreviation": abbreviation,
            "chair_name": chairName,
            "building": building,
            "office": office,
            "description": description,
            "courses": [],  # Need to find a way to insert ID references for courses
            "majors": []
        }
        results = collection.insert_one(department)
        return results
    except Exception as e:
        print(e)
        add_department(db)


def add_course(db):
    '''
    courseNumber - Int
    courseName - String
    description - String
    units - Int


    {departmentAbbreviation, courseNumber}  
    {departmentAbbreviation, courseName}
    '''
    collection = db["courses"]
    department = select_department(db)
    abbreviation = department["abbreviation"]
    # number = input("Course number: ")
    # name = input("Course Name: ")
    # description = input("Course description: ")
    # unit = input("Course unit: ")

    unique_abbr_and_number: bool = False
    unique_abbr_and_name: False
    
    name: str = ''
    number: int = -1
    description = str = ''
    unit: int = -1

    while not unique_abbr_and_number or not unique_abbr_and_name:
        name = input("Course Name: ")
        number = int(input("Course number: "))
        description = input("Course description: ")
        unit = int(input("Course unit: "))
        num_count: int = collection.count_documents({"abbreviation": abbreviation, "number": number})
        unique_abbr_and_number = num_count == 0
        if not unique_abbr_and_number:
                print("We already have a course in that department with that number.  Try again.")
        if unique_abbr_and_number:
                name_count = collection.count_documents({"abbreviation": abbreviation, "name": name})
                unique_abbr_and_name = name_count == 0
    course = {
        "Department Abbreviation": abbreviation,
        "Course Number": number,
        "Course Name": name,
        "description": description,
        "units": unit,
        "sections": []
    }
    results = collection.insert_one(course)
    department_update_course(db, abbreviation, number, name, unit)
    return results
def department_update_course(db, abbreviation, number, name, unit):
    collection = db["courses"]
    found_course = collection.find_one(
        {"Department Abbreviation": abbreviation,
         "Course Number": number,
         "Course Name": name,
         "units": unit
         }
    )

    db["departments"].update_many(
        {'abbreviation': abbreviation},
        {'$push':
            {
                'courses': {
                    'Course ID': found_course["_id"],
                    'Course Name': found_course["Course Name"],
                    'Course Number': found_course["Course Number"],
                    'units': found_course["units"]
                }
            }
        }
    )

def add_section(db):
    '''
    sectionNumber - Integer
    semester - String
    sectionYear - Integer
    building - String
    room - Integer
    schedule - String
    startTime - Time
    instructor - String

    {couse, sectionNumber, semester, sectionYear}
    {semester, sectionyear, building, room, schedule, startTime}
    {semester, sectionYear, schedule, startTime, instructor}
    {semester, sectionYear, departmentAbbreviation, courseNumber, studentID}
    '''
    collection = db["sections"]
    course = select_course(db)
    departmentAbbreviation = course["Department Abbreviation"]
    courseNumber = course["Course Number"]
    # semester = input("Semester: ")
    # sectionYear = input("Year: ")
    # building = input("Building: ")
    # roomNumber = input("Room number: ")
    # schedule = input("Schedule: ")
    # startTime = input("start Time: ")
    # instructor = input("Instructor: ")
    unique_sem_and_year: bool = False
    unique_room: bool = False
    unique_schedule: bool = False
    unique_student: bool = False
    studentID = _id #hello everyone i don't know how this works

    while not unique_sem_and_year or not unique_room or not unique_schedule or not unique_student:
        sectionNumber = int(input("Section number: "))
        semester = input("Semester: ")
        sectionYear = input("Year: ")
        building = input("Building: ")
        roomNumber = input("Room number: ")
        schedule = input("Schedule: ")
        startTime = input("start Time: ")
        instructor = input("Instructor: ")
        sem_and_year_count: int = collection.count_documents({"course": course, "section_number": sectionNumber, "semester": semester, "year": sectionYear})
        unique_sem_and_year = sem_and_year_count == 0
        if not unique_sem_and_year:
            print("We already have a section with the same number going on in that school term. Try again.")
        if unique_sem_and_year:
            room_count: int = collection.count_documents({"semester": semester, "year": sectionYear, "building": building, "room": roomNumber, "schedule": schedule, "start_time": startTime})
            unique_room = room_count == 0
            if not unique_room:
                print("We already have a section with the same time going on in that location. Try again.")
            if unique_room:
                schedule_count: int = collection.count_documents({"semester": semester, "year": sectionYear, "schedule": schedule, "start_time": startTime, "instructor": instructor})
                unique_schedule = schedule_count == 0
                if not unique_schedule:
                    print("There's already an instructor with that start time. Try again")
                if unique_schedule:
                    student_count: int = collection.count_documents({"semester": semester, "year": sectionYear, "department_abbrevation": departmentAbbreviation, "course_number": courseNumber, "_id": studentID})
                    unique_student = student_count == 0
                    

    section = {
        "department_abbreviation": departmentAbbreviation,
        "course_number": courseNumber,
        "section_number": sectionNumber,
        "semester": semester,
        "year": sectionYear,
        "building": building,
        "room": roomNumber,
        "schedule": schedule,
        "start_time": startTime,
        "instruction": instructor
    }
    results = collection.insert_one(section)
    course_update_section(db, departmentAbbreviation, courseNumber, semester, sectionYear, building, roomNumber)
    return results

def course_update_section(db, departmentAbbreviation, courseNumber, semester, year, building, room):
    course = db["courses"]
    collection = db["sections"]
    found_section = collection.find_one(
        {"Department Abbreviation": departmentAbbreviation,
         "Course Number": courseNumber,
         "Semester": semester,
         "Year": year,
         "Building": building,
         "Room": room
         }
    )
    course.update_many(
        {'Department Abbreviation': departmentAbbreviation,
         'Course Number': courseNumber
         },
        {'$push':
            {
                'sections': {
                    'Section ID': found_section["_id"],
                    'Semester': found_section["Semester"],
                    'Year': found_section["Year"],
                    'Room': found_section["Room"],
                    'Schedule': found_section["Schedule"],
                    'Instructor': found_section["Instructor"]
                }
            }
        }
    )


def add_student(db):
    '''
    lastName: String
    firstName: String
    email: String


    {lastName, firstName}
    {email}
    {_id} <-- aaccording to my research this should already be unique but if im wrong then im boo boo the fool
    '''
    collection = db["students"]
    # lastName = input("Student last name: ")
    # firstName = input("Student first name: ")
    # email = input("Student email: ")

    unique_name: bool = False
    unique_email: bool = False

    lastName: str = ''
    firstName: str = ''
    email: str = ''

    while not unique_name or not unique_email:
        lastName = input("Student last name: ")
        firstName = input("Student first name: ")
        email = input("Student email: ")
        name_count: int = collection.count_documents({"lastName": lastName, "firstName": firstName})
        unique_name = name_count == 0
        if not unique_name:
            print("There is already a student by that name. Try again")
        if unique_name:
            email_count = collection.count_documents({"email": email})
            unique_email = email_count == 0
            if not unique_email:
                print("There is already a student with that email address. Try again")

    student = {
        "Last Name": lastName,
        "First Name": firstName,
        "email": email,
        "major": []
    }

    results = collection.insert_one(student)
    return results

def add_major(db):
    collection = db["majors"]
    department = select_department(db)
    departmentAbbreviation = department["abbreviation"]
    majorName = input("name: ")
    description = input("description: ")

    major = {
        "Department Abbreviation": departmentAbbreviation,
        "Major Name": majorName,
        "Description": description,
        "Students": []
    }

    results = collection.insert_one(major)
    department_update_major(db, departmentAbbreviation, majorName)
    return results

def add_student_major(db):
    student = {}
    major = {}
    unique_student_major = False
    while not unique_student_major:
        student = select_student(db)
        major = select_major(db)

        student_major_count = 0
        for object in student["major"]:
            if object["Major ID"] == major["_id"]:
                student_major_count += 1
        unique_student_major = student_major_count == 0
        if not unique_student_major:
            print("That student already has that major.  Try again.")
    db["students"].update_many(
        {'_id': student["_id"]},
        {'$push':
             {
                 "major":{
                     'Major ID': major["_id"],
                     'Major Name': major["Major Name"]
                 }
             }
        }
    )
    db["majors"].update_many(
        {'_id': major["_id"]},
        {'$push':
             {
                 "Students":{
                     'Student ID': student["_id"],
                     'Last Name': student["Last Name"],
                     'First Name': student["First Name"]
                 }
             }
        }
    )

def add_major_student(db):
    major = {}
    student = {}
    unique_student_major = False

    while not unique_student_major:
        major = select_major(db)
        student = select_student(db)

        student_major_count = 0
        for object in major["Students"]:
            if object["Student ID"] == student["_id"]:
                student_major_count += 1
        unique_student_major = student_major_count == 0
        if not unique_student_major:
            print("That major already has that student.  Try again.")
    db["students"].update_many(
        {'_id': student["_id"]},
        {'$push':
            {
                "major": {
                    'Major ID': major["_id"],
                    'Major Name': major["Major Name"]
                }
            }
        }
    )
    db["majors"].update_many(
        {'_id': major["_id"]},
        {'$push':
            {
                "Students": {
                    'Student ID': student["_id"],
                    'Last Name': student["Last Name"],
                    'First Name': student["First Name"]
                }
            }
        }
    )
def department_update_major(db, departmentAbbreviation, majorName):
    collection = db["majors"]
    found_major= collection.find_one(
        {"Department Abbreviation": departmentAbbreviation,
         "Major Name": majorName
         }
    )
    db["departments"].update_many(
        {'abbreviation': departmentAbbreviation},
        {'$push':
            {
                "majors": {
                    'Major ID': found_major["_id"],
                    'Major Name': found_major["Major Name"]
                }
            }
        }
    )

def add_enrollment(db):
    collection = db["enrollments"]
    student = select_student(db)
    section = select_section(db)

    enrollment = {
        "Student ID": student["_id"],
        "Section ID": section["_id"],
        "Student": [],
        "Section": []
    }

    results = collection.insert_one(enrollment)
    return results

def select_department(db):
    collection = db["departments"]

    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    found_department = collection.find_one({"abbreviation": abbreviation})
    return found_department

def select_course(db):
    collection = db["courses"]

    found: bool = False
    departmentAbbreviation: str = ''
    courseNumber: str = ''
    while not found:
        departmentAbbreviation = input("Enter the department abbreviation: ")
        courseNumber = input("Enter the course number: ")

        course_count = collection.count_documents(
            {
                "Department Abbreviation": departmentAbbreviation,
                "Course Number": courseNumber
            }
        )
        found = course_count == 1
        if not found:
            print("No courses were found.  Try again")
    found_course = collection.find_one(
        {"Department Abbreviation": departmentAbbreviation,
         "Course Number": courseNumber
         }
    )
    return found_course

def select_student(db):
    collection = db["students"]

    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name-->")
        firstName = input("Student's first name -->")

        student_count = collection.count_documents(
            {
                "Last Name": lastName,
                "First Name": firstName
            }
        )
        found = student_count == 1
        if not found:
            print("No student found with that name.  Try again.")
    found_student = collection.find_one(
        {"Last Name": lastName,
         "First Name": firstName
         }
    )
    return found_student

def select_major(db):
    collection = db["majors"]

    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter major name: ")

        major_count = collection.count_documents(
            {
                "Major Name": name
            }
        )
        found = major_count == 1
        if not found:
            print("No major found with that name.  Please try again")

    found_major = collection.find_one(
        {
            "Major Name": name
        }
    )
    return found_major

def select_section(db):  # TODO
    #NEED TO DOUBLE CHECK IF THIS IS THE CORRECT WAY TO SELECT SECTION
    collection = db["sections"]

    found: bool = False
    while not found:
        print("Please provide the course that this section belongs to:")
        course = select_course(db)
        semester = input("semester: ")
        sectionYear = input("Section year: ")
        section_count = collection.count_documents(
            {
                "Department Abbreviation": course["Department Abbreviation"],
                "Course Number": course["Course Number"],
                "Year": sectionYear,
                "Semester": semester
            }
        )
        found = section_count == 1
        if not found:
            print("No section found by that course, section#, semester & year.  Try again.")
    found_section = collection.find_one(
        {
            "Department Abbreviation": course["Department Abbreviation"],
            "Course Number": course["Course Number"],
            "Year": sectionYear,
            "Semester": semester
        }
    )
    return found_section

'''
I blatantly stole this from professor's subschema code.
Looks useful tho.
God I hope someone reads this documentation
'''
def drop_collection(schema_ref, collection_name: str):
    """
    Little utility for dropping collections and letting the user know.
    :param schema_ref:          The reference to the current schema.
    :param collection_name:     The name of the collection to drop within that schema.
    :return:                    None
    """
    if collection_name in schema_ref.list_collection_names():
        print(f'Dropping collection: {collection_name}')
        schema_ref[collection_name].drop()

def delete_department(db):
    department = select_department(db)

    departments = db["departments"]
    deleted = departments.delete_one({"_id": department["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments.")

def delete_course(db):
    course = select_course(db)
    if len(course["sections"]) != 0:
        print("Can't delete course because there are some sections in this course!")
        return
    courses = db["courses"]

    deleted = courses.delete_one({"_id": course["_id"]})
    db["departments"].update_many(
        {'abbreviation': course["Department Abbreviation"]},
        {'$pull':
            {
                'courses': {
                    'Course ID': course["_id"]
                }
            }
        }
    )
    print(f"We just deleted: {deleted.deleted_count} courses")

def delete_student(db):
    student = select_student(db)
    students = db["students"]
    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} students")

def delete_major(db):
    major = select_major(db)

    majors = db["majors"]
    deleted = majors.delete_one({"_id": major["_id"]})
    db["departments"].update_many(
        {'abbreviation': major["Department Abbreviation"]},
        {'$pull':
            {
                'majors': {
                    'Major ID': major["_id"]
                }
            }
        }
    )
    print(f"We just deleted: {deleted.deleted_count} majors.")

def delete_student_major(db):
    student = select_student(db)
    major = select_major(db)

    db["students"].update_many(
        {
            '_id': student["_id"]
        },
        {
            '$pull':
                {
                    'major':{
                        'Major ID': major["_id"]
                    }
                }
        }
    )
    db["majors"].update_many(
        {
            '_id': major["_id"]
        },
        {
            '$pull':
                {
                    'Students':{
                        'Student ID': student["_id"]
                    }
                }
        }
    )


def delete_major_student(db):
    major = select_major(db)
    student = select_student(db)

    db["majors"].update_many(
        {
            '_id': major["_id"]
        },
        {
            '$pull':
                {
                    'Students': {
                        'Student ID': student["_id"]
                    }
                }
        }
    )
    db["students"].update_many(
        {
            '_id': student["_id"]
        },
        {
            '$pull':
                {
                    'major': {
                        'Major ID': major["_id"]
                    }
                }
        }
    )

def delete_section(db): #TODO
    section = select_section(db)
    sections = db["sections"]
    db["courses"].update_many(
        {
            'Department Abbreviation': section["Department Abbreviation"],
            'Course Number': section["Course Number"]
        },
        {
            '$pull':
                {
                    'sections':{
                        'Section ID': section["_id"]
                    }
                }
        }
    )
    deleted = sections.delete_one({"_id": section["_id"]})
    print(f"We just deleted: {deleted.deleted_count} sections.")

def list_departments(db):
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING)])
    for department in departments:
        pprint(department)

def list_course(db):
    courses = db["courses"].find({}).sort([("Course Name", pymongo.ASCENDING)])
    for course in courses:
        pprint(course)

def list_major(db):
    majors = db["majors"].find({}).sort([("Major Name", pymongo.ASCENDING)])
    for major in majors:
        pprint(major)

def list_student(db):
    students = db["students"].find({}).sort([("Last Name", pymongo.ASCENDING)])
    for student in students:
        pprint(student)

def list_section(db):
    sections = db["sections"].find({}).sort([("Last Name", pymongo.ASCENDING)])
    for section in sections:
        pprint(section)

def list_student_major(db):
    student = select_student(db)
    for i in student["major"]:
        print(i)

def list_major_student(db):
    major = select_major(db)
    for i in major["Students"]:
        print(i)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)

department_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'description': "An organization that offers one or more degree programs within a college, "
                           "within a university",
            'required': ["name", "abbreviation", "chair_name", "building", "office", "description"],
            'properties': {
                'name': {
                    'bsonType': "string",
                    'minLength': 10,
                    'maxLength': 50
                },
                'abbreviation': {
                    'bsonType': "string",
                    'maxLength': 6,
                },
                'chair_name': {
                    'bsonType': "string",
                    'maxLength': 80,
                },
                'building': {
                    'bsonType': "string",
                    'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"]
                },
                'office': {
                    'bsonType': "int"
                },
                'description': {
                    'bsonType': "string",
                    'minLength': 10,
                    'maxLength': 80
                }
            }
        }
    }
}

sections_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'description': "An organization that offers one or more degree programs within a college, "
                           "within a university",
            'required': ["sectionNumber", "semester", "sectionYear", "building", "room", "schedule", "startTime", "instructor"],
            'properties': {
                'sectionNumber': {
                    'bsonType': "int",
                },
                'semester': {
                    'bsonType': "string",
                    'enum': ["Fall", "Spring", "Summer I", "Summer II", "Summer III", "Winter"]
                },
                'sectionYear': {
                    'bsonType': "int",
                },
                'building': {
                    'bsonType': "string",
                    'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"]
                },
                'room': {
                    'bsonType': "int",
                    'minLength': 0,
                    'maxLength': 1000
                },
                'schedule': {
                    'bsonType': "string",
                    'enum': ["MW", "TuTH", "MWF", "F", "S"]
                },
                'startTime': {
                    'bsonType': "datetime",
                },
                'instructor': {
                    'bsonType': "string",
                }
            }
        }
    }
}

enrollment_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'description': "An organization that offers one or more degree programs within a college, "
                           "within a university",
            # 'required': ["name", "abbreviation", "chair_name", "building", "office", "description"],
            'required': ['category_data'],
            'properties': {
                'category_data': {
                    'oneOf':[
                        {
                            #PassFail
                            'bsonType': 'object',
                            'required': ['applicationDate'],
                            'additionalProperties': False,
                            'properties': {
                                'applicationDate' : {
                                    'bsonType': 'date',
                                    'min': Date()
                                }
                            }
                        }, 

                        {
                            #LetterGrade
                            'bsonType': 'object',
                            'required': ['minSatisfactory'],
                            'additionalProperties': False,
                            'properties': {
                                'minSatisfactory' : {
                                    'bsonType': 'String',
                                    'enum': ["A", "B", "C"]
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    cluster = os.getenv("url")  # Change to your MongoDB url thingy
    client = MongoClient(cluster)
    db = client["CECS323Database"]  # Change to your database

    departments = db["departments"]
    courses = db["courses"]
    majors = db["majors"]
    sections = db["sections"]
    students = db["students"]
    # Ask if this is how you add the department_validator
    db.command('collMod', 'departments', **department_validator)
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")

    departments_index = departments.index_information()
    if 'departments_name' in departments_index.keys():
        print("name index present")
    else:
        departments.create_index([('name', pymongo.ASCENDING)], unique=True, name="departments_name")
    if 'departments_abbreviation' in departments_index.keys():
        print("abbreviation index present.")
    else:
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name="departments_abbreviation")
    if 'departments_chair_name' in departments_index.keys():
        print("chair name index present.")
    else:
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name="departments_chair_name")
    if 'departments_building_and_office' in departments_index.keys():
        print("building and office index present.")
    else:
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)], unique=True,
                                 name="departments_building_and_office")
    if 'departments_description' in departments_index.keys():
        print("description index present.")
    else:
        departments.create_index([('description', pymongo.ASCENDING)], unique=True, name="departments_description")
    if 'department_courses' in departments_index.keys():
        print("departmentCourses index present")
    else:
        departments.create_index([('courses', pymongo.ASCENDING)], name="department_courses")

    courses_index = courses.index_information()
    if 'course_name' in courses_index.keys():
        print("courseName index present")
    else:
        courses.create_index([('Course Name', pymongo.ASCENDING)], unique=True, name="course_name")
    if 'course_number' in courses.index_information():
        print("courseNumber index present")
    else:
        courses.create_index([('Course Number', pymongo.ASCENDING)], unique=True, name="course_number")

    students_index = students.index_information()
    if 'last_name' in students_index.keys():
        print("lastName in index present")
    else:
        students.create_index([('Last Name', pymongo.ASCENDING)], name="last_name")
    if 'first_name' in students_index.keys():
        print("firstname in index present")
    else:
        students.create_index([('First Name', pymongo.ASCENDING)], name="first_name")

    pprint(departments.index_information())
    pprint(courses.index_information())
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
