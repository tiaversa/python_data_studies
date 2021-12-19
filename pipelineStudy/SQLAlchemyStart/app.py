# Extract-Transform-Load ETL
# this is a project to better understand how the ETL process works



# Utilzing python to create a  database and tables to populate that database
# libraries to deal with sqlalquemy
from requests.sessions import session
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import *
from sqlalchemy.sql.functions import user
#libraries for the transformation
from datetime import datetime, timedelta
from random import randint



#first important thing create a connection to the database
engine = create_engine('sqlite:///demo.db')

Base = declarative_base()

# molding the first table
class Users(Base):
    __tablename__ = 'users'
    UserId = Column(Integer, primary_key=True) #first column is populated with a primary key
    Title = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Email = Column(String)
    Username = Column(String)
    DOB = Column(DateTime)

# molding the second table
class Uploads(Base):
    __tablename__ = 'uploads'
    UploadId = Column(Integer, primary_key=True)
    UserId = Column(Integer)
    Title = Column(String)
    Body = Column(String)
    Timestamp = Column(DateTime)

#actually creating the tables (with check to make sure the tables are only created if they do not already exist)
Users.__table__.create(bind=engine, checkfirst=True)
Uploads.__table__.create(bind=engine, checkfirst=True)


# !!! Extracting !!!
# Extracting the raw data from it's source
#this can come from in-house or third-party API or to read data logged in a CSV file.

#in this example we use two APIs to simulate data for the fictional blogging platform described above.

import requests
#populating the first table with a request from a api
url = 'https://randomuser.me/api/?results=10' #adding the font to a variable is a better way to organize the files
users_json = requests.get(url).json()

#populating the second table with a request from a api
url2 = 'https://jsonplaceholder.typicode.com/posts/'
uploads_json = requests.get(url2).json()
# the data is currently held in two objects in JSON format


# !!! Transforming !!!
# usually the JSON objects have more information then necessary.
# we have to transform the data from its current nested JSON forat to a flat format that can be safely written 
# to the database without errors

users, uploads = [], [] # creating and initialazing 
for i, result in enumerate(users_json['results']): 
    row = {} #making a dictionnary containing each information provided for that row
    row['UserId'] = i
    row['Title'] = result['name']['title']
    row['FirstName'] = result['name']['first']
    row['LastName'] = result['name']['last']
    row['Email'] = result['email']
    row['Username'] = result['login']['username']
    #dob = datetime.strptime(result['dob'],'%Y-%m-%d %H:%M:%S')
    #row['DOB'] = dob.date()
    #add the new row to the table with the information on the dictionary
    users.append(row)

for result in uploads_json:
    row = {}
    row['UploadId'] = result['id']
    row['UserId'] = result['userId']
    row['Title'] = result['title']
    row['Body'] = result['body']
    delta = timedelta(seconds=randint(1,86400))
    row['Timestamp']= datetime.now() - delta
    uploads.append(row)


# !!! Load !!!
# session API makes loading straightfoward
# Create a new seesion object, add rows to it, then merges and commits them to the database
Session = sessionmaker(bind=engine) #generate a new session class
session = Session()

for user in users: #loop to iterate through the users list previewsly created(the already clean one)
    row = Users(**user) #** unpacks what is in the dictionary from {'a':1,'b':2} to (a=1,b=2)
    session.add(row) # adding the object to the current session

for upload in uploads:
    row = Uploads(**upload)
    session.add(row)

session.commit() # commit the transation to the database


# !!! Aggregating !!!
# creating an aggregated table showing how many articles each user has posted, and the time they were last active
class UploadCounts(Base): #creating the new table
    __tablename__ = 'upload_counts' 
    UserId = Column(Integer, primary_key=True)
    LastActive = Column(DateTime)
    PostCount = Column(Integer)

UploadCounts.__table__.create(bind = engine, checkfirst = True)
# table with 3 columns, for each usedId, it will store the timestamp of when they were last active and a count of how
    #many posts they have uploaded
    # In SQL: INSERT INTO upload_counts
    #           SELECT UserId, MAX (Timestamp) AS LastActive, COUNT (UploadId) As PostCount
    #            FROM uploads GROUNP BY 1;

    #SQLAlchemy
connection = engine.connect()

query = select([Uploads.UserID, 
    func.max(Uploads.Timestamp).label('LastActive'), 
    func.count(Uploads.Upload).label('PostCount')]).\
    group_by('UserID')

results = connection.execute(query)

for result in results:
    row = UploadCounts(**result)
    session.add(row)

session.commit()