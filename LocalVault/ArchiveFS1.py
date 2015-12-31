import LocalVault.Vault as vault
import hashlib
import json
import pdb

class ArchiveFS1():
	'''
	Local FileSystem class
	'''

	def __init__(self, vault, rootDirName):

	def createRootDirectory(self):
		pass

	def removeAllfromRoot(self):
		pass

	def addTransaction(self, fileName, fileBody):
		pass

	def applyNewTransactions(self):
		'''
		Search the Archive looking for transactions after last one applied.
		If found then add to the vault.
		'''
		pass