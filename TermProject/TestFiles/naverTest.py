# -*- coding: utf-8 -*-
import http.client
server = "openapi.naver.com" #물음표까지 다써도됌
client_id = "J0xlzLY_mwqXVGY7OBho"
client_secret = "8NphEmVq6H"
conn = http.client.HTTPSConnection(server)
conn.request("GET", "/v1/search/book.xml?query=love&dispaly=10&start=1", None,{"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}) #서버에 GET 요청
#GET은 정보를 달라는것
#{"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
#이거는 http connection 문법인데,헤더에다가 클라이언트 아이디,시크릿을 추가했다

req = conn.getresponse()
print(req.status, req.reason) #200이 나와야 정상

cLen = req.getheader("Content-Length")  #헤더에서 Content-Length 즉 얼만큼 읽었는지 추출
print(req.read(int(cLen))) #그만큼 읽음

#한번읽으면 끝인가