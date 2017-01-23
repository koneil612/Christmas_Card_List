#import mysql.connector
import config, os


# ### This py page should only be my classes of card stuff - ie the entry and database things. NOTHING ELSE

class Entry:
    def __init__(self,id=0):
        if(not type(id)==int):
            id=int(id)
            query = "SELECT id,firstname, lastname, address, address2, city, state, zip FROM addresses where id=%d"%id
            result_set = Database.getResult(query,True)
            self.id=id
        if not result_set is None:
            self.firstname=result_set[1]
        return

    def save(self):
        if self.id>0:
            return self.update()
        else:
            return self.insert()

    def insert(self):
        query = ("insert into addresses (firstname, lastname, address, address2, city, state, zip) values (%s, %s, %s, %s, %s, %s, %s)"% Database.escape(self.firstname),Database.escape(self.lastname),Database.escape(self.address),Database.escape(self.address2),Database.escape(self.city),Database.escape(self.state),Database.escape(self.zip))
        self.id=Database.doQuery(query)
        return self.id

    def update(self):
        query = "update addresses set firstname='%s' lastname='%s'address='%s'address2='%s'city='%s'state='%s'zip='%s'where id=%d"%(Database.escape(self.firstname),self.id)
        return Database.doQuery(query)

    def delete(self):
        query = ("update addresses set deleted=1 where id=%d"%self.id)
        Database.doQuery(query)
        return True

    def __str__(self):
     return self.firstname

    @staticmethod
    def getObjects():
        query = "SELECT id FROM addresses where deleted=0"
        result_set = Database.getResult(query)
        entrys=[]
        for item in result_set:
            id = int(item[0])
            entrys.append(Entry(id))
        return entrys

class User(object):
    def __init__ (self, username):
        self.username = username
        self.password = password
        query = "SELECT username, password FROM \"user\" where username = '%s'" % username
        result_set = Database.getResult(query,True)

    def login(self,password):
        if result_list and len(result_list) > 0:
            user = result_list[0]
            if password == user.password:
                #successfully logged in
                session['username'] = user.username
        return loginsuccess

    def logout(self):
        del session['username']

class Database(object):
    @staticmethod
    def getConnection():
        if config.DBTYPE=="mysql":
            return mysql.connector.connect(user=config.DBUSER,password=config.DBPASS,host=config.DBHOST,database=config.DBNAME)
        if config.DBTYPE=="postgresql":
            return pg.db(host=config.DBHOST, user=config.DBUSER, passwd=config.DBPASS, dbname=config.DBNAME)

    @staticmethod
    def escape(value):
        return value.replace("'","''")

    @staticmethod
    def getResult(query, getOne = False):
        result_set=()
        conn = Database.getConnection()
        if config.DBTYPE=="mysql":
            cur = conn.cursor()
            cur.execute(query)
            if getOne:
                result_set = cur.fetchone()
            else:
                result_set = cur.fetchall()
            cur.close()
        if config.DBTYPE=="postgresql":
            result = conn.query(query)
            result_set = result.getresult()
            if getOne and result_set:
                result_set=result_set[0]
                conn.close()
        return result_set

    @staticmethod
    def doQuery(query):
        conn = Database.getConnection()
        if config.DBTYPE == "mysql":
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            lastID = cur.lastrowid
            cur.close()
        if config.DBTYPE == "postgresql":
            result = conn.query(query)
            lastID = result.getresult()[0][0]
            print "lastID=%d" %lastId
        conn.close()
        return lastID

if __name__ == '__main__':
    app.run(debug=True)
