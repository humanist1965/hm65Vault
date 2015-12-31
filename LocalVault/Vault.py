import LocalVault.Database as data
import hashlib
import json
import re
import pdb

class hm65Vault():

	def __init__(self,dbName="hm65VaultTest.db"):
		self.DATABASE_NAME = dbName

	def addItem(self, vaultItem):
		"""
		Add vaultItem to the database. Either as a new item or an update
		"""
		db = self.getDB()
		key = self._getItemKey(vaultItem)
		self._addNewTags(key, vaultItem)
		db_key = "item/" + key
		itemObj = {}
		itemObj['url'] = vaultItem['url']
		itemObj['title'] = vaultItem['title']
		itemObj['notes'] = vaultItem['notes']
		itemObj['to_read'] = vaultItem['to_read']
		itemObj['tags'] = vaultItem['tags']
		db.set(db_key, self._serialiseObj(itemObj))
		return key

	def _getTagList(self, tagListStr):
		l = tagListStr.split()
		resSet = set(l)
		return resSet

	def _addNewTags(self, itemKey, vaultItem):
		self._removeExistingTags(itemKey)
		tagsList = self._getTagList(vaultItem['tags'])
		for tag in tagsList:
			self._addTag(itemKey, tag)
		self._addTagRelationships(tagsList)

	def _addTagRelationships(self, tagsList):
		db = self.getDB()
		tagsStr = self._serialiseObj(list(tagsList))
		for it1 in tagsList:
			dbkey1 = "tagRel/" + it1 
			keyPair = db.get(dbkey1)
			if keyPair is None:
				db.set(dbkey1, tagsStr)
			else:
				# If a tagRel exists already then update it
				tagsList2 = set(tagsList)
				oldRelList = self._deserialiseObj(keyPair[1])
				tagsList2.update(oldRelList)
				tagsStr2 = self._serialiseObj(list(tagsList2))
				db.set(dbkey1, tagsStr2)

	def _removeExistingTags(self, itemKey):
		oldItem = self.getItem(itemKey)
		if not(oldItem is None):
			db = self.getDB()
			tagsList = self._getTagList(oldItem['tags'])
			for tag in tagsList:
				dbkey1 = "tags/"+tag+"/"+itemKey
				dbkey2 = "tagInfo/"+tag+"/count"
				db.rm(dbkey1)
				count = int(db.get(dbkey2)[1])
				count -= 1
				db.set(dbkey2, count)

	def _addTag(self, itemKey, tag):
		db = self.getDB()
		dbkey1 = "tags/"+tag+"/"+itemKey
		dbkey2 = "tagInfo/"+tag+"/count"
		keyPair = db.get(dbkey2)
		if not(keyPair is None):
			count = int(keyPair[1])
			count += 1
		else:
			count = 1
		db.set(dbkey2, count)
		db.set(dbkey1,1)


	def getItem(self, key):
		"""
		get vaultItem from the database.
		"""
		db = self.getDB()
		db_key = "item/" + key
		keyPair = db.get(db_key)
		if not(keyPair is None):
			objStr = keyPair[1]
			return self._deserialiseObj(objStr)
		else:
			return None


	def _getItemKey(self, vaultItem):
		urlToHash = bytes(vaultItem['url'],'utf-8')
		hash_object = hashlib.sha256(urlToHash)
		hex_dig = hash_object.hexdigest()
		return hex_dig

	def _serialiseObj(self, obj):
		return json.dumps(obj)

	def _deserialiseObj(self, objStr):
		return json.loads(objStr)


	def tagCount(self, tagStr):
		db = self.getDB()
		dbkey = "tagInfo/"+tagStr+"/count"
		keyPair = db.get(dbkey)
		if keyPair is None:
			return 0
		else:
			return keyPair[1]

	def listItems(self, matchingTagList):
		resDict = {}
		completeMatches = {}
		db = self.getDB()
		tagsList = self._getTagList(matchingTagList)
		numTags = len(tagsList)
		for tag in tagsList:
			dbkey1 = "tags/"+tag+"/"
			rows = db.list(dbkey1)
			self._addToMatchResults(dbkey1, resDict, rows)
		for (key,value) in resDict.items():
			if value == numTags:
				# Only add keys that match all tags
				completeMatches[key] = 1
		return completeMatches

	def _addToMatchResults(self, prefixStr, resDict, rows):
		for row in rows:
			key = row[0]
			itemKey = key[len(prefixStr):]
			cc = resDict.get(itemKey, 0)
			cc += 1
			resDict[itemKey] = cc


	def listTagsAnywhere(self, tagPattern, context=None):
		tagPattern = r"[^\b]"+tagPattern
		return self.listTags(tagPattern, context)

	def listTags(self, tagPattern, context=None):
		'''
		Find tags that match the tagPattern.
		context is the scope to search for tags in and is a dictionary of item keys
		'''
		tagsStr = self._buildSearchString(context)
		matchList = self._matchTags(tagPattern)
		tidyList = []
		for it in matchList:
			it = it.strip()
			tidyList.append(it)
		return tidyList
		

	def _buildSearchString(self, context):
		'''
		context is list of other tags
		'''
		resSet = self._getTagsInContext(context)
		resList = list(resSet)
		resList = sorted(resList)
		resStr = ""
		for it in resList:
			# Not efficient but will do for now
			resStr += it + " "
		self.TAGS_SEARCH_STR = resStr
		return resStr

	def _getTagsInContext(self, context):
		resSet = set()
		if context is None:
			db = self.getDB()
			dbkey1 = "tagInfo/"
			results = db.list(dbkey1)
			for (key, _) in results:
				tagName = key[len(dbkey1):]
				tagName = tagName[:tagName.find('/')]
				resSet.add(tagName)
		else:
			db = self.getDB()
			resDict = {}
			for tag in context:
				dbkey1 = "tagRel/" + tag 
				results = db.list(dbkey1)
				for (key, val) in results:
					relTags = self._deserialiseObj(val)
					for tagName in relTags:
						if tagName==tag:
							continue
						count = resDict.get(tagName,0)
						count += 1
						resDict[tagName] = count
			contextCount = len(context)
			# Results are the ones that matched all context items
			for (key,val) in resDict.items():
				if val == contextCount:
					resSet.add(key)

		return resSet

	def _matchTags(self, tagPattern):
		# search self.TAGS_SEARCH_STR for tags matching tagPattern
		tagToSearch = r"\b" + tagPattern + "[^ ]*[ ]"
		res = re.findall(tagToSearch, self.TAGS_SEARCH_STR, re.IGNORECASE)
		return res
		
		
	def getDB(self):
		db = data.Database(self.DATABASE_NAME)
		db.createDatabase()
		return db
