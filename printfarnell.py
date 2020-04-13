#!/usr/bin/python3
from lxml import html
import requests
import socket
import os

TCP_IP = '0.0.0.0'
TCP_PORT = 1236
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

run = 1
while run:
    try:
        conn, addr = s.accept()
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        ordercode = str(int(data[-10:]))
        print ("ordercode:" + ordercode)
        page = requests.get('http://nl.farnell.com/search?st=' + ordercode,headers=headers)
        tree = html.fromstring(page.content)
        #print(page.content)
        component_info = tree.xpath('/html/body/div[1]/div[1]/main/div/div/div[2]/div[1]/section[1]/h2/span/text()')
        print("component_info:" + component_info[0])
        os.system("echo '" + component_info[0] + "' | glabels-3-batch --sheets=1 --copies=1 --first=1 componenten.glabels --input=- --output=printfile.ps")
        os.system("lp -d Brother-QL-710W printfile.ps")
        conn.close()
    except:
        conn.close()
        print("error")
        run=1
