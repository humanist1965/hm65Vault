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

class VaultTest2(unittest.TestCase):

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
      item4 = {
        'url': 'www.google3.com',
        'title': 'xxxxtest title',
        'notes': 'xxx',
        'to_read': False,
        'tags': 'tag10 tag11 tag7 tag8 tag9'
      }
      item5 = {
        'url': 'www.google3.com',
        'title': 'xxxxtest title',
        'notes': 'xxx',
        'to_read': False,
        'tags': 'tag12 tag13 tag7'
      }
      vt = vault.hm65Vault()
      key1 = vt.addItem(item1)
      key2 = vt.addItem(item2)
      key3 = vt.addItem(item3)
      key4 = vt.addItem(item4)
      key5 = vt.addItem(item5)
      self.assertEqual(vt.listTags("t"),['tag1', 'tag10', 'tag11', 'tag12', 'tag13', 'tag2', 'tag3', 'tag7', 'tag8', 'tag9' ])
      self.assertEqual(vt.listTags("t",["tag1"]),['tag2', 'tag3'])
      self.assertEqual(vt.listTags("t",["tag6"]),[])
      self.assertEqual(vt.listTags("t",["tag7"]),['tag10', 'tag11', 'tag12', 'tag13', 'tag8', 'tag9'])
      self.assertEqual(vt.listTags("x",["tag7"]),[])
      self.assertEqual(vt.listTags("TaG1",["tag7"]),['tag10', 'tag11', 'tag12', 'tag13'])
      self.assertEqual(vt.listTagsAnywhere("ag",["tag1"]),['tag2', 'tag3'])
if __name__ == '__main__':
  # normally you would run as part of a test runner but if you just want to exercise the test in this file
  unittest.main()