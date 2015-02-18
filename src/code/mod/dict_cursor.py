#!/usr/bin/env jython
from com.ziclix.python.sql import zxJDBC # DB connection

def dict_cursor(cursor):
	"""Takes cursor as an input, following execution of a query, returns results as a list of dicts"""
	# iterate over rows in cursor.description, pulling first element
	description = [x[0] for x in cursor.description] 
	l = []
	for row in cursor: # iterate over rows in cursor
		d = dict(zip(description, row))
#	yield dict(zip(description, row))  # This yields an iterator.  Doesn't actually run until needed.
		l.append(d)
	return l


# def dict_cursor2(cursor):
#     description = [x[0] for x in cursor.description]
# 	dout = ()
#     for row in cursor:
#         #yield dict(zip(description, row))  # Not sure that yield is the best option here, as produces a 
# 		#dout.append(dout[description]=row

def get_cursor(user, pwd):
	conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit", user, pwd, "org.gjt.mm.mysql.Driver") # For local testing
	cursor =  conn.cursor()
	return cursor

def test(user, pwd):
	conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit", user, pwd, "org.gjt.mm.mysql.Driver") # For local testing
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM flycircuit_driver_map")
	dc = dict_cursor(cursor)
	for d in dc:
		print d.items()

	

