# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:47:44 2020
"""

import dropbox
import json
import pandas as pd

#reads the list of files in dropbox
def read_file_data(path):
    response = dbx.files_list_folder(path)
    filename = [file.name for file in response.entries]
    date = [file.client_modified for file in response.entries]
    path = [file.path_lower for file in response.entries]
    data = {'file_name': filename, 'date': date, 'path': path}
    current_files = pd.DataFrame(data)
    return current_files

#saves a list of current files on Dropbox-> in local system and on dropbox in jason format
def save_current_files(drop_box_path):
    response = dbx.files_list_folder(drop_box_path)
    filename = [file.name for file in response.entries]
    date = [file.client_modified for file in response.entries]
    path = [file.path_lower for file in response.entries]
    # dirpath = '/Online portal/DATA'
    
    #saves a local file to keep record of all the files that have been listed in Dropbox directory
    dirpath = "C:/Users/13022/Desktop/website/Automation"
    data = {'file_name': filename, 'date': date, 'path': path}
    current_files = pd.DataFrame(data)
    # print(path)
    # save json file to dropbox folder to pathdir
    current_files.to_json(path_or_buf=dirpath+"/current_files.json",orient='split')
    # dbx.files_upload("Potential headline: Game 5 a nail-biter as Warriors inch out Cavs", '/cavs vs warriors/game 5/story.txt')
    file_name="current_files.json"
#    The files_upload() function does the upload. 
#You need to first open the file on your local computer with open(). 
#I am assuming the file is stored in the same folder as your Python script. 
#This returns a file handler f. Then pass f to the files_upload().
# This is the first argument. The next argument is the path you want the file to be uploaded to dropbox. 
#It has to start with ‘/’, then the file name (including additional path). 
#You don’t have to preserve file name. The third argument is useful. 
#When you sent mute to True, you won’t get notification for the file upload. 
#If you are making a camera trap, you don’t want your PC flooded with Dropbox notifications just because a bunny decides to visit your backyard.
#    overwriting the file on Dropbox each time to save current files in it updated.
#    The file on Dropbox has the last checked list of all files
    with open(file_name, 'rb') as f:
        dbx.files_upload(f.read(),drop_box_path+'/'+ file_name, mode=dropbox.files.WriteMode.overwrite,mute=True)
 
    # dbx.files_download_to_file('Copy of '+file_name,dropbox_path+file_name)

def read_current_files(path=None):
    if(path==None):
        data =pd.read_json (path_or_buf='current_files.json',orient='split')
    else:
        data =pd.read_json (path_or_buf=path+'/current_files.json',orient='split')
    return data

def check_for_change(path):
    file_name="current_files.json"
    dbx.files_download_to_file('Copy of '+file_name,path+'/'+file_name)
   #    read the last list that is stored in current_files.json
    old_data = read_current_files(None)
    #    reads Today's list of files in dropbox and prints them
    new_data = read_file_data(path)

    if(old_data.equals(new_data)==False):
        df = pd.concat([old_data, new_data]) # concat dataframes
        df = df.reset_index(drop=True) # reset the index
        df_gpby = df.groupby(list(df.columns)) #group by
        idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1] #reindex
        # print(df)
        print(df.loc[idx])
#    old_data = read_current_files(None)
#    new_data = read_file_data(path)
#
#    if(old_data.equals(new_data)==False):
#        df = pd.concat([old_data, new_data]) # concat dataframes
#        df = df.reset_index(drop=True) # reset the index
#        df_gpby = df.groupby(list(df.columns)) #group by
#        idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1] #reindex
#        print(idx)

if __name__ == '__main__':
#    The function dropbox.Dropbox() returns an object. You can use this object to upload or download files and more.
    dbx = dropbox.Dropbox("SVnX-m4DCRoAAAAAAAAJ69PpiChdX1zrt3S7lqxxe1MsYYIHleNsizLhqsCUfiRp")
    
    path = '/Online portal/DATA'
#    save_current_files(path)
    check_for_change(path)
    
#    reads Today's list of files in dropbox and prints them
#    print(read_file_data(path))
#    read the last list that is stored in current_files.json
#    print(read_current_files())
#    check_for_change(path)
    drop_box_path = '/Online portal/DATA'
#    read_file_data(path)
    save_current_files(drop_box_path)
    



