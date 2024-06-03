#!/usr/bin/python3
"""Testing file
"""
import hashlib
import MySQLdb
import sys

if __name__ == "__main__":
    """ Access to database and get password TODO
    """
    user_email = "b@b.com"
    clear_pwd = "pwdB"
    hidden_pwd = hashlib.md5(clear_pwd.encode()).hexdigest()
    
    conn = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1], passwd=sys.argv[2], db=sys.argv[3], charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE email = '{}' LIMIT 1".format(user_email))
    query_rows = cur.fetchall()
    for row in query_rows:
        if hidden_pwd.lower() == row[0].lower():
            print("OK")
    cur.close()
    conn.close()
    print("done")
    # ./my_test.py hbnb_dev hbnb_dev_pwd hbnb_dev_db
