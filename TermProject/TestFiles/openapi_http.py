# -*- coding:utf-8 -*-
import os
import sys
import http.client
from xml.dom.minidom import parseString
import urllib.parse

client_id = "NrkKI0dzkjbVyJJaGGg1"
client_secret = "bxP7XUH_Sh"


conn = http.client.HTTPSConnection("openapi.naver.com")

headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
encText = urllib.parse.quote("사랑")

params = "?query=" + encText + "&display=10&start=1"

conn.request("GET", "/v1/search/book.xml" + params, None, headers)
res = conn.getresponse()

if int(res.status) == 200 :
    print(parseString(res.read().decode('utf-8')).toprettyxml())
else:
    print ("HTTP Request is failed :" + res.reason)
    print (res.read().decode('utf-8'))

conn.close()