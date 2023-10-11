import datajoint as dj
import pymysql
from ssl import SSLError


# shared connection values between 2 tests
mysql_host = "db"
mysql_user = "root"
mysql_password = "simple"
print("----------Shared Connection Values----------")
print(f"Host: {mysql_host}")
print(f"User: {mysql_user}")
print(f"Password: {mysql_password}\n")

###############################################################################################
###################            pymysql connection to MYSQL DB               ###################
###############################################################################################
print("----------Entering pymysql connection test----------")
connection = pymysql.connect(user=mysql_user,password=mysql_password,host=mysql_host,port=3306)
cursor = connection.cursor()
cursor.execute('SELECT user, host, ssl_type, ssl_cipher, account_locked FROM mysql.user;')
users = cursor.fetchall()
for user in users:
    print(user)
connection.close()
print("----------Exiting pymysql connection test----------\n")

###############################################################################################
##################            datajoint connection to MYSQL DB               ##################
###############################################################################################
print("----------Entering datajoint connection test----------")

try:
    dj.config["database.host"] = mysql_host
    dj.config["database.user"] = mysql_user
    dj.config["database.password"] = mysql_password

    dj.config.save_global()
    schema = dj.schema('tutorial')

    @schema
    class Mouse(dj.Manual):
        definition = """
        # Experimental animals
        mouse_id             : int                          # Unique animal ID
        ---
        dob=null             : date                         # date of birth
        sex="unknown"        : enum('M','F','unknown')      # sex
        """

    data = [
      (1, '2016-11-19', 'M'),
      (2, '2016-11-20', 'unknown'),
      (5, '2016-12-25', 'F')
      ]

    Mouse.insert(data)
    print(Mouse())
    Mouse.delete()

except SSLError as err:
    print(err)
except pymysql.err.OperationalError as err:
    print(err)
finally:
    print("----------Exiting datajoint connection test----------\n\n")
