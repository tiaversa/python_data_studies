import csv
from tkinter import *

# global Variables
global customersInfo
global mainFrame

# functions
def createFile():
    # creating a new file
    with open('testcsvfile.csv', 'w', newline='') as f:
        # f is the name I gave to the file, it can be anything
        fieldnames = ['name', 'address', 'email', 'birthday']
        # creating a writer object
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        # writing the heather
        thewriter.writeheader()
        thewriter.writerow({'name': 'Mona Lisa', 'address': 'Street 1', 'email': 'abc1@abc.com', 'birthday': '30.04.1996'})
        # when you use a dictionary there it doesn't matter the order.
        thewriter.writerow({'name': 'Tim', 'address': 'Street 2', 'email': 'abc2@abc.com', 'birthday': '05.10.1998'})
        thewriter.writerow({'name': 'Nando', 'address': 'Street 3', 'email': 'abc3@abc.com', 'birthday': '10.04.2006'})
        thewriter.writerow({'name': 'Lara Perez', 'address': 'Street 4', 'email': 'abc4@abc.com', 'birthday': '03.06.1983'})
        thewriter.writerow({'name': 'Pete', 'address': 'Street 5', 'email': 'abc5@abc.com', 'birthday': '20.07.1964'})
        # thewriter.writerow({'name': , 'address': , 'email': , 'birthday': })
    # close this creating the file area


def addBirthNumber():
    # adding the birth munber part for comparason
    for i in range(len(customersInfo)):
        birth = customersInfo[i]['birthday']
        day, month, year = birth.split('.')
        birth = year + month + day
        customersInfo[i]['birthNumber'] = [int(birth)]


def readFile():
    global customersInfo
    # reading the file
    with open('testcsvfile.csv', 'r') as file:
        thereader = csv.DictReader(file)
        # using the dictionary to read
        # creating the list
        customersInfo = []
        for line in thereader:
            # adding each line as a element in a list
            customersInfo.append(line)
        addBirthNumber()


# inicializing the functions
createFile()
readFile()
# creating the gui
root = Tk()
root.title('Customers Information')
# adding the main Frame
mainFrame = LabelFrame(root, width=400, height=400, padx=10, pady=10)
mainFrame.grid(row=1, column=0, columnspan=3)
mainFrame.grid_propagate(False)
# To keep the original size


def remakeMainFrame():
    # erasing frame and make new one
    global mainFrame
    mainFrame.destroy()
    # adding the main Frame
    mainFrame = LabelFrame(root, width=400, height=400, padx=10, pady=10)
    mainFrame.grid(row=1, column=0, columnspan=3)
    mainFrame.pack_propagate(False)
    mainFrame.grid_propagate(False)



def newCustomer():
    # new customer function
    remakeMainFrame()
    titlelabel = Label(mainFrame, text='Adding a new Customer\n')
    titlelabel.grid(row=0, column=0, columnspan=2)
    nameLabel = Label(mainFrame, text='Name: ', width=15)
    nameLabel.grid(row=1, column=0)
    nameEntry = Entry(mainFrame, width=40, borderwidth=5)
    nameEntry.grid(row=1, column=1)
    addressLabel = Label(mainFrame, text='Address: ', width=15)
    addressLabel.grid(row=2, column=0)
    addressEntry = Entry(mainFrame, width=40, borderwidth=5)
    addressEntry.grid(row=2, column=1)
    emailLabel = Label(mainFrame, text='Email: ', width=15)
    emailLabel.grid(row=3, column=0)
    emailEntry = Entry(mainFrame, width=40, borderwidth=5)
    emailEntry.grid(row=3, column=1)
    birthdayLabel = Label(mainFrame, text='Birthday: ', width=15)
    birthdayLabel.grid(row=4, column=0)
    birthdayEntry = Entry(mainFrame, width=40, borderwidth=5)
    birthdayEntry.insert(0,'01.01.2021')
    birthdayEntry.grid(row=4, column=1)
    submitButton = Button(mainFrame, text='Submit New Customer', command=lambda: saveCustomer(nameEntry.get(), addressEntry.get(), emailEntry.get(), birthdayEntry.get()))
    submitButton.grid(row=5, column=1)


def saveCustomer(name, address, email, birthday):
    # making sure the name always begins with caps
    nameList = name.split(' ')
    for i in range(len(nameList)):
        n = list(nameList[i])
        n[0] = n[0].upper()
        nameList[i] = ''.join(n)
    name = ' '.join(nameList)
    # adding to the file
    with open('testcsvfile.csv', 'a', newline='') as f:
        fieldnames = ['name', 'address', 'email', 'birthday']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writerow({'name': name, 'address': address, 'email': email, 'birthday': birthday})
    remakeMainFrame()
    confirmLabel = Label(mainFrame,text='Customer '+name+' information added to the System.')
    confirmLabel.pack()
    readFile()


def presentLabelsInFrame ():
    # passing throught the information and adding as labels
    rowCount = 0
    for line in customersInfo:
        columnCount = 0
        for key, value in line.items():
            if key != 'birthNumber':
                Label(mainFrame, text=value).grid(row=rowCount, column=columnCount)
            columnCount += 1
        rowCount += 1
    mainFrame.pack_propagate(False)



def sortBirthday():
    # sorting the list by date of birth
    remakeMainFrame()
    readFile()
    global customersInfo
    # sorting by the birthnumber
    customersInfo = sorted(customersInfo, key=lambda customer: customer['birthNumber'])
    # present labels
    presentLabelsInFrame()


def sortName():
    # sort by the name
    remakeMainFrame()
    readFile()
    global customersInfo
    # sorting by name
    customersInfo = sorted(customersInfo, key=lambda customer: customer['name'])
    presentLabelsInFrame()


# adding a button to the frame
newCustomerButton = Button(root, text='Add New Customer', command=newCustomer)
sortBirthdayButton = Button(root, text='Sort By Age', command=sortBirthday)
sortNameButton = Button(root, text='Sort By Name', command=sortName)

# Organizing the root
newCustomerButton.grid(row=0, column=0)
sortBirthdayButton.grid(row=0, column=1)
sortNameButton.grid(row=0, column=2)


presentLabelsInFrame()
root.mainloop()
