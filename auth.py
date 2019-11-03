# init cursor and stuff
auth = False
invalidUID = True
invalidPW = True
counter = 0
while (auth):
    while (invalidUID):
        # ask UID
        time.sleep(1000)
        userID = result.text
        if (len(userID) > 0):
            invalidUID = False
    while (invalidPW):
        # ask password
        time.sleep(4000)
        password = result.text
        if (len(password) > 0):
            invalidPW = False
    cursor.execute("SELECT * from users WHERE UserID=" + str(userID) + 'and Password= \'' + str(password) + '\'')
    if (val is not None):
        auth = False
    counter += 1
    if (counter > 5):
        break  