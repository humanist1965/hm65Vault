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
import LocalVault.Vault as vault

class VaultTest(unittest.TestCase):

  def setUp(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()

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

  def test_addItem(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      item = {
        'url': 'www.google.com',
        'title': 'test title',
        'notes': '',
        'to_read': False,
        'tags': 'tag1 tag2 tag3'
      }
      vt = vault.hm65Vault()
      key = vt.addItem(item)
      self.assertTrue(key == "191347bfe55d0ca9a574db77bc8648275ce258461450e793528e0cc6d2dcf8f5")
      item2 = vt.getItem(key)
      self.assertEqual(item, item2)
      tagCount = [vt.tagCount("tag1"), vt.tagCount("tag2"), vt.tagCount("tag3")]
      self.assertEqual(tagCount, ['1','1','1'])

  def test_addItem2(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      item = {
        'url': 'www.google.com',
        'title': 'test title',
        'notes': '',
        'to_read': False,
        'tags': 'tag1 tag2 tag3'
      }
      item2 = {
        'url': 'www.google.com',
        'title': 'xxxxtest title',
        'notes': 'xxx',
        'to_read': False,
        'tags': 'tag1 tag2 tag3'
      }
      vt = vault.hm65Vault()
      key = vt.addItem(item)
      key2 = vt.addItem(item2)
      self.assertEqual(key,key2)
      tagCount = [vt.tagCount("tag1"), vt.tagCount("tag2"), vt.tagCount("tag3")]
      self.assertEqual(tagCount, ['1','1','1'])

  def test_addItem3(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      item = {
        'url': 'www.google.com',
        'title': 'test title',
        'notes': '',
        'to_read': False,
        'tags': 'tag1 tag2 tag3'
      }
      item2 = {
        'url': 'www.google2.com',
        'title': 'xxxxtest title',
        'notes': 'xxx',
        'to_read': False,
        'tags': 'tag1 tag2 tag3'
      }
      vt = vault.hm65Vault()
      key = vt.addItem(item)
      key2 = vt.addItem(item2)
      self.assertFalse(key==key2)
      tagCount = [vt.tagCount("tag1"), vt.tagCount("tag2"), vt.tagCount("tag3")]
      self.assertEqual(tagCount, ['2','2','2'])

  def test_listItems(self):
      db = data.Database()
      db.deleteDatabase()
      db.createDatabase()
      item1 = {
        'url': 'www.google.com',
        'title': 'test title',
        'notes': '',
        'to_read': False,
        'tags': 'tag1'
      }
      item2 = {
        'url': 'www.google2.com',
        'title': 'xxxxtest title',
        'notes': 'xxx',
        'to_read': False,
        'tags': 'tag2'
      }
      item3 = {
        'url': 'www.google3.com',
        'title': 'xxxxtest title',
        'notes': 'xxx',
        'to_read': False,
        'tags': 'tag3 tag1 tag2'
      }
      vt = vault.hm65Vault()
      key1 = vt.addItem(item1)
      key2 = vt.addItem(item2)
      key3 = vt.addItem(item3)
      res = vt.listItems("tag1")
      expected = {key1:1,key3:1}
      self.assertEqual(res,expected)
      res = vt.listItems("tag2")
      expected = {key2:1,key3:1}
      self.assertEqual(res,expected)
      res = vt.listItems("tag3")
      expected = {key3:1}
      self.assertEqual(res,expected)
      res = vt.listItems("tag3 tag1")
      expected = {key3:1}
      self.assertEqual(res,expected)
  

if __name__ == '__main__':
  # normally you would run as part of a test runner but if you just want to exrecise the test in this file
  unittest.main()