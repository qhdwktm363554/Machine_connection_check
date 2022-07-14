import pandas as pd
import numpy as np
from pandas.core.arrays.integer import Int64Dtype
import pymssql, os, glob

server_df = pd.read_excel("00_basic_config.xlsx")
server_df_1 = server_df.iloc[0:2:,0:3]
server_df_2 = server_df.iloc[:,3:]
# server_df_1.set_index('SERVER', inplace = True)
server_df_2.set_index('line', inplace = True)

username = 'sa'
password = 'solution'
database1 = 'SeojunAndon'
database2 = 'AK'

# sever 바뀔 경우 아래 수정 필요하다. 
# query_1은 하루/이틀 전에 각 라인 별로 machine이 몇개나 연결이 된건가
# query_2는 지난 7일 일별 총 row 수, 연결된 line 수
sql_query_1_original = "use SeojunAndon select Line ,count(distinct Station) as TotalMachines, cast(DateAdd(\"d\", -1, GETDATE())as date) as \"-1day\", count(dtCreated) as row_count from [SeojunAndon].[dbo].[PickupDetail] where cast(dtCreated as date) = cast(DateAdd(\"d\", -1, GETDATE())as date) group by Line"
sql_query_2_original = "select top (10) cast(dtCreated as date) as Datefield, count(cast(dtCreated as date)) as TotalRows, count(distinct Line) as TotalLines from [SeojunAndon].[dbo].[PickupDetail] group by cast(dtCreated as date)  order by cast(dtCreated as date) desc"
sql_query_1_backup = "use AKANDON select Line ,count(distinct Station) as TotalMachines, cast(DateAdd(\"d\", -1, GETDATE())as date) as \"-1day\", count(dtCreated) as row_count from [AKANDON].[dbo].[PickupDetail] where cast(dtCreated as date) = cast(DateAdd(\"d\", -1, GETDATE())as date) group by Line"
sql_query_2_backup = "select top (10) cast(dtCreated as date) as Datefield, count(cast(dtCreated as date)) as TotalRows, count(distinct Line) as TotalLines from [AKANDON].[dbo].[PickupDetail] group by cast(dtCreated as date)  order by cast(dtCreated as date) desc"

length = len(server_df_1['SERVER'])
for n,i in enumerate(range(length)):
    server_name = server_df_1.iloc[i,1]
    db_name = server_df_1.iloc[i,2]
    print(server_name, db_name)

    if n == 0:
        # cnxn = pymssql.connect(server_name, username, password, db_name, port='1433')
        cnxn = pymssql.connect(server_name, username, password, db_name, )

        curs = cnxn.cursor()
        curs.execute(sql_query_1_original)
        row = curs.fetchall()
        Column_names = ['line', 'StQty_O', 'Date_O', 'RowNr_O']
        df = pd.DataFrame(row, columns=Column_names)
        # 'line'을 동시에 index로 지정한다. 
        df.set_index('line', inplace = True)

        curs_2 = cnxn.cursor()
        curs_2.execute(sql_query_2_original)
        row_2 = curs_2.fetchall()
        Column_names_2 = ['Date', 'RowNr_O',"LineQty_O"]
        df2 = pd.DataFrame(row_2, columns = Column_names_2)
        df2.set_index('Date', inplace = True)
        print(f"okay server {server_name} is finished")
        
        # print(df)
        # print("----------------------------------------------------")
        # print(df2)           
    else:
        cnxn_2 = pymssql.connect(server_name, username, password, db_name)

        curs_3 = cnxn_2.cursor()
        curs_3.execute(sql_query_1_backup)
        row_3 = curs_3.fetchall()
        Column_names = ['line', 'StQty_B', 'Date_B', 'RowNr_B']
        df3 = pd.DataFrame(row_3, columns=Column_names)
        # 'line'을 index로 지정한다. 
        df3.set_index('line', inplace = True)

        curs_4 = cnxn_2.cursor()
        curs_4.execute(sql_query_2_backup)
        row_4 = curs_4.fetchall()
        Column_names_2 = ['Date', 'RowNr_B',"LineQty_B"]
        df4 = pd.DataFrame(row_4, columns = Column_names_2)
        df4.set_index('Date', inplace = True)
        
        # print(df3)
        # print("----------------------------------------------------")
        # print(df4)      

df_connected_machine = pd.concat([server_df_2,df, df3],1)
df_connected_machine = df_connected_machine[['Date_O','StQty','StQty_O', 'StQty_B', 'RowNr_O', 'RowNr_B']]
df_connected_machine['Comparison'] = np.where((df_connected_machine['StQty'] ==df_connected_machine['StQty_O']) & (df_connected_machine['StQty'] ==df_connected_machine['StQty_B']) , 'OK', 'NGNG')

df_daily = pd.concat([df2, df4], 1)
df_daily = df_daily[['RowNr_O', 'RowNr_B', 'LineQty_O', 'LineQty_B']]
df_daily['RowNr_CP'] = np.where(df_daily['RowNr_O'] == df_daily['RowNr_B'], 'OK', 'NG')
df_daily['LineQty_CP'] = np.where(df_daily['LineQty_O'] == df_daily['LineQty_B'], 'OK', 'NG')
df_daily = df_daily[['RowNr_O', 'RowNr_B', 'RowNr_CP','LineQty_O', 'LineQty_B', 'LineQty_CP']]

print("*******Yesterday connection status**************")
print(df_connected_machine)
print("----------------------------------------------------------------------------------")
print("*******Connection over the last 10 days***********")
print(df_daily)





# import sys
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QTableView
# from PyQt5.QtCore import QAbstractTableModel, Qt


# class pandasModel(QAbstractTableModel):

#     def __init__(self, data):
#         QAbstractTableModel.__init__(self)
#         self._data = data

#     def rowCount(self, parent=None):
#         return self._data.shape[0]

#     def columnCount(self, parnet=None):
#         return self._data.shape[1]

#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid():
#             if role == Qt.DisplayRole:
#                 return str(self._data.iloc[index.row(), index.column()])
#         return None

#     def headerData(self, col, orientation, role):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return self._data.columns[col]
#         return None

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
    
#     model = pandasModel(df_connected_machine)
#     view = QTableView()

#     model_2 = pandasModel(df_daily)
#     view_2 = QTableView()

#     view.setModel(model)
#     view.resize(1000, 600)
#     view.show()

#     view_2.setModel(model_2)
#     view_2.resize(1000, 600)
#     view_2.show()

#     sys.exit(app.exec_())