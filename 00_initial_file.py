import pandas as pd
import numpy as np
import pymssql, os

server_df = pd.read_excel("00_basic_config.xlsx")

df1 = server_df.iloc[0:2:,0:2]
df2 = server_df.iloc[:,2:]

#DB에 접근하기
server1 = df1.loc[df1['SERVER'] =='original_server', "HOST"].values[0]
server2 = df1.loc[df1['SERVER'] =='backup_server', "HOST"].values[0]
username = 'sa'
password = 'solution'
database1 = 'SeojunAndon'
database2 = 'AK'


# df_ori_server = 

# sever 바뀔 경우 아래 수정 필요하다. 
# query_1은 하루/이틀 전에 각 라인 별로 machine이 몇개나 연결이 된건가
# query_2는 지난 7일 일별 총 row 수, 연결된 line 수
# sql_query_1_original = "use SeojunAndon select Line ,count(distinct Station) as TotalMachines, cast(DateAdd("d", -1, GETDATE())as date) as "-1day" from [SeojunAndon].[dbo].[PickupDetail] where cast(dtCreated as date) = cast(DateAdd("d", -1, GETDATE())as date) group by Line"
sql_query_2_original = "select top (7) cast(dtCreated as date) as Datefield, count(cast(dtCreated as date)) as TotalRows, count(distinct Line) as TotalLines from [SeojunAndon].[dbo].[PickupDetail] group by cast(dtCreated as date)  order by cast(dtCreated as date) desc"
# sql_query_1_backup = "use AKANDON select Line ,count(distinct Station) as TotalMachines, cast(DateAdd("d", -2, GETDATE())as date) as "-2day" from [AKANDON].[dbo].[PickupDetail] where cast(dtCreated as date) = cast(DateAdd("d", -2, GETDATE())as date) group by Line"
# sql_query_2_backup = "select top (7) cast(dtCreated as date) as Datefield, count(cast(dtCreated as date)) as TotalRows, count(distinct Line) as TotalLines from [AKANDON].[dbo].[PickupDetail] group by cast(dtCreated as date)  order by cast(dtCreated as date) desc"


# print(df1)
for i in range(2):
    server_name = df1.iloc[i,1]
    db_name = df1.iloc[i,2]
    print(server_name, db_name)
    cnxn = pymssql.connect(server_name, username, password, db_name)
    curs = cnxn.cursor()
    curs.execute(sql_query_2_original)
    row = curs.fetchall()
    df = pd.DataFrame(row)
    print(df)
    break