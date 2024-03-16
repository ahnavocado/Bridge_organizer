import re
import shutil
import os
import sqlite3
import time
from sqlite3 import Error

sql_path = ''
# ex) /Users/abc/Library/Caches/Adobe/Bridge/Cache/v36/data/store
db_parent_path = ""
# ex)bridge:fs:file:///Users/abc/Desktop/230110
target_folder = ""
# ex) /Users/abc/Desktop/230110



def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def connection():
    try:
        con = sqlite3.connect(sql_path)
        return con
    except Error:
        print(Error)


def read_name_label(con) -> list:
    # read db file and append the tuple ( filename, label ) in db_info
    db_info = []
    cursor_db = con.cursor()
    cursor_db.execute(
        f'SELECT name,label FROM FileSystem_Nodes where label is not null and parentPath="{db_parent_path}"')
    raw_datas = (cursor_db.fetchall())
    for _ in raw_datas:
        db_info.append(_)
    print(db_info)
    return db_info
def read_rating(con)->list:
    # read db file and append the tuple ( filename, rating ) in db_info
    db_rating=[]
    cursor_db = con.cursor();
    cursor_db.execute(f'SELECT name, rating FROM FileSystem_Nodes where  rating is not null and not rating ="0" and parentPath="{db_parent_path}" ')
    rating_data = (cursor_db.fetchall())
    for _ in rating_data:
        db_rating.append(_)
    print(db_rating)
    return db_rating


def move_file(parent_path, file_name):
    try:
        shutil.move(f'{parent_path}/{file_name}', f"{parent_path}/trash")
    except (FileNotFoundError, shutil.Error) as e:
        print(e)
    else:
        print(file_name + " moved to trash")


def file_classification(file_info: list, parent_path):
    # get db_info by list and judge whether to move the file to trash or not

    # we create a trash folder to safely classify the files instead of deleting it
    # exceptions when the trash folder exists must be tempered
    createFolder(f'{parent_path}/trash')

    for i in file_info:
        jpg_version_file_name = i[0]
        raw_version_file_name = i[0][:-4] + ".ARW"

        if i[1] == "leave jpg":
            move_file(parent_path, raw_version_file_name)
        elif i[1] == "delete":
            move_file(parent_path, raw_version_file_name)
            move_file(parent_path, jpg_version_file_name)
def arw_moveRating(file_ratingInfo : list, con):
    cursor_db = con.cursor()

    for i in file_ratingInfo:

        temp_filename=i[0][:-4:]+".ARW"
        cursor_db.execute(f'UPDATE FileSystem_Nodes set rating="{i[1]}" where name="{temp_filename}"')
    con.commit()


def check(con):
    cursor_db = con.cursor()
    cursor_db.execute(
        f'SELECT COUNT(*) FROM FileSystem_Nodes  where label="Approved" and parentPath="{db_parent_path}" ')
    approved_file_count = cursor_db.fetchall()
    print("Approved files : " + str(approved_file_count) + "  files")

    cursor_db.execute(
        f'SELECT COUNT(*) FROM FileSystem_Nodes  where label="leave jpg" and parentPath="{db_parent_path}" ')
    jpg_only_file_count = cursor_db.fetchall()
    print("jpg left files : " + str(jpg_only_file_count) + "  files")

    orginal_folder_file_list = os.listdir(target_folder)
    orginal_folder_size = len([file for file in orginal_folder_file_list if file.endswith(".JPG")])
    print("original file count : " + str(orginal_folder_size))

    trash_folder_file_list = os.listdir(target_folder + "/trash")
    trash_folder_size = len([file for file in trash_folder_file_list if file.endswith(".JPG")])
    print("trash_folder count : " + str(trash_folder_size))

    if orginal_folder_size == approved_file_count[0][0] * 2 + jpg_only_file_count[0][0]:
        # originally the check formmula should be <orginal_folder_size == approved_file_count[0][0] *2  +
        # jpg_only_file_count[0][0]> but since we labeled the arw files as same as the jpg files the formula should
        # look like above
        print('--------------------------------')
        print("NO ERROR")
    else:
        print(" ERROR exists ")


def label_arw(con):
    # label arw files as same as the jpg file
    cursor_db = con.cursor()
    cursor_db.execute(
        f'UPDATE FileSystem_Nodes set label = "Approved" where sortName in (select REPLACE(sortName, "JPG", "ARW") as target_arw FROM FileSystem_Nodes where label="Approved" and parentPath="{db_parent_path}") ')
    con.commit()
def rate_arw(con):
    cursor_db= con.cursor()
    cursor_db.execute(f'UPDATE FileSystem_Nodes set rating ="5" where sortName in (select REPLACE(sortName, "JPG", "ARW") as target_arw FROM FileSystem_Nodes where rating="5" and parentPath="{db_parent_path}"))')



con = connection()
label_arw(con)
file_classification(read_name_label(con), target_folder)
arw_moveRating(read_rating(con),con)

#check(con)
