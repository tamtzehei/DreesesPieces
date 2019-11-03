import pyodbc
import numpy as np
server = 'mocksqlserver.database.windows.net'
database = 'mockBanking'
username = 'azureuser'
password = 'Abc12345'
userID = 10000
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


def get_ints(text):
  for c in text:
      if (c != ' ' and c.isdigit() == False):
          text = text.replace(c, '')
  return [int(i) for i in text.split() if i.isdigit()] 

def deal_with_switch(command_type,command_string):
  list_boii = get_ints(command_string)
  if (command_type == "deposit"):
    #Add specified amount
    accountID = list_boii.pop(np.argmax(np.asarray(list_boii)))
    amount = list_boii.pop(0)
    cursor.execute("SELECT Balance FROM accounts where AccountNumber=" + str(userID))   
    val = np.asarray(cursor.fetchone())
    if (val is None):
      # output "invalid information"
      print("Invalid information")
    else:
      cursor.execute('INSERT INTO transactions (Receiving, Sending, Amount) VALUES (0,' + str(accountID) + ', ' + str(amount) + ')')
      cursor.execute('UPDATE accounts SET Balance = Balance + '+ str(amount) + ' WHERE AccountNumber = ' + str(accountID))
  elif (command_type =="withdraw"):
    accountID = list_boii.pop(np.argmax(np.asarray(list_boii)))
    amount = list_boii.pop(0)
    cursor.execute("SELECT Balance FROM accounts where AccountNumber=" + str(userID))   
    val = np.asarray(cursor.fetchone())
    if (val is None):
      # output "invalid information"
      print("Invalid information")
    elif (val[0] > amount):
      cursor.execute('INSERT INTO transactions (Receiving, Sending, Amount) VALUES (0,' + str(accountID) + ', ' + str(amount) + ')')
      cursor.execute('UPDATE accounts SET Balance = Balance + '+ str(amount) + ' WHERE AccountNumber = ' + str(accountID))
    else:
      # output "cannot withdraw more than you have"
      print("Cannot withdraw more than you have")
  elif (command_type=="transfer"):
    cursor.execute('SELECT AccountNumber FROM accounts where UserID = ' + str(userID))
    row = cursor.fetchone()
    amount = list_boii.pop(np.argmin(list_boii))
    transferTo = 0
    transferFrom = 0
    boole = True
    list = []
    while row:
      list.append(row[0])  
      row = cursor.fetchone()
    if (list_boii[0] in list):
      transferFrom = list_boii[0]
      transferTo = list_boii[1]

    elif (list_boii[1] in list):
      transferTo = list_boii[0]
      transferFrom = list_boii[1]
    else:
      #output "invalid information"
      print("Invalid information")
      boole = False

    if (boole):
      cursor.execute('SELECT Balance FROM accounts where AccountNumber=' + str(transferTo))
      val = np.asarray(cursor.fetchone())
      cursor.execute('SELECT Balance FROM accounts where AccountNumber=' + str(transferFrom))
      valTwo = np.asarray(cursor.fetchone())
      if (val is None):
        #output invalid information
        print("Invalid information")
      elif (valTwo[0] > amount):
        cursor.execute('INSERT INTO transactions (Receiving, Sending, Amount) VALUES (' + str(transferFrom) + ', ' + str(transferTo) + ', ' + str(amount) + ')')
        cursor.execute('UPDATE accounts SET Balance = Balance - ' + str(amount) + ' WHERE AccountNumber = ' + str(transferFrom))
        cursor.execute('UPDATE accounts SET Balance = Balance + ' + str(amount) + ' WHERE AccountNumber = ' + str(transferTo))
      else:
        #output not enough balance to transfer  
        print("Not enough balance to transfer")  
  elif (command_type =="balance"):
    # Query Deposit
    accountID = list_boii[0]
    cursor.execute('SELECT Balance from accounts where AccountNumber = ' + str(accountID))
    val = cursor.fetchone()
    # output val[0] as account balance.
    print(str(val[0]))
  cursor.commit()