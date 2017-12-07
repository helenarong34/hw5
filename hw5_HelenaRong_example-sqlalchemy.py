
# Using SQLAlchemy to Talk to a Database
# =====================
# SqlAlchemy helps you use a database to store and retrieve information from python.  It abstracts the specific storage engine from te way you use it - so it doesn't care if you end up using MySQL, SQLite, or whatever else. In addition, you can use core and the object-relational mapper (ORM) to avoid writing any SQL at all.  The [SQLAlchemy homepage](http://www.sqlalchemy.org/) has lots of good examples and full documentation.


from sqlalchemy import *
import datetime
import mediacloud, datetime



# The core library generates SQL for you.  Read more about it on their [expression language tutorial page](http://docs.sqlalchemy.org/en/rel_1_0/core/index.html). Below are some basic examples.

# ### Creating a Table
# Read more about [defining and creating tables](http://docs.sqlalchemy.org/en/rel_1_0/core/tutorial.html#define-and-create-tables).


# add `echo=True` to see log statements of all the SQL that is generated
engine = create_engine('sqlite:///:memory:',echo=True) # just save the db in memory for now (ie. not on disk)
metadata = MetaData()
# define a table to use
queries = Table('queries', metadata,
    Column('id', Integer, primary_key=True),
    Column('keywords', String(400), nullable=False),
    Column('count', Integer, default=0),
)
metadata.create_all(engine) # and create the tables in the database




insert_stmt = queries.insert()
str(insert_stmt) # see an example of what this will do




mc = mediacloud.api.MediaCloud('4923e5782ddbc72d23d4a57cfcf2176efbaef3b18677b4ae7eb7581e8356e924')
res1 = mc.sentenceCount('( Trump)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
res2 = mc.sentenceCount('( Clinton)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
print (res1['count'])
print (res2['count'])


insert_stmt = queries.insert().values(keywords="Trump", count = res1['count'])



str(insert_stmt)


db_conn = engine.connect()
result = db_conn.execute(insert_stmt)
result.inserted_primary_key # print out the primary key it was assigned

insert_stmt = queries.insert().values(keywords="Hilary",count=res2['count'])
result = db_conn.execute(insert_stmt)
result.inserted_primary_key # print out the primary key it was assigned


# ### Retrieving Data
# Read more about using [SQL select statments](http://docs.sqlalchemy.org/en/rel_1_0/core/tutorial.html#selecting).

from sqlalchemy.sql import select
select_stmt = select([queries])
results = db_conn.execute(select_stmt)
for row in results:
    print(row)




select_stmt = select([queries]).where(queries.c.id==1)
for row in db_conn.execute(select_stmt):
    print(row)



select_stmt = select([queries]).where(queries.c.keywords.like('p%'))
for row in db_conn.execute(select_stmt):
    print(row)


# ## ORM
# You can use their ORM library to handle the translation into full-fledged python objects.  This can help you build the Model for you [MVC](https://en.wikipedia.org/wiki/Model–view–controller) solution.


import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


# ### Creating a class mapping
# Read more about [creating a mapping](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#declare-a-mapping).


class Query(Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True)
    keywords = Column(String(400))
    count = Column(Integer,default=0)
    def __repr__(self):
        return "<Query(keywords='%s',count ='%s') >" % (self.keywords, self.count)
Query.__table__


# ### Creating a connection and session
# Read more about [creating this stuff](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#creating-a-session).



engine = create_engine('sqlite:///:memory:') # just save the db in memory for now (ie. not on disk)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
my_session = Session()


# ### Inserting Data
# Read more about [inserting data with an ORM](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#adding-new-objects).


query = Query(keywords="Trump",count=res1['count'])
query


my_session.add(query)
my_session.commit()
query.id


# ### Retrieving Data
# Read more about [retrieving data from the db](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#querying) via an ORM class.


for q in my_session.query(Query):
    print (q)



query1 = Query(keywords="robot")
query2 = Query(keywords="puppy")
my_session.add_all([query1,query2])
my_session.commit()



for q in my_session.query(Query):
    print (q)


for q in my_session.query(Query).filter(Query.keywords.like('r%')):
    print (q)





