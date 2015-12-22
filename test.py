import os
import sys

def getRootDir():
  cwd = os.getcwd()
  print(cwd)
  pos = cwd.find("hm65Vault")
  print(pos)
  pos += len("hm65Vault")
  cwd = cwd[0:pos]
  print(cwd)

getRootDir()
sys.exit(0)