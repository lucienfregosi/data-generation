# 1.3 Data Backup

# Import List
import os
from shutil import copyfile
import sys

# Function List
def backup_dataset(folderToBackup, backupFolderPath):
    
    # Test if the folder to backup exists
    if not os.path.exists(folderToBackup):
        print("folder does not exist. Execute previously 1.1 Data Generation.py")
        sys.exit()

    # Create the input folder in backup
    if os.path.exists(backupFolderPath):
        print("Backup Folder does exist")
        sys.exit()
    else:
        os.makedirs(backupFolderPath)
    



    # The folder exists. We are gonna loop in the folder to copy the files
    for (path, dirs, files) in os.walk(folderToBackup):
      # Loop on the different folder name
      for dir in dirs:
        subFolderToBackup = folderToBackup + "\\" + dir
        subFolderBackup = backupFolderPath + "\\" + dir
        # Create the subfolder to backup
        os.makedirs(subFolderBackup)
            
        # Loop on the different file in the folder
        for (path, dirs, files) in os.walk(subFolderToBackup):
          for file in files:
              # Build Path
              subFilePath   = subFolderToBackup + "\\" + file
              subFileBackup = subFolderBackup + "\\" + file
              copyfile(subFilePath,subFileBackup)

        print("Successfull backup at path:" + backupFolderPath)
              
              


# Main programm
backup_dataset("C:\\Users\\lucien\\AppData\\Local\\Programs\\Python\\Python35-32\\Sentiance\\test1","C:\\Users\\lucien\\AppData\\Local\\Programs\\Python\\Python35-32\\backup\\testBackup")
