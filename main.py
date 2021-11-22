#!/usr/bin/env python
# coding: utf-8

# In[3]:


import re
from datetime import datetime
printerAddress_expo = ''
printerAddress_kitchen = ''
printerPort = 9100
from escposprinter import *
from escposprinter.escpos import EscposIO, Escpos
import mysql.connector
import time


# In[ ]:


def checkPrinterAlive(printerAddress,printerPort):
        if (printer.Network.isAlive(printerAddress, printerPort)):
            return True
        else:
            return True
            #raise Exception ("Host is unreachable, socket communication was not opened")
def generate_kitchenview(order_in):
    if (checkPrinterAlive(printerAddress_kitchen,printerPort)):
        string = str("String: " + str(datetime.now().microsecond))
        for iteration in range(1):
            with EscposIO(printer.Network(printerAddress_kitchen, printerPort)) as p:
                p.set(font='b', codepage='cp1251', size='2x', align='center', bold=False,color=2)
                p.writelines('')
                p.writelines(f"Order Id: {order_in[0]}")
                d = datetime.strptime(str(order_in[15]), "%H:%M:%S")
                p.writelines(f"Pickup Time: {d.strftime('%I:%M %p')}")
                p.writelines('')
                order_splited = order_in[8].replace(':',"").split('O27')[1:]
                for x in order_splited:
                    quantity = int(x.split('"qty";')[1].split(";")[0].split('"')[1::2][0])
                    print_que = 0
                    while print_que < quantity:
                        print_que = print_que + 1
                    #Print Order
                        p.set(font='b', codepage='cp1251', size='2x', align='left', bold=False,color=2)
                        Item_message = x.split('"name"')[1].split(";")[1]
                        item_message_final = Item_message.split('"')[1::2][0]
                        p.writelines(f'{item_message_final}')
                        p.writelines('')
                        Price_message = x.split('"price";d')[1].split(";")[0]
                        Comment_message = x.split(';s7"comment"')[1].split(";")[1]
                        if re.findall('CartItemOptionValue',x) != []:
                            j = 1
                            while j <= len(re.findall('CartItemOptionValues',x)):
                                mods_message = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"name"')[1]
                                mods_quantity = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"qty"')[1]
                                message_quantity = int(mods_quantity.split(";")[1][1::2][0])
                                message_finals = mods_message.split('"')[1::2][0]
                                mod_print = 0
                                while mod_print < message_quantity :
                                    p.set(font='a', codepage='cp1251', size='2h', align='left', bold=False,color=2)
                                    p.writelines(f'   Mods: {message_finals}')
                                j = j+1

                        p.set(font='a', codepage='cp1251', size='2h', align='right', bold=True,color=1)
                        if Comment_message != 'N' and Comment_message != 's0""':
                            comment_message_final = Comment_message.split('"')[1::2][0]
                            p.writelines(f'  {comment_message_final}')
                        p.writelines(' ')
                        
def generate_expoview(order_in):                
    if (checkPrinterAlive(printerAddress_expo,printerPort)):
        string = str("String: " + str(datetime.now().microsecond))
        for iteration in range(1):
            with EscposIO(printer.Network(printerAddress_expo, printerPort)) as p:
                p.set(font='b', codepage='cp1251', size='normal', align='center', bold=False,color=2)
                p.writelines(f"Order Id: {order_in[0]}")
                p.writelines('')
                p.writelines(f"Order Name:  {order_in[2]} {order_in[3]}")
                p.writelines('')
                p.writelines(f"Phone Number:  {order_in[5]}")
                p.writelines('')
                p.writelines(f"Total Items: {order_in[9]}")
                p.writelines('')
                p.writelines(f"Order Comments: {order_in[10]}")
                p.writelines('')
                d = datetime.strptime(str(order_in[15]), "%H:%M:%S")
                p.writelines('')
                p.writelines(f"Pickup Time: {d.strftime('%I:%M %p')}")
                p.writelines('')
                p.writelines(f"Order Total: ${order_in[17]}")
                p.writelines('')
                order_splited = order_in[8].replace(':',"").split('O27')[1:]
                for x in order_splited:
                    quantity = int(x.split('"qty";')[1].split(";")[0].split('"')[1::2][0])
                    print_que = 0
                    while print_que < quantity:
                        print_que = print_que + 1
                    #Print Order
                        p.set(font='b', codepage='cp1251', size='2x', align='left', bold=False,color=2)
                        Item_message = x.split('"name"')[1].split(";")[1]
                        item_message_final = Item_message.split('"')[1::2][0]
                        p.writelines(f'{item_message_final}')
                        p.writelines('')
                        Price_message = x.split('"price";d')[1].split(";")[0]
                        Comment_message = x.split(';s7"comment"')[1].split(";")[1]
                        if re.findall('CartItemOptionValue',x) != []:
                            j = 1
                            while j <= len(re.findall('CartItemOptionValues',x)):
                                mods_message = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"name"')[1]
                                mods_quantity = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"qty"')[1]
                                message_quantity = int(mods_quantity.split(";")[1][1::2][0])
                                message_finals = mods_message.split('"')[1::2][0]
                                mod_print = 0
                                while mod_print < message_quantity :
                                    p.set(font='a', codepage='cp1251', size='2h', align='left', bold=False,color=2)
                                    p.writelines(f'   Mods: {message_finals}')
                                j = j+1

                                
                        p.set(font='a', codepage='cp1251', size='2h', align='right', bold=True,color=1)
                        if Comment_message != 'N' and Comment_message != 's0""':
                            comment_message_final = Comment_message.split('"')[1::2][0]
                            p.writelines(f'  {comment_message_final}')
                    
                        p.writelines('')




# In[80]:


#local Print statements
def generate_kitchenview_local(order_in):
    string = str("String: " + str(datetime.now().microsecond))
    print(f"Order Id: {order_in[0]}")
    d = datetime.strptime(str(order_in[15]), "%H:%M:%S")
    print(f"Pickup Time: {d.strftime('%I:%M %p')}")
    order_splited = order_in[8].replace(':',"").split('O27')[1:]
    for x in order_splited:
        quantity = int(x.split('"qty";')[1].split(";")[0].split('"')[1::2][0])
        print_que = 0
        while print_que < quantity:
            print_que = print_que + 1
        #Print Order
            Item_message = x.split('"name"')[1].split(";")[1]
            item_message_final = Item_message.split('"')[1::2][0]
            print(f'{item_message_final}')
            Price_message = x.split('"price";d')[1].split(";")[0]
            Comment_message = x.split(';s7"comment"')[1].split(";")[1]
            if re.findall('CartItemOptionValue',x) != []:
                j = 1
                while j <= len(re.findall('CartItemOptionValues',x)):
                    mods_message = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"name"')[1]
                    mods_quantity = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"qty"')[1]
                    message_quantity = int(mods_quantity.split(";")[1][1::2][0])
                    message_finals = mods_message.split('"')[1::2][0]
                    mod_print = 0
                    while mod_print < message_quantity :
                        print(f'   Mods: {message_finals}')
                        mod_print = mod_print + 1
                    j = j+1

            if Comment_message != 'N' and Comment_message != 's0""':
                comment_message_final = Comment_message.split('"')[1::2][0]
                print(f'  {comment_message_final}')
                    
def generate_expoview_local(order_in):                
    string = str("String: " + str(datetime.now().microsecond))
    print(f"Order Id: {order_in[0]}")
    print(f"Order Name:  {order_in[2]} {order_in[3]}")
    print(f"Phone Number:  {order_in[5]}")
    print(f"Total Items: {order_in[9]}")
    print(f"Order Comments: {order_in[10]}")
    d = datetime.strptime(str(order_in[15]), "%H:%M:%S")
    print(f"Pickup Time: {d.strftime('%I:%M %p')}")
    print(f"Order Total: ${order_in[17]}")
    order_splited = order_in[8].replace(':',"").split('O27')[1:]
    for x in order_splited:
        quantity = int(x.split('"qty";')[1].split(";")[0].split('"')[1::2][0])
        print_que = 0
        while print_que < quantity:
            print_que = print_que + 1
        #Print Order
            Item_message = x.split('"name"')[1].split(";")[1]
            item_message_final = Item_message.split('"')[1::2][0]
            print(f'{item_message_final}')
            Price_message = x.split('"price";d')[1].split(";")[0]
            Comment_message = x.split(';s7"comment"')[1].split(";")[1]
            if re.findall('CartItemOptionValue',x) != []:
                j = 1
                while j <= len(re.findall('CartItemOptionValues',x)):
                    mods_message = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"name"')[1]
                    message_finals = mods_message.split('"')[1::2][0]
                    mods_quantity = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"qty"')[1]
                    message_quantity = int(mods_quantity.split(";")[1][1::2][0])
                    mod_print = 0
                    while mod_print < message_quantity :
                        print(f'   Mods: {message_finals}')
                        mod_print = mod_print + 1
                    j = j+1
                    
            if Comment_message != 'N' and Comment_message != 's0""':
                comment_message_final = Comment_message.split('"')[1::2][0]
                print(f'  {comment_message_final}')
            #print(f'   Price: $  {Price_message}')




# In[81]:


mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""  
)



# In[82]:

#run repetively and print on network printers every 15 seconds.
while True:
    try:
       mycursor = mydb.cursor()
       mycursor.execute("SELECT * FROM ti_orders WHERE status_id = 1")
       now = datetime.now()
       current_time = now.strftime("%H:%M:%S")
       print("Orders Last Checked at: ", current_time, end="\r")
       myresult = mycursor.fetchall()
       for x in myresult:
           sql= f"UPDATE ti_orders SET status_id = '3' WHERE order_id = {x[0]}"
           generate_expoview(x)
           generate_kitchenview(x)
           mycursor.execute(sql)
           mydb.commit()
       time.sleep(15)
    except:
       pass

