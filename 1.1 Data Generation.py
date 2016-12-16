# 1.1 Data Generation

# Import List
import string
import os
import time
import math
from random import randint
import random

# Function List

# Creating the input folder at the specified path
def create_input_folder(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        return folderName
    else:
        #File is already existing. Concatenation with a timestamp to be certain of its unicity
        os.makedirs(folderName + str(time.time()))
        return folderName + str(time.time())

# Creating a folder with a specific name below the input folder    
def create_subfolder(folderName):
    os.makedirs(folderName)
    return folderName

# Generate a random string in a various size
def generate_string():
    stringSize = randint(1,10000)
    return ''.join(random.choice('0123456789ABCDEF') for x in range(stringSize))
    
# Create file 
def create_file(index, blockSize, maxSize, folderName):

    # 1. Creating new empty file at the specified path
    folderName = folderName + "\\" + "file" + str(index + 1) # index + 1 to start the file indexation at 1
    fileSize = 0

    
    f = open(folderName,"w")
    # We are going to generate random strings with various size and test if it's close to the size limit
    # When the size limit is overtaked, exiting the loop
    while fileSize < blockSize:
        # Generate random alphanumeric string with a various sizeù
        randomString = generate_string()
        f.write(randomString)
        f.write("\n") # Writing a new line
        # Increment file size
        fileSize = os.stat(folderName).st_size

    f.close() # Close the file


# Manage each file to create
def manage_subfile(blockSize, maxSize, subfolderName,key):
    # 1. Define the number of file
    # Ceil to get the exact number of files in integer format
    fileToCreateCount = math.ceil(maxSize / blockSize)

    # Test if this is an exact divisor
    if maxSize % blockSize == 0:
        exactDivisorFlag = 1
    else:
        exactDivisorFlag = 0

    print("Preparing to create " + str(fileToCreateCount) + " files in the folder " + str(key) + " with a blocksize of " + str(blockSize))
    for i in range(0,fileToCreateCount):
        # if it's the last file to create and the divisor is not exact we have to change the file creation
        if exactDivisorFlag == 0 and i == (fileToCreateCount - 1):
            # How to modiify the size ?
            lastFileSize = maxSize % blockSize
            create_file(i, lastFileSize, maxSize, subfolderName)
        else:
            create_file(i, blockSize, maxSize, subfolderName)

# Get size of a folder given a input path      
def get_folder_size(subFolderName):
    folderSize = 0
    for (path, dirs, files) in os.walk(subFolderName):
      # Get the index of the last file for later
      for file in files:
        filename = os.path.join(path, file)
        folderSize += os.path.getsize(filename)
    return folderSize


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
    
# NB : fileSize is in KiloBytes
def generate_dataset(inputFolder, fileSize, fileSpecification):
    #print(inputFolder)
    #print(fileSize)
    #print(fileSpecification)

    nameSizeArray = {}

    # File size is in KB
    fileSize = float(fileSize) * 1000

    # 1. Manage third argument to create a dictionnary with (Name|Size)
    nameLocationSizeList = fileSpecification.split(',')

    # 2. Check if the number of item is even
    itemCnt = len(nameLocationSizeList)

    if itemCnt % 2 != 0:
        # Should be equal to 0. If it's not don't take the last element
        nameLocationSizeList = nameLocationSizeList[:-1]
        #print(nameLocationSizeList)
    
    # 3. Construction of the array Name|Size
    for i in range(0,itemCnt,2):
        nameSizeArray[nameLocationSizeList[i]] = nameLocationSizeList[i+1]

    # 4. Creation of the input folder
    inputFolder = create_input_folder(inputFolder)

    # 5. Creation of the subfolder with the name
    for key, value in nameSizeArray.items():
        subfolderName = create_subfolder(inputFolder + "\\" + key)
        # 6. Manage (create name, files etc..) for each element of the dictionnary
        # * 1 000 000 because size is in megabytes
        manage_subfile(fileSize, float(value) * 1000000, subfolderName, key)

    # 6. We need to print a conclusion to check easily the result of the program
    printResult(inputFolder)
 



# Main programm
generate_dataset("C:\\Users\\lucien\\AppData\\Local\\Programs\\Python\\Python35-32\\Sentiance\\test1","11000","locations,64,sensors,138,devices,24")

#printResult("C:\\Users\\lucien\\AppData\\Local\\Programs\\Python\\Python35-32\\Sentiance\\test1")
