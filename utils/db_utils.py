__author__ = 'Rahul.R'
import MySQLdb
from MySQLdb.cursors import DictCursor
def connect_db():
    """
    Connects to the
    :return:
    """
    db = MySQLdb.connect(host="127.0.0.1", user="singlebox",
                              passwd="global!23", db="test",
                              cursorclass=MySQLdb.cursors.DictCursor)
    return db