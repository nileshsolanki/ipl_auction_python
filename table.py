from tkinter import *
import pymysql as Mysqldb

def populate_table(curse, a, b, root):
    col_count = 6
    row_count = curse.rowcount
    result = curse.fetchall()
    print(result)
    x1,y1=a,b
    j = 0
    for i in range (0,row_count):
        Label(root, bg="white", text=result[j][0]).place(x=x1, y=y1, width=200)
        y1 += 30
        j+=1




def create_table():
    ui_table = Tk()

    ui_table.title("AUCTION RESULTS")

    table_frame = Frame(ui_table, height="670", width="1150")
    Label(ui_table, text = "Kolkata Knight Riders").place(x=50,y=10, width=200)
    Label(ui_table, text="Mumbai Indians").place(x=300, y=10, width=200)
    Label(ui_table, text="Rajasthan Royals").place(x=600, y=10, width=200)
    Label(ui_table, text="Royal Challengers Of Bangalore").place(x=900, y=10, width=200)

    connection = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
    columns = 6
    sql_common = "SELECT * FROM "
    cursor = connection.cursor()

    cursor.execute(sql_common + "KKR;")
    populate_table(cursor, 50,50, ui_table)

    cursor.execute(sql_common + "MI;")
    populate_table(cursor, 300, 50, ui_table)

    cursor.execute(sql_common + "RR;")
    populate_table(cursor, 600, 50, ui_table)

    cursor.execute(sql_common + "RCB;")
    populate_table(cursor, 900, 50, ui_table)

    cursor.close()

    table_frame.pack()
    ui_table.mainloop()


# create_table()