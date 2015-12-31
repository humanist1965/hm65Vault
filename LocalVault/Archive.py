import LocalVault.Database as data
import hashlib
import json
import pdb

class Archive():
	'''
	To synchronise across machines we use a persistent file system archive.
	In live environment the plan is to use GoogleDrive but we will also support a local file system
	implementation for test purposes.
	'''

	def __init__(self, vault):
		self.VAULT = vault

	def update(itemKey):
		'''
		Add new/updated item to the archive
		'''
		pass

	def receive():
		'''
		Look for new items in the archive and if found bring them into the local vault
		'''
		pass

	def repackArchive():
		'''
		rebuild the archive from the local vault.
		'''
		pass