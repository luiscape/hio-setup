#!/usr/bin/python
# -*- coding: utf-8 -*-

# system
import os
import sys
dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(dir, 'scripts'))

# testing
import mock
import unittest
from mock import patch

# program
import setup_db as SB
import rethinkdb as r
import config as Config

class CheckConfigurationWorks(unittest.TestCase):
  '''Unit tests for the configuration scripts.'''

  ## Object type tests.
  def test_config_is_dict(self):
    d = Config.LoadConfig('config.json')
    assert type(d) is dict

  def test_config_returns_a_table_dict(self):
    d = Config.LoadConfig('config.json')
    t = d['database'][0]['tables']
    assert type(t) is list



  ## Object atributes tests.
  def test_config_returns_right_n_tables(self):
    d = Config.LoadConfig('config.json')
    t = d['database'][0]['tables']
    n = 3 
    assert len(t) == n


  ## Output tests.
  def test_right_tables_in_config_file(self):
    d = Config.LoadConfig('config.json')
    t = d['database'][0]['tables']
    names = []
    for table in t:
      names.append(table['id'])
    assert 'values' in names
    assert 'metrics' in names
    assert 'values' in names


class CheckDatabaseCreationWorks(unittest.TestCase):
  '''Unit tests for the setup of RethinkDB.'''

  ## Testing connection.
  def test_db_connection(self):
    db = Config.LoadConfig()['database'][0]
    assert SB.DbConnection(db['port_dev'], db['host_dev']) != False

  ## Testing db setup.
  def test_table_creation(self):
    database_config = Config.LoadConfig()['database'][0]
    assert SB.CreateDatabase('hio_main') == True

  # def test_table_drop(self):
  #   assert SB.DropTable('test') == True


  def test_create_table_works(self):
    db = Config.LoadConfig()['database'][0]
    assert SB.CreateTables(db) != False


  def test_that_data_load_function_works(self):
    db = Config.LoadConfig()['database'][0]
    assert SB.LoadTestData('ebola-data-db-format.csv', db) == True

  ## Testing results.
  def test_db_exists(self):
    db = Config.LoadConfig()['database'][0]
    conn = SB.DbConnection(db['port_dev'], db['host_dev'])
    l = r.db_list().run(conn)
    assert db['name'] in l

