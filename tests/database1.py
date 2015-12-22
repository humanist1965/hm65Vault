import unittest
import sys
import os

def addRootDirToSysPath():
  cwd = os.getcwd()
  pos = cwd.find("hm65Vault")
  pos += len("hm65Vault")
  cwd = cwd[0:pos]
  sys.path.insert(0,cwd)
addRootDirToSysPath()

import LocalVault.Database as data

class DatabaseTest2(unittest.TestCase):

  def setUp(self):
      pass

  def tearDown(self):
      pass

  def assertEqualUnordered(self, L1, L2):
    """
    Given two unordered lists of items will check to see if they have the same items
    """
    # Was doing the below originally but does not give enough info if there is a problem
    #self.assertTrue( len(L1) == len(L2) and sorted(L1) == sorted(L2))
    self.assertTrue(len(L1) == len(L2))
    self.assertEqual(sorted(L1),sorted(L2))

  def test_creationDeletion(self):
      db = data.Database()
      db.deleteDatabase()
      self.assertFalse(db.databaseExists())
      db.createDatabase()
      self.assertTrue(db.databaseExists())

  def test_setInsert(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      db.set("mk1", "val1")
      db.set("mk2", "val2")
      db.set("mk3", "val3")
      mk1 = db.get("mk1")[1]
      mk2 = db.get("mk2")[1]
      mk3 = db.get("mk3")[1]
      self.assertEqual([mk1,mk2,mk3],["val1","val2","val3"])

  def test_setUpdate(self):
      """
      If the key exists in the database already then an update will be performed and not an insert
      """
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      db.set("mk1", "val1")
      db.set("mk2", "val2")
      db.set("mk1", "val1b")
      mk1 = db.get("mk1")[1]
      mk2 = db.get("mk2")[1]
      self.assertEqual([mk1,mk2],["val1b","val2"])

  def test_setInsertFromDict(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      d = { "mk1": "val1",
            "mk2": "val2",
            "mk3": "val3"}
      db.set(d)
      mk1 = db.get("mk1")[1]
      mk2 = db.get("mk2")[1]
      mk3 = db.get("mk3")[1]
      self.assertEqual([mk1,mk2,mk3],["val1","val2","val3"])

  def test_list(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      d = { "mk1": "val1",
            "mk2": "val2",
            "mk3": "val3"}
      db.set(d)
      
      results = db.list("mk")
      # The results will not necessarily be in the order that you set them
      self.assertEqualUnordered(results,[("mk1","val1"), ("mk2","val2"), ("mk3","val3")])

      # If you include a % is patToMatch then a % will not be appended at the end
      results = db.list("%k")
      self.assertTrue(len(results)==0)
      # If you want to find all keys with "k" anywhere in key
      results = db.list("%k%")
      self.assertEqualUnordered(results,[("mk1","val1"), ("mk2","val2"), ("mk3","val3")])

  def test_moreComplexKeyInserts(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      d = { "root.customer[1].user[1]": "{f1:val1.1,f2:val1.2}",
            "root.customer[2].user[1]": "{f1:val2.1,f2:val2.2}",
            "root.customer[3].user[1]": "{f1:val3.1,f2:val3.2}",
            "root.customer[4].user[uniqueUserId]": "{f1:val3.1,f2:val3.2}"}
      db.set(d)
      results = db.list("root.customer[1]")
      self.assertEqualUnordered(results,[("root.customer[1].user[1]","{f1:val1.1,f2:val1.2}")])
      results = db.list("root.customer")
      self.assertEqualUnordered(results,[("root.customer[1].user[1]", "{f1:val1.1,f2:val1.2}"),
            ("root.customer[2].user[1]", "{f1:val2.1,f2:val2.2}"),
            ("root.customer[3].user[1]", "{f1:val3.1,f2:val3.2}"),
            ("root.customer[4].user[uniqueUserId]", "{f1:val3.1,f2:val3.2}")])
      results = db.list("%user[uniqueUserId]%")
      self.assertEqualUnordered(results,[("root.customer[4].user[uniqueUserId]", "{f1:val3.1,f2:val3.2}")])

  def test_getResultSet(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      self.assertTrue(db.getResultSet("root.customer"))


if __name__ == '__main__':
  # normally you would run as part of a test runner but if you just want to exrecise the test in this file
  unittest.main()