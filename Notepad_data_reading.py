import pandas as pd
import numpy as np
from pandas.core.arrays.integer import Int64Dtype
import pymssql, os, glob

server_df = pd.read_excel("00_basic_config.xlsx")
server_df_1 = server_df.iloc[0:2:,0:2]
server_df_2 = server_df.iloc[:,3:]
server_df_2.set_index('LINE', inplace = True)

cwd = os.getcwd()
file_path = os.path.join(cwd, 'test_original_server.txt')
TEXT_FILE_NAMES = ["D:\\09.python\\15.Connection_check\\test_original_server.txt", "D:\\09.python\\15.Connection_check\\test_backup_server.txt"]


for k, i in enumerate(TEXT_FILE_NAMES):
    f = open(i)
    a = f.readlines()
    line_list = []
    nr_list = []
    for n, i in enumerate(a):
        if n == 0: pass
        else: 
            val = i.split("\t")
            val_2 = val[1].replace("\n","")
            line_list.append(val[0])
            nr_list.append(val_2)
    if k == 0: 
        df1 = pd.DataFrame({'LINE': line_list, 'MACHINES_original': nr_list})   
        df1.set_index('LINE', inplace = True)
        
    else:
        df2 = pd.DataFrame({'LINE': line_list, 'MACHINES_backup': nr_list})
        df2.set_index('LINE', inplace = True)