__author__ = 'Rahul.R'
def connect_db(self):
    """
    :return:
    """
    self.db = MySQLdb.connect(host="127.0.0.1", user="singlebox",
                              passwd="global!23", db="test",
                              cursorclass=MySQLdb.cursors.DictCursor)
    return self.db