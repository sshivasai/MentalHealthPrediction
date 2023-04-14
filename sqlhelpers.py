from app import makeconnection

class Table():
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args

        #if table does not already exist, create it.
        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(1000)," %column

            conn = makeconnection()
            cur = conn.cursor() #create the table
            print("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            conn.commit()
            cur.close()

    #get all the values from the table
    def getall(self):
        cur = makeconnection().cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    def getone(self, search, value):

        data = {}; cur = makeconnection().cursor()
        result = cur.execute("SELECT * FROM "+str(self.table)+ " WHERE "+ str(search)+ " = " + "'"+str(value)+ "'")
        data = cur.fetchone()
        cur.close(); return data

    #delete a value from the table based on column's data
    def deleteone(self, search, value):
        conn = makeconnection()
        cur =conn.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        conn.commit(); cur.close()

    #delete all values from the table.
    def deleteall(self):
        self.drop() #remove table and recreate
        self.__init__(self.table, *self.columnsList)

    #remove table from mssql
    def drop(self):
        conn = makeconnection()
        cur = conn.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        conn.commit()
        cur.close()

    #insert values into the table
    def insert(self, *args):
        #print("sdf")
        data = []
        for arg in args: #convert data into string mssql format
            data.append("'"+str(arg)+"'")

        data = ",".join(data)
        data = "(" + data +")"
        print(data)
        conn = makeconnection()
        table_name = self.table
        print(str(self.columns))
        cur = conn.cursor()
        cur.execute("INSERT INTO "+ table_name +str(self.columns)+" VALUES" + data)
        conn.commit()
        cur.close()

#execute mssql code from python
def sql_raw(execution):
    conn = makeconnection()
    cur = conn.cursor()
    
    cur.execute(execution)
    conn.commit()
    cur.close()

#check if table already exists
def isnewtable(tableName):

    cur = makeconnection().cursor()

    try: #attempt to get data from table
        result = cur.execute("SELECT * from %s" %tableName)
        cur.close()
    except:
        return True
    else:
        return False

#check if user already exists
def isnewuser(username,email = None):
    #access the users table and get all values from column "username"
    users = Table("users", "name", "email", "username", "password","age","gender")
    data = users.getall()
    usernames = [user.get('username') for user in data]
    if email:
        emails = [user.get('email') for user in data]
        return False if username in usernames or email in emails else True
    else:
        return False if username in usernames else True


def getdetails(username):
    
    conn = makeconnection()
    cur = conn.cursor()

    username = "'"+str(username)+"'"
    result = cur.execute("SELECT * FROM details where username = "+str(username)+" order by dateandtime desc" )
    data = cur.fetchall(); 
    cur.close()
    
    return data

def getprofile(username):
   
    conn = makeconnection()
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM users where username = '" +str(username)+"'" )
    data = cur.fetchone(); 
    
    cur.close()
    return data

def getage(username):
    conn = makeconnection()
    cur = conn.cursor()
    result = cur.execute("SELECT age FROM users where username = '" +str(username)+"'" )
    data = cur.fetchone(); 
    cur.close()
    return data

def getGender(username):
    conn = makeconnection()
    cur = conn.cursor()
    result = cur.execute("SELECT gender FROM users where username = '" +str(username)+"'" )
    data = cur.fetchone(); 
    cur.close()
    return data

def updatequery(username,column,value):
    conn = makeconnection()
    cur = conn.cursor()
    result = cur.execute("UPDATE users " +"SET " +str(column)+ " = " + "'"+str(value)+"' where username = '" +str(username)+ "'" )
    cur.commit()
    cur.close()
    
