# 1.2 Data Update

# Import List
import string
import os
import time
import math
import sys
from random import randint
import random

# Function List

# Show at the end of the program these files newly created with their size to check
def printResult(inputFolder):
    # 2 results to show.
    # One overall with the three folder name and the global size of each of us
    # A second detailled with the file detail and the size of each size
    resultOverall = {}
    resultDetail = {}

    resultOverall[inputFolder] = {}
    resultDetail[inputFolder] = {}

    # Loop in the input folder
    for (path, dirs, files) in os.walk(inputFolder):
        # Loop in each directory
        for dir in dirs:
            resultDetail[inputFolder][dir] = {}
            resultOverall[inputFolder][dir] = {}

            # Build the subfolder path
            subFolderPath = inputFolder + "\\" + dir
            # Manage the folder size for the overall result
            resultOverall[inputFolder][dir] = str(round(get_folder_size(subFolderPath) / 1000000,2)) + "Mb"

            
            # Loop on each files
            for (path, dirs, files) in os.walk(subFolderPath):
                for file in files:
                    filePath = subFolderPath + "\\" + file
                    resultDetail[inputFolder][dir][file] = {}
                    resultDetail[inputFolder][dir][file] = str(round(os.path.getsize(filePath) / 1000000,2)) + "Mb"
    

    print("Overall Result")
    print(resultOverall)
    print("\n")
    print("Result Result")
    print(resultDetail)

# Get size of a folder given a input path  
def get_folder_size(subFolderName):
    folderSize = 0
    for (path, dirs, files) in os.walk(subFolderName):
      # Get the index of the last file for later
      for file in files:
        filename = os.path.join(path, file)
        folderSize += os.path.getsize(filename)
    return folderSize

# Generate a random string in a various size
def generate_string():
    stringSize = randint(1,30)
    return ''.join(random.choice('0123456789ABCDEF') for x in range(stringSize))

# Function to manage the last file of a folder to update
# Case 1 : when the initial file size + the size to add is lower than a block size
def fill_last_file_uncompleted(lastFilePath, sizeToAdd):
    # Keep the initale size
    initialFileSize = os.stat(lastFilePath).st_size
    fileSize = initialFileSize
    
    f = open(lastFilePath,"w")
    while fileSize < initialFileSize + sizeToAdd :
        # Generate random alphanumeric string with a various size
        randomString = generate_string()
        f.write(randomString)
        f.write("\n")
        # Redfine file size
        fileSize = os.stat(lastFilePath).st_size
    f.close()

# Case 2 : when the initial file size + the size to add is greater than a block size
#          Populating the last file from its initial size from the file block size
def fill_last_file(lastFilePath, blockSize):
    # Should be not null
    print("Filling the last file with path:" + str(lastFilePath))
    fileSize = os.stat(lastFilePath).st_size
    f = open(lastFilePath,"w")
    while fileSize < blockSize:
        # Generate random alphanumeric string with a various sizeù
        randomString = generate_string()
        f.write(randomString)
        f.write("\n")
        # Increment file size
        fileSize = os.stat(lastFilePath).st_size
    f.close()

# Create a new file
def create_file(index, blockSize, folderName):

    # 1. Creating new empty file
    folderName = folderName + "\\" + "file" + str(index)
    fileSize = 0
    f = open(folderName,"w")

    # We are going to generate random strings with various size and test if it's close to the size limit
    while fileSize < blockSize:
        # Generate random alphanumeric string with a various sizeù
        randomString = generate_string()
        f.write(randomString)
        f.write("\n")
        # Increment file size
        fileSize = os.stat(folderName).st_size
    f.close()


def manage_file_creation(sizeToAdd, blockSize, startIndex, subFolderPath):
    # 1. Define the number of file
    # Ceil to get the exact number of files in integer format
    fileToCreateCount = math.ceil(sizeToAdd / blockSize)

    # Test if this is an exact divisor
    if sizeToAdd % blockSize == 0:
        exactDivisorFlag = 1
    else:
        exactDivisorFlag = 0

    #print(startIndex)

    for i in range(startIndex, fileToCreateCount + startIndex):
        # if it's the last file to create and the divisor is not exact we have to change the file creation
        if exactDivisorFlag == 0 and i == (fileToCreateCount - 1 + startIndex):
            #print("last one:" + str(i))
            lastFileSize = sizeToAdd % blockSize
            create_file(i, lastFileSize,subFolderPath)
        else:
            create_file(i, blockSize, subFolderPath)
    

def manage_subfolder(sizeToAdd, subFolderPath):
    if not os.path.exists(subFolderPath):
        print("Error folder path does not exist")
        sys.exit()

    # 1. Get the current size of the folder
    folderInitialSize = 0
    for (path, dirs, files) in os.walk(subFolderPath):
      # Get the index of the last file for later
      lastIndex = len(files)
      for file in files:
        filename = os.path.join(path, file)
        folderInitialSize += os.path.getsize(filename)
        
    # 2. Get the block size (from the size of the first file)
    firstFilePath = subFolderPath + "\\file1"
    if not os.path.exists(firstFilePath):
        print("Error : No file in the folder")
        sys.exit()
        
    blockSize = os.path.getsize(firstFilePath)

    # 3. Complete the last file
    lastFilePath = subFolderPath + "\\file" + str(lastIndex)
    lastFileSize = os.path.getsize(lastFilePath)

    #print(lastFileSize)
    #print(blockSize)
    #print(sizeToAdd)

    # 4. Test if we will juste complete the last file or add some others files
    if blockSize - lastFileSize >= sizeToAdd:
        #print("only the last file has to be completed")
        # In that case we have to add data in only one file
        fill_last_file_uncompleted(lastFilePath, sizeToAdd)
    else:
        #print("more than one file has to be added")
        fill_last_file(lastFilePath, blockSize)
        # 5. We have to create the others files, as the same way than 1.1 Data Creation
        # Define the new size to add (without the data to complet the previous file
        sizeToAdd = sizeToAdd - blockSize + lastFileSize
        # The behaviour of this funciton is very similar to the 1.1 data creation. 
        manage_file_creation(sizeToAdd, blockSize,lastIndex +1, subFolderPath)

def update_dataset(folderToUpdate, fileSpecification):
    
    # 1. Check if the foldera already exists
    if not os.path.exists(folderToUpdate):
        print("folder does not exist. Execute previously 1.1 Data Generation.py")
        sys.exit()

    # Ditcionnary int the following format (name:size)
    nameSizeArray = {}
    
    # 2. Manage third argument to create a dictionnary with (Name|Size)
    nameLocationSizeList = fileSpecification.split(',')
    
    # 3. Check if the number of item is even
    itemCnt = len(nameLocationSizeList)

    if itemCnt % 2 != 0:
        # Should be equal to 0. If it's not don't take the last element
        nameLocationSizeList = nameLocationSizeList[:-1]
        #print(nameLocationSizeList)

    # 3. Construction of the array Name|Size
    for i in range(0,itemCnt,2):
        nameSizeArray[nameLocationSizeList[i]] = nameLocationSizeList[i+1]

    # 4. For each subfolder, adding new files
    for key, value in nameSizeArray.items():
        # Define the file folder for each of us
        subfolderName = folderToUpdate + "\\" + key
        # 6. Manage (add files etc) for each element of the dictionnary
        # * 1 000 000 because size is in megabytes
        #print("Going to manage :" + key)
        manage_subfolder(float(value) * 1000000, subfolderName)

    # 5. Print result to validate script
    printResult(folderToUpdate)




# Main programm
update_dataset("C:\\Users\\lucien\\AppData\\Local\\Programs\\Python\\Python35-32\\Sentiance\\test1","locations,12,sensors,23,devices,10")
#printResult("C:\\Users\\lucien\\AppData\\Local\\Programs\\Python\\Python35-32\\Sentiance\\test1")
