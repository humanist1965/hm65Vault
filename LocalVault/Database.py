import sqlite3 as lite
import sys
import os
import pdb

class Database():

    def __init__(self,dbName="hm65VaultTest.db"):
        self.DATABASE_PATH = None # getDatabasePath will set this
        self.DATABASE_NAME = dbName

    def doDBConnect(self, dbConn=None):
        if dbConn == None:
            con = lite.connect(self.getDatabasePath())
        else:
            con = dbConn
        return con

    def getDatabasePath(self):
        if self.DATABASE_PATH is None:
            dbName = self.DATABASE_NAME
            # database will be stored under hm65Vault directory
            path = os.getcwd()
            pos = path.find("hm65Vault")
            pos += len("hm65Vault")
            path = path[0:pos]
            self.DATABASE_PATH = path+"/"+dbName
        return self.DATABASE_PATH


    def createDatabase(self):
        # See if the database already exists
        if not(os.path.exists(self.getDatabasePath())):

            con = self.doDBConnect()
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS KeyValue")   
                cur.execute("CREATE TABLE IF NOT EXISTS KeyValue(Key TEXT PRIMARY KEY DESC, Value TEXT)")

    def deleteDatabase(self):
        # See if the database already exists
        if os.path.exists(self.getDatabasePath()):
            os.remove(self.getDatabasePath())

    def databaseExists(self):
        return os.path.exists(self.getDatabasePath())

    def get(self, key, dbConn = None):
        con = self.doDBConnect(dbConn)
        with con:    
            cur = con.cursor()    
            cur.execute("SELECT * FROM KeyValue where Key=?", (key,)) # the comma next to key is needed!
            row = cur.fetchone()
            if row is None:
                return None
            else:
                return (key, row[1])


    def set(self, keyOrDict, value=None , dbConn=None):
        """
        Set the key to have value in the database

        ARGS:

        key     - Key to set. Key(s) are unique in the database. If key already exists then existing value will be updated
        value   - Value to set key to
        """
        if isinstance(keyOrDict ,dict):
            self._setFromDict(keyOrDict, dbConn)
            return
        else:
            key = keyOrDict

        con = self.doDBConnect(dbConn)
        if not(self.get(key,dbConn) is None):
            with con:
                cur = con.cursor()    
                cur.execute("UPDATE KeyValue SET Value=? WHERE Key=?", (value, key))        
                con.commit()
        else:
            with con:
                cur = con.cursor()    
                cur.execute("INSERT INTO KeyValue VALUES (?, ?)", (key, value))        
                con.commit()

    def _setFromDict(self, dict, dbConn=None):
        for (key,value) in dict.items():
            self.set(key,value,dbConn)

    def list(self, keyPat, dbConn=None):
        """
        finds all the keys that match keyPat.
        if keyPat does not contain any wildcard % chars then we will place one at end
        """

        # if there is no % in keypat then add one to the end
        # NOTE: If you want to find a specific item then use get()
        keyPat = keyPat if keyPat.find("%") != -1 else keyPat + "%"

        con = self.doDBConnect(dbConn)
        with con:    
            cur = con.cursor()    
            cur.execute("SELECT * FROM KeyValue where Key LIKE ?", (keyPat,)) # the comma next to key is needed!
            rows = cur.fetchall()
            return rows

    def getResultSet(self, keyPat, dbConn=None):
        """
        Calls list() and then converts the results into a result set.

        """
        return False

def main():
    db = Database()
    db.deleteDatabase()
    db.createDatabase()
    db.set("mk1", "val1")
    #db.set("mk2", "val2")
    #db.set("mk3", "val3")
    db.set("mk1", "val1b")

if __name__ == '__main__':
    main()