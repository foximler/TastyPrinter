printerAddress_expo = ''
printerAddress_kitchen = ''
printerPort = 9100
from escposprinter import *
from escposprinter.escpos import EscposIO, Escpos
from datetime import datetime
import time
api_key=""
base_url=""
class orders: 
    def __init__(self, order_id, order_status, order_printed, order_name,order_email,order_number,
                 order_total_items,order_comments,pickup_time,
                 order_total,order_items, order_type, order_city, order_address, order_state): 
        self.order_id = order_id 
        self.order_status = order_status
        self.order_printed = order_printed
        self.order_email = order_email
        self.order_name = order_name
        self.order_number = order_number
        self.order_total_items = order_total_items
        self.order_comments = order_comments
        self.order_pickup_time = pickup_time
        self.order_total = order_total
        self.order_items = order_items
        self.order_type = order_type
        self.order_address = order_address
        self.order_city = order_city
        self.order_state = order_state

import requests
import json

def get_active_orders():
    url = f'{base_url}active_orders'
    myobj = {'api_key': api_key}

    data = requests.post(url, data = myobj)
    items = []
    for y in data.json():
        x = json.loads(y)
        items.append(orders(x["order_id"],x["order_status"],x["order_printed"],x["order_email"],x["order_name"],x["order_number"],x["order_total_items"],x["order_comments"],x["order_pickup_time"],x["order_total"],x["order_items"],x["order_type"],x['order_city'],x['order_address'], x['order_state']))
    return items
def checkPrinterAlive(printerAddress,printerPort):
        if (printer.Network.isAlive(printerAddress, printerPort)):
            return True
        else:
            return True
            raise Exception ("Host is unreachable, socket communication was not opened")
def generate_kitchenview(order_in):
    if (checkPrinterAlive(printerAddress_kitchen,printerPort)):
        with EscposIO(printer.Network(printerAddress_kitchen, printerPort)) as p:
            p.set(font='b', codepage='cp1251', size='2x', align='center', bold=1)
            p.writelines('')
            p.writelines(f"Order Id: {order_in.order_id}")
            p.writelines(f"Pickup Time: {order_in.order_pickup_time}")
            p.writelines(f"Order Comments: {order_in.order_comments}")
            p.writelines('')
            for x in order_in.order_items:
                p.set(font='b', codepage='cp1251', size='2x', align='left', bold=1)
                p.writelines(x["Item_name"])
                for mod in x["Item_mods"]:
                    p.set(font='a', codepage='cp1251', size='2h', align='left', bold=1)
                    p.writelines(f'   Mods: {mod}')
                p.set(font='a', codepage='cp1251', size='2h', align='right', bold=1)
                p.writelines(x["Item_comments"])
                p.writelines(' ')

def generate_expoview(order_in):                
    if (checkPrinterAlive(printerAddress_expo,printerPort)):
        with EscposIO(printer.Network(printerAddress_expo, printerPort)) as p:
            p.set(font='b', codepage='cp1251', size='2x', align='left', bold=1)
            p.writelines(x["order_type"])
            p.set(font='b', codepage='cp1251', size='normal', align='center', bold=1)
            p.writelines(f"Order Id: {order_in.order_id}")
            p.writelines('')
            p.writelines(f"Order Name:  {order_in.order_name}")
            p.writelines('')
            if(order_in.type == "delivery"):
                p.writelines('')
                p.writelines(f"Order Address:  {order_in.order_address}")
                p.writelines(f"{order_in.order_city}")
                p.writelines('')
            p.writelines(f"Phone Number:  {order_in.order_number}")
            p.writelines('')
            p.writelines(f"Total Items: {order_in.order_total_items}")
            p.writelines('')
            p.writelines(f"Order Comments: {order_in.order_comments}")
            p.writelines('')
            p.writelines('')
            p.writelines(f"Pickup Time: {order_in.order_pickup_time}")
            p.writelines('')
            p.writelines(f"Order Total: ${order_in.order_total}")
            p.writelines('')
            for x in order_in.order_items:
                p.set(font='b', codepage='cp1251', size='2x', align='left', bold=1)
                p.writelines(x["Item_name"])
                for mod in x["Item_mods"]:
                    p.set(font='a', codepage='cp1251', size='2h', align='left', bold=1)
                    p.writelines(f'   Mods: {mod}')
                p.set(font='a', codepage='cp1251', size='2h', align='right', bold=1)
                p.writelines(x["Item_comments"])
                p.writelines(' ')
def update_order_status(order_id, order_status):
    url = f'{base_url}update_order_status'
    myobj = {'order_id': order_id,'order_status':order_status,'api_key':api_key}
    x = requests.post(url, data = myobj)
def update_print_status(order_id, print_status):
    url = f'{base_url}update_print_status'
    myobj = {'order_id': order_id,'print_status':print_status,'api_key':api_key}
    x = requests.post(url, data = myobj)
while True:
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Orders Last Checked at: ", current_time, end="\r")
        myresult = get_active_orders()
        for x in myresult:
           if x.order_printed == 0:
               generate_expoview(x)
               generate_kitchenview(x)
               update_print_status(x.order_id,1)
               update_order_status(x.order_id,3)

        time.sleep(15)
    except:
       print("fail")
       time.sleep(30)
