import sqlite3
con = sqlite3.connect('db.sqlite3')
def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT name from sqlite_master where type= "table"')

    #cursorObj.execute('DELETE FROM DjangoEcommerceApp_categories_images;')
    #cursorObj.execute('DELETE FROM DjangoEcommerceApp_categories_images where id=5;')
    #cursorObj.execute('DELETE FROM DjangoEcommerceApp_categories_images;');
    #print('We have deleted', cursorObj.rowcount, 'records from the table.')

    # Commit the changes to db
    #con.commit()

    cursorObj.execute('SELECT * from DjangoEcommerceApp_Jewellery_store_cat')


    #cursorObj.execute('SELECT name from sqlite_master where type= "table"')
    print(cursorObj.fetchall())
    data = cursorObj.fetchall()
    for da in data:
        print(da.alotted,da)
sql_fetch(con)
