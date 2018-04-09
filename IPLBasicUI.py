from tkinter import *
from playerInfo import player_info
from pymysql import *
import pymysql as Mysqldb
from tkinter import messagebox
import table
ui = Tk()
ui.title("mini IPL Auction 126-127-128")
turn, highest_bidder = 0, 0
turn_team = Label()
curr_player = PhotoImage()
label_mi, label_kkr, label_rcb, label_rr, label_player_photo, stats, label_player_price = Label(), Label(), Label(), Label(), Label(), Label(), Label()
spin_box = Spinbox()
max_quote = 400000
pic_no = 1
z = 0
pic_no1 = 1
check = 0
b = 1
c = 1
def action_pass(a):
    global turn, pic_no, turn_team, check, spin_box, max_quote
    label_mi.config(borderwidth=4, relief='flat')
    label_rr.config(borderwidth=4, relief='flat')
    label_kkr.config(borderwidth=4, relief='flat')
    label_rcb.config(borderwidth=4, relief='flat')

    def update_player_stats(name, matches, runs, wickets, sr, avg):
        stats.config(text="Name: "+name+"\nMatches: "+matches+"\nRuns: "+runs+"\nWickets: "+wickets+"\nStrike Rate: "+sr+"\nAverage: "+avg)

    x = turn % 4
    if x == 2:
        # chance of second team
        turn_team.config(text="Rajasthan Royals\n Do you want to BID?")
        # TODO: highlight somehow
        if a == 2:
            check = 2
        label_rr.config(borderwidth=6, relief='solid')

    elif x == 3:
        # chance of 3rd team
        turn_team.config(text="Kolkata Knight Riders\n Do you want to BID?")
        # TODO: highlight somehow
        if a == 2:
            check = 3
        label_kkr.config(borderwidth=6, relief='solid')

    elif x == 0:
        # chance of 4th team
        turn_team.config(text="Royal Challengers Bangalore\n Do you want to BID?")
        # TODO: highlight somehow
        if a == 2:
            check = 4
        label_rcb.config(borderwidth=6, relief='solid')

    elif x == 1:
        # chance of 1st team
        turn_team.config(text="Mumbai Indians\n Do you want to BID?")
        label_mi.config(borderwidth=6, relief='solid')
        # TODO: highlight somehow
        if a == 2:
            check = 1
    if turn % 12 == 0 and turn > 0:
        turn += 1
        pic_no += 1
        if pic_no == 9:
            messagebox.showinfo("Auction Complete", "Auction Complete!")
            table.create_table()
        file = 'assets/' + str(pic_no) + '.png'
        curr_player.config(file=file)
        curr_player.subsample(2)
        label_player_photo.config(image=curr_player)
        pi = player_info[str(pic_no)]
        update_player_stats(pi['name'], str(pi['matches']), str(pi['runs']), str(pi['wickets']), str(pi['strike_rate']),
                            str(pi['average']))
        max_quote = 500000
        spin_box = Spinbox(from_=500000, to=5000000, increment=100000)
        spin_box.place(x=525, y=550, height=25, width=150)
        label_player_price.config(text='Current highest bid for this player is Rs. ' + str(max_quote))
        if a==2:
            return (2, check)
        elif a==1:
            if check == 1:
                db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
                cursors = db.cursor()
                global pic_no1
                d = player_info[str(pic_no1)]
                sql = "INSERT INTO RCB(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
                cursors.execute(sql, (d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
                pic_no1 += 1
                db.commit()
            elif check == 0:
                db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
                cursors = db.cursor()
                d = player_info[str(pic_no1)]
                sql = "INSERT INTO KKR(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
                cursors.execute(sql, (d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
                pic_no1 += 1
                db.commit()
            elif check == 3:
                db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
                cursors = db.cursor()
                d = player_info[str(pic_no1)]
                sql = "INSERT INTO RR(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
                cursors.execute(sql, (d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
                pic_no1 += 1
                db.commit()
            elif check == 2:
                db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
                cursors = db.cursor()
                d = player_info[str(pic_no1)]
                sql = "INSERT INTO MI(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
                cursors.execute(sql, (d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
                pic_no1 += 1
                db.commit()
    elif turn%12!=0 or turn==0:
        turn+=1
    return(1,check)

def action_bid():
    global max_quote, turn, b,c, highest_bidder
    curr_quote = spin_box.get()
    curr_quote = int(curr_quote)
    if curr_quote > max_quote:
        max_quote = curr_quote
        highest_bidder = turn % 4
        print("highest bidder is ",highest_bidder)
        label_player_price.config(text = 'Current highest bid for this player is Rs. '+str(max_quote))
        b,c = action_pass(2)
    else:
        msg = "FOR BIDDING YOUR BID PRICE MUST BE GREATER THAN PREVIOUS BID VALUE"
        messagebox.showinfo("You Got some trouble",msg)
    if b==2:
        if highest_bidder==1:
            db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
            cursors = db.cursor()
            global pic_no1
            d = player_info[str(pic_no1)]
            sql = "INSERT INTO RCB(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
            cursors.execute(sql,(d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
            pic_no1 += 1
            db.commit()
        elif highest_bidder==0:
            db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
            cursors = db.cursor()
            d = player_info[str(pic_no1)]
            sql = "INSERT INTO KKR(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
            cursors.execute(sql, (d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
            pic_no1 += 1
            db.commit()
        elif highest_bidder==3:
            db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
            cursors = db.cursor()
            d = player_info[str(pic_no1)]
            sql = "INSERT INTO RR(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
            cursors.execute(sql, (d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
            pic_no1 += 1
            db.commit()
        elif highest_bidder==2:
            db = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
            cursors = db.cursor()
            d = player_info[str(pic_no1)]
            sql = "INSERT INTO MI(name,matches,runs,wickets,strike_rate,average) VALUES(%s,%s,%s,%s,%s,%s)"
            cursors.execute(sql, (d['name'], d['matches'], d['runs'], d['wickets'], d['strike_rate'], d['average']))
            pic_no1 += 1
            db.commit()

        if pic_no1 == 9:
            messagebox(text = "Auction Complete!")
            table.create_table()


def display_player_list():
    player_frame = Frame(ui, height="670", width="1200", )
    background_image = PhotoImage(file="assets/wallpaper.png")
    # background_image = background_image.subsample(2)
    background_label = Label(image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    p1 = PhotoImage(file="assets/1.png").subsample(2)
    Label(image=p1).place(x=10, y=100, width=250, height=200)
    Label(text="R Ashwin").place(x=10, y=310)

    p2 = PhotoImage(file="assets/2.png").subsample(2)
    Label(image=p2).place(x=310, y=100, width=250, height=200)
    Label(text="Yuvraj S").place(x=310, y=310)

    p3 = PhotoImage(file="assets/3.png").subsample(2)
    Label(image=p3).place(x=610, y=100, width=250, height=200)
    Label(text="H Pandya").place(x=610, y=310)

    p4 = PhotoImage(file="assets/4.png").subsample(2)
    Label(image=p4).place(x=910, y=100, width=250, height=200)
    Label(text="M S Dhoni").place(x=910, y=310)

    p5 = PhotoImage(file="assets/5.png").subsample(2)
    Label(image=p5).place(x=10, y=400, width=250, height=200)
    Label(text="R Jadeja").place(x=10, y=610)

    p6 = PhotoImage(file="assets/6.png").subsample(2)
    Label(image=p6).place(x=310, y=400, width=250, height=200)
    Label(text="S Raina").place(x=310, y=610)

    p7 = PhotoImage(file="assets/7.png").subsample(2)
    Label(image=p7).place(x=610, y=400, width=250, height=200)
    Label(text="Virat K").place(x=610, y=610)

    p8 = PhotoImage(file="assets/8.png").subsample(2)
    Label(image=p8).place(x=910, y=400, width=250, height=200)
    Label(text="R Sharma").place(x=910, y=610)

    player_frame.pack()
    ui.mainloop()

def start_auction():
    global turn_team, label_kkr, label_mi, label_rcb, label_rr, curr_player, label_player_photo, spin_box, stats, label_player_price
    auction_frame = Frame(ui, bg="black", height="670", width="1150", )
    background_image = PhotoImage(file="assets/wallpaper.png")
    background_label = Label(image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    MI = PhotoImage(file="assets/MI.png").subsample(2)
    label_mi = Label(image=MI, borderwidth=6, relief='flat')
    label_mi.place(x=100, y=12, width=300, height=300)
    # Label(text="Yuvraj S").place(x=310, y=310)

    RR = PhotoImage(file="assets/RR.png").subsample(2)
    label_rr = Label(image=RR, borderwidth=0, relief='flat')
    label_rr.place(x=950, y=12, width=300, height=300)

    KKR = PhotoImage(file="assets/KKR.png").subsample(2)
    label_kkr = Label(image=KKR)
    label_kkr.place(x=100, y=390, width=300, height=300)

    RCB = PhotoImage(file="assets/RCB.png").subsample(2)
    label_rcb = Label(image=RCB, borderwidth=6, relief='solid')
    label_rcb.place(x=950, y=390, width=300, height=300)

    curr_player = PhotoImage(file='assets/1.png')
    curr_player.subsample(2)
    label_player_photo = Label(image=curr_player)
    label_player_photo.place(x=525, y=50, width=300)

    pi = player_info['1']
    stats = Label(
        text="Name: "+pi['name']+"\nMatches: "+str(pi['matches'])+"\nRuns: "+str(pi['runs'])+"\nWickets: "+str(pi['wickets'])+"\nStrike Rate: "+str(pi['strike_rate'])+"\nAverage: "+str(pi['average']),
        font=('Helvetica', 10, "bold"))
    stats.place(x=525, y=350, width=300)

    turn_team = Label(bg="white", text="\n Do you want to start BID?", font=("Helvetica", 16, "bold"))
    turn_team.place(x=525, y=450, width=300, height=80)
    def Buttons():
        btn_pass = Button(height=1, width=20, text="PASS", bg="white", command=lambda: action_pass(1)).place(x=775, y=550, width=50)
        btn_bid = Button(height=1, width=20, text="BID", bg="white", command=lambda: action_bid()).place(x=700, y=550, width=50)
    start = Button(height=1, width=50, text="Start", bg="white",command=Buttons).place(x=700, y=550, width=50)
    spin_box = Spinbox(from_=500000, to=5000000, increment=100000)
    spin_box.place(x=525, y=550, height=25, width=150)
    label_player_price = Label(bg="white", text="Current highest bid for this player is Rs. 500000")
    label_player_price.place(x=525, y=600, width=300)

    auction_frame.pack()
    ui.mainloop()


main_frame = Frame(ui, height="670", width="1150", )

background_image = PhotoImage(file="assets/ipl-auction.png")
background_image = background_image.zoom(2)
background_label = Label(image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


conn = Mysqldb.connect('localhost', 'root', '9802', 'ipl')
curs1 = conn.cursor()
sql_truncate = "TRUNCATE "
curs1.execute(sql_truncate + "MI")
curs1.execute(sql_truncate + "KKR")
curs1.execute(sql_truncate + "RR")
curs1.execute(sql_truncate + "RCB")
conn.close()

btn_start_auct = Button(height=1,
                        width=20,
                        text="START AUCTION",
                        bg="gray", font=('Helvetica', 12, "bold"),
                        command=start_auction)\
                        .place(x=650, y=500)
btn_player_list = Button(height=1,
                         width=20,
                         text="PLAYER LIST",
                         bg="gray", font=('Helvetica', 12, "bold",),
                         command=display_player_list) \
                        .place(x=900, y=500)

main_frame.pack()
ui.mainloop()
