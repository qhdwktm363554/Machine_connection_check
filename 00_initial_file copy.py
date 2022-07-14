import pandas as pd
import numpy as np
from pandas.core.arrays.integer import Int64Dtype
import pymssql, os, glob

server_df = pd.read_excel("00_basic_config.xlsx")
server_df_1 = server_df.iloc[0:2:,0:3]
server_df_2 = server_df.iloc[:,3:]
server_df_1.set_index('SERVER', inplace = True)
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
        
df1['MACHINES_original'] = df1['MACHINES_original'].astype(str).astype(int)
df2['MACHINES_backup'] = df2['MACHINES_backup'].astype(str).astype(int)

new_df = pd.concat([server_df_2, df1, df2], 1)

new_df['Comparison'] = np.where((new_df['MACHINES'] ==new_df['MACHINES_original']) & (new_df['MACHINES'] ==new_df['MACHINES_backup']) , 'OKOK', 'NG_1')
print(new_df)

new_df = new_df.reset_index()

import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = pandasModel(new_df)
    view = QTableView()
    view.setModel(model)
    view.resize(1000, 600)
    view.show()
    sys.exit(app.exec_())