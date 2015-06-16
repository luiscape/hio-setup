#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import rethinkdb as r
from config import LoadConfig

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

def DbConnection(port, host):  # default
  '''Connecting to the RethinkDb instance.'''
  try:
    conn = r.connect("localhost", port).repl()
    return conn

  except Exception as e:
    print "Could not connect to RethinkDb on port %s" % port
    return False


def DropTable(name, conn):
  '''Dropping tables -- for clean-up.'''

  try:
    r.db_drop(name).run(conn)
    return True

  except Exception as e:
    print "Could not drop table `%s`" % name
    return False


def CreateDatabase(name, conn, v = False):
  '''Creating a database.'''

  if v:
    print "Creating database ..."

  l = r.db_list().run(conn)

  if name in l:
    if v:
      print "Database `%s` already exists." % name
    return True

  try:
    r.db_create(name).run(conn)
    return True

  except Exception as e:
    print "Could not create database."
    return False


def CreateTables(db, conn, v = False):
  '''Creating tables in database.'''

  if v:
    print "Creating tables ..."

  l = r.db(db['name']).table_list().run(conn)
  tables = db['tables']
  for t in tables:

    if t['id'] in l:
      if v:
        print "Table `%s` already exists." % t['id']
      continue

    else:
      try:
        r.db(db['name']).table_create(t['id']).run(conn)
        if v:
          print "Table `%s` created." % t['id']

      except Exception as e:
        print "Could not create table `%s`." % t['id']
        return False


def LoadTestData(file, db, conn, v = False):
  '''Loading test data into the database.'''

  ## Loading data.
  data_dir = os.path.split(dir)[0]
  path = os.path.join(data_dir, 'tests', 'data', file)
  print path
  try:
    with open(path) as csv_file:
      data = csv.DictReader(csv_file)
      test_data = []
      for row in data:
        test_data.append(row)

  except Exception as e:
    print "Couldn't load test data."
    return False


  ## Storing in db.
  try:
    # Checking for existing records.
    n = r.db(db['name']).table('values').count().run(conn)
    if n > 0:
      if v:
        print "Data already in db. Deleting ..."
      r.db(db['name']).table('values').delete().run(conn)

    r.db(db['name']).table('values').insert(test_data).run(conn)
    return True

  except Exception as e:
    print "Could not insert data into database."
    return False



def Main(t = False, v = True):
  '''Wrapper.'''

  #
  # Load configuration.
  #
  db = LoadConfig()['database'][0]

  if db != False:
    conn = DbConnection(db['port_dev'], db['host_dev'])

  else:
    print 'Could not connect to RethingDb instance.'
    return False

  #
  # Create database and tables.
  #
  CreateDatabase(db['name'], conn=conn)
  CreateTables(db, conn=conn)

  if t:
    LoadTestData(file='ebola-data-db-format.csv', conn=conn, db=db)

  if v:
    print "Setup ran successfully."
    return True



if __name__ == '__main__':
  Main()
