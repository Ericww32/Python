######################################################################################
# Author: Eric Willoughby
# Date: 2024-10-26
# Filename: Flatten_Dir.py
# Description: The goal of this is to minimize the amount of sub-directories by moving 
#              all files forward to a top directory "flattening" the directory count to 1
#
# Install the following:
######################################################################################
#! /usr/bin/python3

import os, itertools, shutil

cwd = os.getcwd()
destPath = os.path.join(cwd, "flattened")

# Create the directory if it doesn't exist
if not os.path.exists(destPath):
    try:
        print("Destination path does not exist...")
        os.mkdir(destPath)
        print(f"Directory '{destPath}' created successfully.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{destPath}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Removes any directory it sees in the current working directory
def clean_up():
    # List of directories to keep
    skip_dirs = {'tmp', 'flattened'}
    i = 0

    for item in os.listdir(cwd):
        item_path = os.path.join(cwd, item)
        # Check if it is a directory and not in the list of directories to keep
        if os.path.isdir(item_path) and item not in skip_dirs:
            # Remove the directory
            shutil.rmtree(item_path)
            i += 1

    print(f"Removed {i} directories")

# Checks if a file exists in the specified directory.
#     Args:
#         filename: The name of the file.
#         dir_path: The path to the directory.
#     Returns:
#         True if the file exists in the directory, False otherwise.
def check_file_dup(destination, filename):
    file_path = os.path.join(destination, os.path.basename(filename))
    return os.path.exists(file_path)

# Walks through every directory and gathers a list of files
#     Args:
#         destination: the path that all the files will flow to.
def flat_dir(destination):
    all_files = []
    i = 1

    for root, dirs, files in itertools.islice(os.walk(cwd), 1, None):
        for filename in files:
            all_files.append(os.path.join(root, filename))
    for filename in all_files:
        try:
            if not filename == "Flatten_Dir.py" and not check_file_dup(destination, filename):
                shutil.move(filename, destination)
                i += 1
        except Exception as e:
            print(f"An error occurred: {e}")

    print(f"Moved {i} files to {destination}")

flat_dir(destPath)
clean_up()