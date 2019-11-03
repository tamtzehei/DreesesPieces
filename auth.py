# init cursor and stuff
auth = True
while (auth):
    # ask them for input and shit
    # userID = something
    # password = something
    cursor.execute("SELECT * from users WHERE UserID=" + str(userID) + 'and Password= \'' + str(password) + '\'')
    if (val is not None):
        auth = False

    

    