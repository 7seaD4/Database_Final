from re import A
import tkinter
from tkinter import ttk #Ttk widgets gives the application an improved look and feel
from tkinter import messagebox
import sqlite3
import os
from variables import *

        #storemainGUI()�ɌĂяo�����GUI�͑S��user_id���Q�Ƃ���B
        #bookcatalogue�ꗗ����I�� -> �I����ʂ����C���E�B���h�E��GUI(user_id)
            #�ꗗ�X�N���[���@���@���C���ɒ��t���E���t���[���i�L�����o�X���j
            #�J�^���O�̃t�B���^�����O �����t���[��
            #���v���z�̌v�Z�@���@��O�t���[��
        #�I���ꗗ�@���@�I�[�o�[���C�t���[�����̇@
            #���v���z�@���@function
            #�I���ꗗ����J�^���O�ɖ߂��K�v������@���@�I���ꗗ.place_forget()
        #��v�@���@�I�[�o�[���C�t���[�����̇A
            #�x�������@�̑I���@��
                #�x�������@�̓��́@���@�I�[�o�[�������̇B
                    #�x�������@�̕ۑ��@���@function
        #�w�������̕ۑ�
            #book��sold��available�̃A�b�v�f�[�g
            #account��saved_payment�̃A�b�v�f�[�g
            #orders�ɒǉ�

        #�A�J�E���g���̕ύX
            #user_id�ȊO�͑S��
            #saved_payment�͈ꂩ��ύX�̋���
        #�ߋ��̍w�������̊m�F
            #�����̃t�B���^�����O

#BuyBooksGUI: set the BuyBooks window's appearance and actions
class BuyBooksGUI():
    def __init__(self, user_id): #storemainGUI()�ɌĂяo�����GUI�͑S��user_id���Q�Ƃ���B
        self.user_id = user_id
        self.cursor = db.cursor()

    #Set the appearance
        self.selectbook_window = tkinter.Tk() #bookcatalogue�ꗗ����I�� -> �I����ʂ����C���E�B���h�E��GUI(user_id)
        self.selectbook_window.title("Order Books [User ID: %s]" %self.user_id)
        self.selectbook_window.geometry(multiframe_geo)
        self.selectbook_window.config(bg = bg_normal)

        self.selectbook_window_mid = tkinter.Frame(height = 125, width = multiframe_w, bg = bg_normal) #�J�^���O�̃t�B���^�����O �����t���[��
        self.selectbook_window_bot = tkinter.Frame(height = 175, width = multiframe_w, bg = bg_normal) #���v���z�̌v�Z�@���@��O�t���[��
        self.purchase_window_top = tkinter.Frame(height = 30, width = multiframe_w, bg = bg_normal) #��v�@���@�I�[�o�[���C�t���[�����̇A
        self.purchase_window_bot = tkinter.Frame(height = 300, width = multiframe_w, bg = bg_normal) #��v�@���@�I�[�o�[���C�t���[�����̇A
        self.method_window_main = tkinter.Frame(height = multiframe_h, width = multiframe_w, bg = bg_normal) #�x�������@�̓��́@���@�I�[�o�[�������̇B
        self.method_window_card = tkinter.Frame(height = 300, width = multiframe_w, bg = bg_method)
        self.method_window_cash = tkinter.Frame(height = 150, width = multiframe_w, bg = bg_method)
        self.method_window_bank = tkinter.Frame(height = 300, width = multiframe_w, bg = bg_method)

        self.canvas = tkinter.Canvas(self.selectbook_window, bg =bg_normal, height = 275, width= multiframe_w) #�ꗗ�X�N���[���@���@���C���ɒ��t���E���t���[���i�L�����o�X���j

        # Scrollbar �𐶐����Ĕz�u
        self.bar = tkinter.Scrollbar(self.selectbook_window, orient=tkinter.VERTICAL)
        
        self.bar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.bar.set)
        

        # Frame Widget�� ����
        #frame = tkinter.Frame(canvas,height = 200, width = multiframe_w, bg = bg_label) #�ꗗ�X�N���[���@���@���C���ɒ��t���E���t���[���i�L�����o�X���j

        # Frame Widget�� Canvas Widget��ɔz�u

        maxid = self.cursor.execute('SELECT Max(book_id) FROM books').fetchone()[0]
        maxprice = self.cursor.execute('SELECT Max(price) FROM books').fetchone()[0]
        maxavailable = self.cursor.execute('SELECT Max(available) FROM books').fetchone()[0]
        if maxid != None:
            self.orderbooks = [0]* (maxid + 1)
        else: self.orderbooks = [0]
        if maxprice == None:
            maxprice = 0
        if maxavailable == None:
            maxavailable = 0
        self.subtotal = 0
        self.qtytotal = 0

    #Set the actions
        def cancel():
            self.cursor.close()
            self.selectbook_window.destroy()
            from main import StoreMainGUI
            StoreMainGUI(self.user_id)
        

        def calctotalprice():
            self.subtotal = 0
            self.qtytotal = 0
            for i in range(0, len(self.listofbooks)):
                if int(self.numberofbooks[i].get()) > self.listofbooks[i][5]:
                    messagebox.showwarning(title = "ERROR", message = (self.listofbooks[i][1] + " is added more than available number of books"))
                else:
                    self.subtotal = (float(self.priceofbooks[i]) * int(self.numberofbooks[i].get())) + self.subtotal
                    self.qtytotal = int(self.numberofbooks[i].get()) + self.qtytotal
                    self.total_head.place_forget()
                    self.total_head = tkinter.Label(self.selectbook_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(round(self.subtotal, 2))), font=font_normal_bold, fg=fc_label, bg=bg_label)
                    self.total_head.place(x=300, y=10)
                    self.orderbooks[self.listofbooks[i][0]] = self.numberofbooks[i].get()
                    
            

        # ������ Button Widget �������AFrame��ɔz�u = �X�N���[�����Ė{��I�ԂƂ�������𐬗�������
        
        self.listofbooks = []
        self.priceofbooks = []
        self.numberofbooks = []
        def createbookslist(conn):
            self.listofbooks = []
            self.priceofbooks = []
            self.numberofbooks = []
            self.bookcatalogue = tkinter.Frame(self.canvas,height = 200, width = multiframe_w, bg = bg_label)

            self.canvas.config(height = 275)
            self.canvas.create_window((0,0), window=self.bookcatalogue, anchor=tkinter.NW, width=self.canvas.cget('width'))
            selectedbooks = conn.fetchall()
            self.canvas.config(scrollregion=(0,0,50,len(selectedbooks)*30)) #�X�N���[���͈�
            title_head = create_label_frame_small(self.bookcatalogue, "Title")
            author_head = create_label_frame_small(self.bookcatalogue, "Author")
            publisher_head = create_label_frame_small(self.bookcatalogue, "Publisher")
            price_head = create_label_frame_small(self.bookcatalogue, "Price")
            available_head = create_label_frame_small(self.bookcatalogue, "Availablity")
            qty_head = create_label_frame_small(self.bookcatalogue, "Qty")

            title_head.grid(row = 0, column = 1)
            author_head.grid(row = 0, column = 2)
            publisher_head.grid(row = 0, column = 3)
            price_head.grid(row = 0, column = 4)
            available_head.grid(row = 0, column = 5)
            qty_head.grid(row = 0, column = 6)
            
            for bk in selectedbooks:
                self.listofbooks.append(bk)
                var = tkinter.DoubleVar()
                title = tkinter.Label(self.bookcatalogue, text= str(bk[1]), font=font_small, fg=fc_label, bg=bg_label)
                author = tkinter.Label(self.bookcatalogue, text= str(bk[2]), font=font_small, fg=fc_label, bg=bg_label)
                publisher = tkinter.Label(self.bookcatalogue, text= str(bk[3]), font=font_small, fg=fc_label, bg=bg_label)
                price = tkinter.Label(self.bookcatalogue, text= ("$" + str(bk[4])), font=font_small, fg=fc_label, bg=bg_label)
                available = tkinter.Label(self.bookcatalogue, text= str(bk[5]), font=font_small, fg=fc_label, bg=bg_label)
                unavailable = tkinter.Label(self.bookcatalogue, text= "Unavailable", font=font_small, fg=fc_label, bg=bg_label)
                numofbk = tkinter.Spinbox(self.bookcatalogue, from_=0, to=bk[5], width = 20, command = calctotalprice)
                numofbk.configure(width = 5)
                numofbk.delete(0)
                if self.orderbooks[bk[0]] != 0:
                    numofbk.insert(0, int(self.orderbooks[bk[0]]))
                else:
                    numofbk.insert(0,0)
                self.priceofbooks.append(bk[4])
                self.numberofbooks.append(numofbk)
                title.grid(row = len(self.priceofbooks) + 1, column = 1, sticky = tkinter.W)
                author.grid(row = len(self.priceofbooks) + 1, column = 2, sticky = tkinter.W)
                publisher.grid(row = len(self.priceofbooks) + 1, column = 3, sticky = tkinter.W)
                price.grid(row = len(self.priceofbooks) + 1, column = 4, sticky = tkinter.W)
                available.grid(row = len(self.priceofbooks) + 1, column = 5)
                if bk[5] != 0:
                    numofbk.grid(row = len(self.priceofbooks) + 1, column=6)
                else:
                    unavailable.grid(row = len(self.priceofbooks) + 1, column=6)

            self.bar.pack(side=tkinter.RIGHT, pady=120, ipady =158, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 125)

        createbookslist(self.cursor.execute('SELECT * FROM books'))
        
        

        def filterbooks():
            def is_positivenum(n):
                try:
                    float(n)
                except ValueError:
                    return False
                else:
                    if float(n) < 0:
                        return False
                    else:
                        return True
                
            if self.price_min_entry.get() == "" or is_positivenum(self.price_min_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Minimum price is empty or invalid input"))
            elif self.price_max_entry.get() == "" or is_positivenum(self.price_max_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Maximum price is empty or invalid input"))
            elif self.available_min_entry.get() == "" or is_positivenum(self.available_min_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Minimum available is empty or invalid input"))
            elif self.available_max_entry.get() == "" or is_positivenum(self.available_max_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Maximum available is empty or invalid input"))
            elif self.price_min_entry.get() > self.price_max_entry.get():
                messagebox.showwarning(title = "ERROR", message = ("Minimum price is greater than Maximum price"))
            elif self.available_min_entry.get() > self.available_max_entry.get():
                messagebox.showwarning(title = "ERROR", message = ("Minimum avilable is greater than Maximum available"))
            else:
                self.bookcatalogue.destroy()
                row = [("%" + self.title_entry.get() + "%"), ("%" + self.author_entry.get() + "%"),("%" + self.publisher_entry.get() + "%"),
                       self.price_min_entry.get(), self.price_max_entry.get(), self.available_min_entry.get(), self.available_max_entry.get()]
                self.listofbooks = []
                self.priceofbooks = []
                self.numberofbooks = []
                createbookslist(self.cursor.execute('SELECT * FROM books WHERE \
                                                    title LIKE ? AND\
                                                    author LIKE ? AND\
                                                    publisher LIKE ? AND\
                                                    ? <= price AND price <= ? AND\
                                                    ? <= available AND available <= ?',
                                                    row))
        def filterreset():
            if len(self.title_entry.get()) != 0: self.title_entry.delete(0, len(self.title_entry.get()))
            if len(self.author_entry.get()) != 0: self.author_entry.delete(0, len(self.author_entry.get()))
            if len(self.publisher_entry.get()) != 0: self.publisher_entry.delete(0, len(self.publisher_entry.get()))
            
            if len(self.price_min_entry.get()) != 0: self.price_min_entry.delete(0, len(self.price_min_entry.get()))
            self.price_min_entry.insert(0, int(0))
            if len(self.price_max_entry.get()) != 0: self.price_max_entry.delete(0, len(self.price_max_entry.get()))
            self.price_max_entry.insert(0, maxprice)
            
            if len(self.available_min_entry.get()) != 0: self.available_min_entry.delete(0, len(self.available_min_entry.get()))
            self.available_min_entry.insert(0, int(0))
            if len(self.available_max_entry.get()) != 0: self.available_max_entry.delete(0, len(self.available_max_entry.get()))
            self.available_max_entry.insert(0, maxavailable)

        def cartreset():
            maxid = self.cursor.execute('SELECT Max(book_id) FROM books').fetchone()[0]
            if maxid != None:
                self.orderbooks = [0]* (maxid + 1)
            else: self.orderbooks = [0]
            self.qtytotal = 0
            self.subtotal = 0
            self.total_head.destroy()
            self.bookcatalogue.destroy()
            self.total_head = tkinter.Label(self.selectbook_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(self.subtotal)),
                                            font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.total_head.place(x=300, y=10)
            createbookslist(self.cursor.execute('SELECT * FROM books'))
            
            

        def backtoCatalogue():
            self.purchase_window_top.place_forget()
            self.purchase_window_bot.place_forget()
            self.bkcatalogue_summary.destroy()
            self.selectbook_window_mid.place(x = 0, y = 0)
            self.selectbook_window_bot.place(x = 0, y = 375)
            self.total_head_summary.place_forget()
            self.subandtax.place_forget()
            self.taxtotal.place_forget()
            self.bar.pack(side=tkinter.RIGHT, pady=120, ipady =158, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 125)
            createbookslist(self.cursor.execute('SELECT * FROM books'))
            filterreset()

        def is_invalid(n):
            try:
                int(n)
            except ValueError:
                return True
            else:
                if int(n) < 0:
                    return True
                else:
                    return False

        self.method = "None"
        self.payinfo = []

        def selectpayment():
            
            def gotopay():
                self.pay_method = tkinter.Label(self.purchase_window_bot, text=self.method, font=font_small, fg=fc_label, bg=bg_label)
                self.pay_method.place(x=135, y=210)
                print(self.savecheck.get())
                print(self.payinfo)
                self.method_window_main.place_forget()
                self.method_window_cash.place_forget()
                self.method_window_bank.place_forget()
                self.method_window_card.place_forget()
                self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =73, anchor = tkinter.N)
                self.canvas.pack(side=tkinter.TOP, pady = 35)

            def backtosum():
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_main.place_forget()
                self.method_window_cash.place_forget()
                self.method_window_bank.place_forget()
                self.method_window_card.place_forget()
                self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =73, anchor = tkinter.N)
                self.canvas.pack(side=tkinter.TOP, pady = 35)
                
            def card():
                def savecard():
                    if self.cardname_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Name on Card is empty"))
                    elif self.cardnumber_entry.get() == "" or is_invalid(self.cardnumber_entry.get()) or len(self.cardnumber_entry.get())!=16:
                        messagebox.showwarning(title = "ERROR", message = ("Card Number is empty or invalid input"))
                    elif self.cardcvc_entry.get() == "" or is_invalid(self.cardcvc_entry.get()) or len(self.cardcvc_entry.get())!=3:
                        messagebox.showwarning(title = "ERROR", message = ("Card CVC is empty or invalid input"))
                    elif self.cardexpmon_entry.get() == "" or is_invalid(self.cardexpmon_entry.get()) or len(self.cardexpmon_entry.get())!=2:
                        messagebox.showwarning(title = "ERROR", message = ("Card Exp Month is empty or invalid input"))
                    elif int(self.cardexpmon_entry.get()) > 12:
                        messagebox.showwarning(title = "ERROR", message = ("Card Exp Month is invalid input"))
                    elif self.cardexpyear_entry.get() == "" or is_invalid(self.cardexpyear_entry.get()) or len(self.cardexpyear_entry.get())!=2:
                        messagebox.showwarning(title = "ERROR", message = ("Card Exp Year is empty or invalid input"))
                    elif self.bill_street_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: Street is empty or invalid input"))
                    elif self.bill_city_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: City is empty or invalid input"))
                    elif self.bill_state_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: State is empty or invalid input"))
                    elif self.bill_country_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: Country is empty or invalid input"))
                    elif self.bill_zip_entry.get() == "" or is_invalid(self.bill_zip_entry.get()) or len(self.bill_zip_entry.get())<5:
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: Zip Code is empty or invalid input"))
                    elif self.cardphone_entry.get() == "" or is_invalid(self.bill_zip_entry.get()):
                        messagebox.showwarning(title = "ERROR", message = ("Phone number is empty or invalid input"))
                    else:
                        self.payinfo = [self.user_id, str(self.cardname_entry.get()), str(self.cardnumber_entry.get()),
                                        str(self.cardexpmon_entry.get()), str(self.cardexpyear_entry.get()), str(self.bill_street_entry.get()),
                                        str(self.bill_city_entry.get()), str(self.bill_state_entry.get()), str(self.bill_country_entry.get()),
                                        str(self.bill_zip_entry.get()), str(self.cardphone_entry.get())]
                        gotopay()
                    
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_cash.place_forget()
                self.method_window_bank.place_forget()
                self.method = "Credit/Debit Card"

                self.card_selectpay_head = tkinter.Label(self.method_window_card, text="Card Information", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.card_selectpay_head.place(x=350, y=5)

                self.cardinfo_head = tkinter.Label(self.method_window_card, text="Card Detail:", font=font_small_bold, fg=fc_label, bg=bg_label)
                self.cardname_label = tkinter.Label(self.method_window_card, text="Name on Card:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardname_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.cardnumber_label = tkinter.Label(self.method_window_card, text="Card Number:", font=font_small, fg=fc_label, bg=bg_label)
                self.nospace = tkinter.Label(self.method_window_card, text = "(no space)", font=font_small, fg=fc_label, bg=bg_label)
                self.cardnumber_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.cardexp_label = tkinter.Label(self.method_window_card, text="Expire MM/YY:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardexpmon_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=3)
                self.cardexpto_label = tkinter.Label(self.method_window_card, text="/", font=font_small, fg=fc_label, bg=bg_method)
                self.cardexpyear_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=3)
                self.cardcvc_label = tkinter.Label(self.method_window_card, text="CVC:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardcvc_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, show = "*", fg=fc_entry, bg=bg_entry, width=5)
                self.cardphone_label = tkinter.Label(self.method_window_card, text="Phone:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardphone_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)

                
                
                
                self.bill_head = tkinter.Label(self.method_window_card, text="Billing Address:", font=font_small_bold, fg=fc_label, bg=bg_label)
                self.bill_street_label = tkinter.Label(self.method_window_card, text="Street:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_street_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_city_label = tkinter.Label(self.method_window_card, text="City:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_city_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_state_label = tkinter.Label(self.method_window_card, text="State:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_state_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_country_label = tkinter.Label(self.method_window_card, text="Country:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_country_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_zip_label = tkinter.Label(self.method_window_card, text="Zipcode:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_zip_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.card_savemethod_button = tkinter.Checkbutton(self.method_window_card, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 1, offvalue = 0, font = font_small, bg = bg_method)
                self.card_savemethod_button.deselect()

                pmethod = self.cursor.execute('SELECT saved_payment FROM accounts WHERE user_id=?', [self.user_id,]).fetchone()[0]

                if pmethod == 1:
                    pinfo = self.cursor.execute('SELECT * FROM cards WHERE user_id=?', [self.user_id,]).fetchone()
                    self.cardname_entry.insert(0, pinfo[1])
                    self.cardnumber_entry.insert(0, pinfo[2])
                    self.cardexpmon_entry.insert(0, pinfo[3])
                    self.cardexpyear_entry.insert(0, pinfo[4])
                    self.bill_street_entry.insert(0, pinfo[5])
                    self.bill_city_entry.insert(0, pinfo[6])
                    self.bill_state_entry.insert(0, pinfo[7])
                    self.bill_country_entry.insert(0, pinfo[8])
                    self.bill_zip_entry.insert(0, pinfo[9])
                    self.cardphone_entry.insert(0, pinfo[10])
                    self.card_savemethod_button.select()
                    
                self.cardinfo_head.place(x=20, y=50)
                self.cardname_label.place(x=20, y=70)
                self.cardname_entry.place(x=113, y=71)
                self.cardnumber_label.place(x=20, y=90)
                self.cardnumber_entry.place(x=113, y=91)
                self.nospace.place(x=325, y=90)
                self.cardexp_label.place(x=20, y=110)
                self.cardexpmon_entry.place(x=113, y=111)
                self.cardexpto_label.place(x=138, y=110)
                self.cardexpyear_entry.place(x=148, y=111)
                self.cardcvc_label.place(x=20, y=130)
                self.cardcvc_entry.place(x=113, y=131)
                self.cardphone_label.place(x=20, y=150)
                self.cardphone_entry.place(x=113, y=151)
                
                self.bill_head.place(x=430, y=50)
                self.bill_street_label.place(x=430, y=70)
                self.bill_street_entry.place(x=485, y=71)
                self.bill_city_label.place(x=430, y=90)
                self.bill_city_entry.place(x=485, y=91)
                self.bill_state_label.place(x=430, y=110)
                self.bill_state_entry.place(x=485, y=111)
                self.bill_country_label.place(x=430, y=130)
                self.bill_country_entry.place(x=485, y=131)
                self.bill_zip_label.place(x=430, y=150)
                self.bill_zip_entry.place(x=485, y=151)

                
                
                self.card_savemethod_button.place(x=305, y=180)
                self.savecard_button = ttk.Button(self.method_window_card, command=savecard, text="Save Payment Method", style="TButton", width=30)
                self.savecard_button.place(x=316, y=220)
                self.card_backtosum_button = ttk.Button(self.method_window_card, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
                self.card_backtosum_button.place(x=316, y=250)
                
                self.method_window_card.place(x=0,y=130)

            def bank():
                
                def savebank():
                    if self.bankname_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Bank Name is empty"))
                    elif self.banktype.get() == "None":
                        messagebox.showwarning(title = "ERROR", message = ("Account Type is not selected"))
                    elif self.routing_entry.get() == "" or is_invalid(self.routing_entry.get()):
                        messagebox.showwarning(title = "ERROR", message = ("Routing Number is empty or invalid input"))
                    elif self.bankacc_entry.get() == "" or is_invalid(self.bankacc_entry.get()):
                        messagebox.showwarning(title = "ERROR", message = ("Account Number is empty or invalid input"))
                    else:
                        self.payinfo = [self.user_id, (self.bankname_entry.get()), str(self.banktype.get()),
                                        str(self.routing_entry.get()), str(self.bankacc_entry.get())]
                        gotopay()
                    
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_card.place_forget()
                self.method_window_cash.place_forget()
                self.method = "Bank Check"

                self.bank_selectpay_head = tkinter.Label(self.method_window_bank, text="Bank Information", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.bank_selectpay_head.place(x=350, y=5)

                self.bankinfo_head = tkinter.Label(self.method_window_bank, text="Bank Detail:", font=font_small_bold, fg=fc_label, bg=bg_label)
                self.bankname_label = tkinter.Label(self.method_window_bank, text="Bank Name:", font=font_small, fg=fc_label, bg=bg_label)
                self.bankname_entry = tkinter.Entry(self.method_window_bank, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.banktype = tkinter.StringVar(value="None")
                self.banktype_label = tkinter.Label(self.method_window_bank, text="Account Type:", font=font_small, fg=fc_label, bg=bg_label)
                self.banktype_entry = tkinter.OptionMenu(self.method_window_bank, self.banktype, "Checking", "Saving" )
                self.routing_label = tkinter.Label(self.method_window_bank, text="Routing Number:", font=font_small, fg=fc_label, bg=bg_label)
                self.routing_entry = tkinter.Entry(self.method_window_bank, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.bankacc_label = tkinter.Label(self.method_window_bank, text="Account Number:", font=font_small, fg=fc_label, bg=bg_label)
                self.bankacc_entry = tkinter.Entry(self.method_window_bank, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)

                self.bank_savemethod_button = tkinter.Checkbutton(self.method_window_bank, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 2, offvalue = 0, font = font_small, bg = bg_method)
                self.bank_savemethod_button.deselect()
                pmethod = self.cursor.execute('SELECT saved_payment FROM accounts WHERE user_id=?', [self.user_id,]).fetchone()[0]

                if pmethod == 2:
                    pinfo = self.cursor.execute('SELECT * FROM checks WHERE user_id=?', [self.user_id,]).fetchone()
                    self.bankname_entry.insert(0, pinfo[1])
                    self.banktype = tkinter.StringVar(value=pinfo[2])
                    self.banktype_entry = tkinter.OptionMenu(self.method_window_bank, self.banktype, "Checking", "Saving" )
                    self.routing_entry.insert(0, pinfo[3])
                    self.bankacc_entry.insert(0, pinfo[4])
                    self.bank_savemethod_button.select()


                self.banktype_entry.config(font = font_small)
                self.bankinfo_head.place(x=20, y=50)
                self.bankname_label.place(x=20, y=70)
                self.bankname_entry.place(x=125, y=71)
                self.banktype_label.place(x=20, y=97)
                self.banktype_entry.place(x=125, y=93)
                self.routing_label.place(x=20, y=125)
                self.routing_entry.place(x=125, y=126)
                self.bankacc_label.place(x=20, y=150)
                self.bankacc_entry.place(x=125, y=151)

                
                
                self.bank_savemethod_button.place(x=305, y=180)
                self.savebank_button = ttk.Button(self.method_window_bank, command=savebank, text="Save Payment Method", style="TButton", width=30)
                self.savebank_button.place(x=316, y=220)
                self.bank_backtosum_button = ttk.Button(self.method_window_bank, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
                self.bank_backtosum_button.place(x=316, y=250)
                
                self.method_window_bank.place(x=0,y=130)

            def cash():
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_card.place_forget()
                self.method_window_bank.place_forget()
                self.method_window_cash.place(x=0,y=130)
                self.method = "Cash (on Delivery)"

                self.cash_head = tkinter.Label(self.method_window_cash, text="You must pay when you receive the box.", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.cash_head.place(x=230, y=10)

                self.cash_savemethod_button = tkinter.Checkbutton(self.method_window_cash, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 3, offvalue = 0, font = font_small, bg = bg_method)
                self.cash_savemethod_button.deselect()

                pmethod = self.cursor.execute('SELECT saved_payment FROM accounts WHERE user_id=?', [self.user_id,]).fetchone()[0]

                if pmethod == 3:
                    self.cash_savemethod_button.select()
                    
                self.cash_savemethod_button.place(x=305, y=40)
                self.savecash_button = ttk.Button(self.method_window_cash, command=gotopay, text="Save Payment Method", style="TButton", width=30)
                self.savecash_button.place(x=316, y=80)
                self.cash_backtosum_button = ttk.Button(self.method_window_cash, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
                self.cash_backtosum_button.place(x=316, y=110)
                
            self.canvas.pack_forget()
            self.bar.pack_forget()
            self.method_window_main.place(x=0,y=0)
            self.selectpay_head = tkinter.Label(self.method_window_main, text="Select Payment Method", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.selectpay_head.place(x=310, y=0)
            self.credit_button = ttk.Button(self.method_window_main, command=card, text="Credit/Debit Card", style="TButton", width=30)
            self.credit_button.place(x=316, y=40)
            self.bank_button = ttk.Button(self.method_window_main, command=bank, text="Bank Check", style="TButton", width=30)
            self.bank_button.place(x=316, y=70)
            self.cash_button = ttk.Button(self.method_window_main, command=cash, text="Cash on Delivary", style="TButton", width=30)
            self.cash_button.place(x=316, y=100)
            self.backtosum_button = ttk.Button(self.method_window_main, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
            self.backtosum_button.place(x=316, y=130)
            self.savecheck = tkinter.IntVar(value = 0)
            

        def checkout():
            if self.ship_name_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Full Name is empty"))
            elif self.ship_street_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: Street is empty or invalid input"))
            elif self.ship_city_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: City is empty or invalid input"))
            elif self.ship_state_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: State is empty or invalid input"))
            elif self.ship_country_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: Country is empty or invalid input"))
            elif self.ship_zip_entry.get() == "" or is_invalid(self.ship_zip_entry.get()) or len(self.ship_zip_entry.get())<5:
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: Zip Code is empty or invalid input"))
            elif self.payinfo == [] and self.method != "Cash (on Delivery)":
                messagebox.showwarning(title = "ERROR", message = ("Payment Method is not selected"))
            else:
                maxorderid = len(self.cursor.execute('SELECT * FROM orders').fetchall())
                
                f = open("orderconfirmation_" + self.user_id + "_" + str(maxorderid) +".txt", "w")
                f.write("Order Confirmation\n==================================================================="
                        +"\nOrdered Books:\n===================================================================")
                for i in range(0, len(self.ordersummary)):
                    book = self.cursor.execute('SELECT * FROM books WHERE book_id =?', [self.ordersummary[i][0],]).fetchone()
                    f.write("\nTitle: " + str(book[1]) + "\nAuthor: " + str(book[2]) + "\nPublisher: " + str(book[3]) + "\nPrice: " + str(book[4]) + "\nQty: " + str(self.ordersummary[i][1]))
                    f.write("\n===================================================================")
                    self.cursor.execute('UPDATE books SET available=?, sold=? WHERE book_id=?', [(int(book[5]) - self.ordersummary[i][1]), (int(book[6]) + self.ordersummary[i][1]), self.ordersummary[i][0]])
                    
                f.write("\nCustomer Information:\n===================================================================")
                f.write("\nFull Name: " + str(self.ship_name_entry.get()) +
                        "\nShipping Address:" +
                        "\n Street: " + str(self.ship_street_entry.get()) +
                        "\n City: " + str(self.ship_city_entry.get()) +
                        "\n State: " + str(self.ship_state_entry.get()) +
                        "\n Country: " + str(self.ship_country_entry.get()) +
                        "\n Zip: " + str(self.ship_zip_entry.get()))
                f.write("\n===================================================================")
                f.write("\nPayment Information:\n===================================================================")
                f.write("\nPayment Method: " + str(self.method))
                if self.method == "Credit/Debit Card":
                    f.write("\nName on Card: " + str(self.payinfo[1]) +
                            "\nCard Number: " + str(self.payinfo[2]) +
                            "\nCard Exp: " + str(self.payinfo[3]) + "/" + str(self.payinfo[4]) +
                            "\nBilling Address:" +
                            "\n Street: " + str(self.payinfo[5]) +
                            "\n City: " + str(self.payinfo[6]) +
                            "\n State: " + str(self.payinfo[7]) +
                            "\n Country: " + str(self.payinfo[8]) +
                            "\n Zip: " + str(self.payinfo[9]) +
                            "\n Phone: " + str(self.payinfo[10]))
                    self.cursor.execute('SELECT * FROM cards WHERE user_id=?', [self.user_id,])
                    exist = len(self.cursor.fetchall())
                    if exist == 0:
                        if self.savecheck.get() == 1:
                            self.cursor.execute('INSERT into cards values (?,?,?,?,?,?,?,?,?,?,?)', self.payinfo)
                            db.commit()
                    else:
                        if self.savecheck.get() == 1:
                            pinfoforupdate = self.payinfo[1:11]+[self.payinfo[0]]
                            self.cursor.execute('UPDATE cards SET name=?, cardnumber=?, exp_month=?, exp_year=?,\
                                                                  bill_street=?, bill_city=?, bill_state=?, bill_country=?,\
                                                                  bill_zip=?, bill_phone=?\
                                WHERE user_id=?', pinfoforupdate)
                            db.commit()
                        else:
                            self.cursor.execute('DELETE cards WHERE user_id=?', self.user_id)
                            db.commit()
                            
                elif self.method == "Bank Check":
                    f.write("\nName: " + str(self.payinfo[1]) +
                            "\nBank Type: " + str(self.payinfo[2]) +
                            "\nRouting Number: " + str(self.payinfo[3]) +
                            "\nAccount Number: " + str(self.payinfo[4]))
                    self.cursor.execute('SELECT * FROM checks WHERE user_id=?', [self.user_id,])
                    exist = len(self.cursor.fetchall())
                    if exist == 0:
                        if self.savecheck.get() == 2:
                            self.cursor.execute('INSERT into checks values (?,?,?,?,?)', self.payinfo)
                            db.commit()
                    else:
                        if self.savecheck.get() == 2:
                            pinfoforupdate = self.payinfo[1:5]+[self.payinfo[0]]
                            self.cursor.execute('UPDATE checks SET name=?, acctype=?, routing=?, bankacc=? WHERE user_id=?', pinfoforupdate)
                            db.commit()
                        else:
                            self.cursor.execute('DELETE checks WHERE user_id=?', self.user_id)
                            db.commit()
                else:
                    f.write("\nYou must pay when you receive the box.")

                self.cursor.execute('UPDATE accounts SET saved_payment=? WHERE user_id=?', [self.savecheck.get(), self.user_id])
                db.commit()
                

                orderqty = ""
                for x in range(0, len(self.orderbooks)):
                    if x == len(self.orderbooks)-1:
                        orderqty = orderqty + str(self.orderbooks[x])
                    else:
                        orderqty = orderqty + str(self.orderbooks[x])+":"
                    
                total = (round(self.subtotal, 2)+round(self.subtotal * 0.0625))
                
                shipadd =  (str(self.ship_name_entry.get()) + ":" + str(self.ship_street_entry.get()) + ":" + 
                           str(self.ship_city_entry.get()) + ":" + str(self.ship_state_entry.get()) + ":" + 
                           str(self.ship_country_entry.get()) + ":" + str(self.ship_zip_entry.get()))
                paymet = self.method
                for y in range(0, len(self.payinfo)):
                    paymet = paymet + ":" + str(self.payinfo[y])
                
                row = [str(maxorderid), self.user_id, orderqty, total, shipadd, paymet]
                
                self.cursor.execute('INSERT into orders values (?,?,?,?,?,?)', row)
                db.commit()
                    
                f.close()
                messagebox.showinfo(title="Thank You", message="You Purchase has been Completed!\nOrder Confirmation is saved as txt file on your file.\nThank You!")

                self.cursor.close()
                self.selectbook_window.destroy()
                storemainGUI(self.user_id)
            

        def viewsummary():
            self.bookcatalogue.destroy()
            self.selectbook_window_mid.place_forget()
            self.selectbook_window_bot.place_forget()
            self.canvas.config(height = 180)
            
            self.summary_head = tkinter.Label(self.purchase_window_top, text="Order Summary", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.summary_head.place(x=340, y=0)
            self.bkcatalogue_summary = tkinter.Frame(self.canvas,height = 180, width = multiframe_w, bg = bg_label)
            self.canvas.create_window((0,0), window=self.bkcatalogue_summary, anchor=tkinter.NW, width=self.canvas.cget('width'))

            title_head = tkinter.Label(self.bkcatalogue_summary, text= "Title", font=font_small, fg=fc_label, bg=bg_label)
            title_head.grid(row = 0, column = 1)
            author_head = tkinter.Label(self.bkcatalogue_summary, text= "Author", font=font_small, fg=fc_label, bg=bg_label)
            author_head.grid(row = 0, column = 2)
            publisher_head = tkinter.Label(self.bkcatalogue_summary, text= "Publisher", font=font_small, fg=fc_label, bg=bg_label)
            publisher_head.grid(row = 0, column = 3)
            price_head = tkinter.Label(self.bkcatalogue_summary, text= "Price", font=font_small, fg=fc_label, bg=bg_label)
            price_head.grid(row = 0, column = 4)
            qty_head = tkinter.Label(self.bkcatalogue_summary, text= "Qty", font=font_small, fg=fc_label, bg=bg_label)
            qty_head.grid(row = 0, column = 5)
            self.ordersummary = []
            
            for i in range(0, len(self.orderbooks)):
                bid = int(self.orderbooks[i])
                if bid != 0:
                    self.ordersummary.append([i, bid])
                    book = self.cursor.execute('SELECT * FROM books WHERE book_id =?', [i,]).fetchone()
                    title = tkinter.Label(self.bkcatalogue_summary, text= str(book[1]), font=font_small, fg=fc_label, bg=bg_label)
                    author = tkinter.Label(self.bkcatalogue_summary, text= str(book[2]), font=font_small, fg=fc_label, bg=bg_label)
                    publisher = tkinter.Label(self.bkcatalogue_summary, text= str(book[3]), font=font_small, fg=fc_label, bg=bg_label)
                    price = tkinter.Label(self.bkcatalogue_summary, text= ("$" + str(book[4])), font=font_small, fg=fc_label, bg=bg_label)
                    qty = tkinter.Label(self.bkcatalogue_summary, text= str(self.orderbooks[i]), font=font_small, fg=fc_label, bg=bg_label)
                    title.grid(row = len(self.ordersummary) + 1, column = 1, sticky = tkinter.W)
                    author.grid(row = len(self.ordersummary) + 1, column = 2, sticky = tkinter.W)
                    publisher.grid(row = len(self.ordersummary) + 1, column = 3, sticky = tkinter.W)
                    price.grid(row = len(self.ordersummary) + 1, column = 4, sticky = tkinter.W)
                    qty.grid(row = len(self.ordersummary) + 1, column = 5)
            self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =73, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 35)

            self.total_head_summary = tkinter.Label(self.purchase_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(round(self.subtotal, 2))),
                                            font=font_normal, fg=fc_label, bg=bg_label)
            self.total_head_summary.place(x=300, y=10)
            self.backtocatalogue_button = ttk.Button(self.purchase_window_bot, command=backtoCatalogue, text="Back to Catalogue", style="TButton", width=20)
            self.backtocatalogue_button.place(x=650, y=4)

            self.ship_head = tkinter.Label(self.purchase_window_bot, text="Shipping Address:", font=font_small_bold, fg=fc_label, bg=bg_label)
            self.ship_name_label = tkinter.Label(self.purchase_window_bot, text="Full Name:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_name_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_street_label = tkinter.Label(self.purchase_window_bot, text="Street:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_street_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_city_label = tkinter.Label(self.purchase_window_bot, text="City:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_city_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_state_label = tkinter.Label(self.purchase_window_bot, text="State:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_state_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_country_label = tkinter.Label(self.purchase_window_bot, text="Country:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_country_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_zip_label = tkinter.Label(self.purchase_window_bot, text="Zipcode:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_zip_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_head.place(x=20, y=70)
            self.ship_name_label.place(x=20, y=50)
            self.ship_name_entry.place(x=86, y=51)
            self.ship_street_label.place(x=20, y=90)
            self.ship_street_entry.place(x=75, y=91)
            self.ship_city_label.place(x=20, y=110)
            self.ship_city_entry.place(x=75, y=111)
            self.ship_state_label.place(x=20, y=130)
            self.ship_state_entry.place(x=75, y=131)
            self.ship_country_label.place(x=20, y=150)
            self.ship_country_entry.place(x=75, y=151)
            self.ship_zip_label.place(x=20, y=170)
            self.ship_zip_entry.place(x=75, y=171)

            self.subandtax = tkinter.Label(self.purchase_window_bot, text=("Subtotal: $" + str(round(self.subtotal, 2)) +
                                                                           "\nTax: $" + str(round(self.subtotal * 0.0625))), font=font_normal, fg=fc_label, bg=bg_label)
            self.taxtotal = tkinter.Label(self.purchase_window_bot, text=("    Total: $" + str(round(self.subtotal, 2)+round(self.subtotal * 0.0625))), font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.subandtax.place(x=500, y=70)
            self.taxtotal.place(x=500, y=130)

            self.pay_head = tkinter.Label(self.purchase_window_bot, text="Payment Method:", font=font_small_bold, fg=fc_label, bg=bg_label)
            self.pay_head.place(x=20, y=210)
            self.pay_method = tkinter.Label(self.purchase_window_bot, text=self.method, font=font_small, fg=fc_label, bg=bg_label)
            self.pay_method.place(x=135, y=210)
            self.pay_select_button = ttk.Button(self.purchase_window_bot, command=selectpayment, text="Select Payment Method", style="TButton", width=20)
            self.pay_select_button.place(x=40, y=235)

            self.confirm_button = ttk.Button(self.purchase_window_bot, command=checkout, text="Place Your Order", style="font_normal.TButton", width=20)
            self.confirm_button.place(x=500, y=200)
            self.pur_cancel_button = ttk.Button(self.purchase_window_bot, command=cancel, text="Cancel", style="TButton", width=15)
            self.pur_cancel_button.place(x=555, y=240)

            self.payinfo = []           
            
            self.purchase_window_top.place(x=0,y=0)
            self.purchase_window_bot.place(x=0,y=215)
            
            

        self.filterbooks_button = ttk.Button(self.selectbook_window_mid, command=filterbooks, text="Filter the Book Catalogue", style="TButton", width=30)
        self.filterbooks_button.place(x=300.5, y=50)
        self.filterreset_button = ttk.Button(self.selectbook_window_mid, command=filterreset, text="Filter Reset", style="TButton", width=15)
        self.filterreset_button.place(x=528, y=25)
        self.bookcatalogue_label = tkinter.Label(self.selectbook_window_mid, text="Book Catalogue", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.bookcatalogue_label.place(x=340, y=90)
        self.title_label = tkinter.Label(self.selectbook_window_mid, text="Title=", font=font_small, fg=fc_label, bg=bg_label)
        self.title_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
        self.author_label = tkinter.Label(self.selectbook_window_mid, text="Author=", font=font_small, fg=fc_label, bg=bg_label)
        self.author_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
        self.publisher_label = tkinter.Label(self.selectbook_window_mid, text="Publisher=", font=font_small, fg=fc_label, bg=bg_label)
        self.publisher_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
        self.price_label = tkinter.Label(self.selectbook_window_mid, text="Price=", font=font_small, fg=fc_label, bg=bg_label)
        self.price_to = tkinter.Label(self.selectbook_window_mid, text="=<=", font=font_small, fg=fc_label, bg=bg_label)
        self.price_min_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)
        self.price_max_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)
        self.available_label = tkinter.Label(self.selectbook_window_mid, text="Available=", font=font_small, fg=fc_label, bg=bg_label)
        self.available_to = tkinter.Label(self.selectbook_window_mid, text="=<=", font=font_small, fg=fc_label, bg=bg_label)
        self.available_min_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)
        self.available_max_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)

        #�ꕶ�� = x=7, y=22 �i�����悻�jentry 219;1=7.3
        self.title_label.place(x=5, y=0)
        self.title_entry.place(x=41, y=0)
        self.author_label.place(x=260, y=0)
        self.author_entry.place(x=309, y=0)
        self.publisher_label.place(x=528, y=0)
        self.publisher_entry.place(x=593, y=0)
        self.price_label.place(x=5, y=25)
        self.price_to.place(x=120, y=25)
        self.price_min_entry.insert(0, int(0))
        self.price_min_entry.place(x=46, y=25)
        self.price_max_entry.insert(0, maxprice)
        self.price_max_entry.place(x=149, y=25)
        self.available_label.place(x=260, y=25)
        self.available_min_entry.insert(0, 0)
        self.available_min_entry.place(x=322, y=25)
        self.available_to.place(x=396, y=25)
        self.available_max_entry.insert(0, maxavailable)
        self.available_max_entry.place(x=425, y=25)

        self.total_head = tkinter.Label(self.selectbook_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(self.subtotal)), font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.total_head.place(x=270, y=10)
        self.vieworder_button = ttk.Button(self.selectbook_window_bot, command=viewsummary, text="Proceed to Checkout", style="font_normal.TButton", width=20)
        self.vieworder_button.place(x=310, y=45)
        self.cartreset_button = ttk.Button(self.selectbook_window_bot, command=cartreset, text="Reset Cart", style="TButton", width=20)
        self.cartreset_button.place(x=650, y=4)
        self.sel_cancel_button = ttk.Button(self.selectbook_window_bot, command=cancel, text="Cancel", style="TButton", width=15)
        self.sel_cancel_button.place(x=365, y=90)

        self.selectbook_window_mid.place(x = 0, y = 0)
        self.selectbook_window_bot.place(x = 0, y = 375)

        #style - appearance of a widget class.
        #the style name of a ttk widget starts with the letter 'T' followed by the widget name - eg, TLabel and TButton
        self.style = ttk.Style()
        self.style.configure("TButton", font=font_small, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
        self.style.configure("font_normal.TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)

        self.selectbook_window.mainloop()

#UserInfoGUI: set the userinfo window's appearance and actions
class UserInfoGUI():
    def __init__(self, user_id):
        self.cursor = db.cursor()
        self.user_id = user_id

    #Set the appearance
        self.userinfo_window = tkinter.Tk()
        #Title of the application
        self.userinfo_window.title("Update User Info")
        #Geometry string is a standard way of describing the size and location of the window
        # Set the size of the window (x and  y position of the root window)
        self.userinfo_window.geometry(normal_geo)
        self.userinfo_window.config(bg=bg_normal) #Background color

    #Set the actions
        def edituserinfo():
            row = [self.pass_entry.get(), self.fname_entry.get(), self.lname_entry.get(), self.email_entry.get(), self.user_id]
            self.cursor.execute('UPDATE accounts SET password=?, fname=?, lname=?, email=? WHERE user_id=?', row)
            db.commit()
            messagebox.showinfo(title="Save", message= ("Account infomation is updated!----- \nUser ID: "+ str(self.user_id)
                                                           + "\nPassword: " + str(self.pass_entry.get())
                                                           + "\nFirstname: " + str(self.fname_entry.get())
                                                           + "\nLastname: " + str(self.lname_entry.get())
                                                           + "\nEmail: " + str(self.email_entry.get())))
            self.cursor.close()
            self.userinfo_window.destroy()
            storemainGUI(self.user_id)
            
        def cancel():
            self.cursor.close()
            self.userinfo_window.destroy()
            storemainGUI(self.user_id)

    #Set the detail appearance    
        self.userinfo_head = tkinter.Label(self.userinfo_window, text="User Info Update", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a label for Password
        self.pass_label = tkinter.Label(self.userinfo_window, text="Password:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for Password
        self.pass_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating a label for First Name
        self.fname_label = tkinter.Label(self.userinfo_window, text="First Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for First Name
        self.fname_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating a label for Last Name
        self.lname_label = tkinter.Label(self.userinfo_window, text="Last Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for Last Name
        self.lname_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating a label for Email
        self.email_label = tkinter.Label(self.userinfo_window, text="Email:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for Email
        self.email_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating buttons
        self.save_button = ttk.Button(self.userinfo_window, command = edituserinfo, text = "Update Information", style="TButton", width=20)
        self.cancel_button = ttk.Button(self.userinfo_window, command=cancel, text="Cancel", style="TButton", width=20)

        self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [self.user_id,])

        # Position the buttons
        self.userdata = self.cursor.fetchone()
                    
        self.pass_entry.insert(0, self.userdata[1])
        self.fname_entry.insert(0, self.userdata[2])
        self.lname_entry.insert(0, self.userdata[3])
        self.email_entry.insert(0, self.userdata[4])

        self.userinfo_head.place(x=180, y=10)
        
        self.pass_label.place(x=5, y=60)
        self.fname_label.place(x=5, y=90)
        self.lname_label.place(x=5, y=120)
        self.email_label.place(x=5, y=150)
            
        self.pass_entry.place(x=200, y=60)
        self.fname_entry.place(x=200, y=90)
        self.lname_entry.place(x=200, y=120)
        self.email_entry.place(x=200, y=150)

        self.save_button.place(x=150, y=190)
        self.cancel_button.place(x=150, y=225)

        self.style = ttk.Style()
        self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
        
        #Loop the window
        self.userinfo_window.mainloop()