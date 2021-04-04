import csv

with open('peopleInformationCSV.csv','r') as file:
    # making the dictionary
    thereader = csv.DictReader(file)
    DictionaryInfo = []
    for line in thereader:
        DictionaryInfo.append(line)

with open('peopleInformationCSV.csv', 'r') as file:
    #making the list
    reader = csv.reader(file)
    ListInfo = list(reader)
    ListInfo.pop(0)


# printing the lists
print('Printing Both Lists:')
print(DictionaryInfo)
print(ListInfo)

# get the first element of the list, print name and age
print('Get the first element of the list, print name and age:')
print('List: ' + ListInfo[0][0] + ', ' + ListInfo[0][1] + ' years old.')  # first item in the list is the heather
fistDictItem = next(iter(DictionaryInfo))
print('Dictionary: ' + fistDictItem['name'] + ', ' + fistDictItem['age'] + ' years old.')

# people in a range of age
# input age
print('Sorting people in a range of age')
minimumAge = int(input('Minimum age: '))
maximumAge = int(input('Maximum age: '))

# list sorting age
listByAge = []
for lineIndex in range(0,len(ListInfo)-1):  # ask anderson about this line of code!!!!!!
    lineage = int(ListInfo[lineIndex][1])
    if minimumAge <= lineage <= maximumAge:
        listByAge.append(ListInfo[lineIndex])
print(listByAge)

# dictionary sorting age
dictByAge = []
for lineIndex in range(0,len(DictionaryInfo)):  # why does this one doesn't need the -1?????
    lineage = int(DictionaryInfo[lineIndex]['age'])
    if minimumAge <= lineage <= maximumAge:
        dictByAge.append(DictionaryInfo[lineIndex])
print(dictByAge)
