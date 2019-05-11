# -*- coding: utf-8 -*-
#https://api.neople.co.kr/df/servers?apikey=fS1DhnBRYjp0EIzzj2pMONApSNSkhOYV
#캐릭터 이미지 URL : https://img-api.neople.co.kr/df/servers/<serverId>/characters/<characterId>?zoom=<zoom>


import http.client
server = "api.neople.co.kr" #물음표까지 다써도됌
client_id = ""
client_secret = "su795WU14mjFeoFzOitaqgPYKXzXF5BI"
conn = http.client.HTTPSConnection(server)
#conn.request("GET", "/df/servers/cain/characters?characterName=dog&jobId=<jobId>&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
#conn.request("GET", "/df/servers?apikey=fS1DhnBRYjp0EIzzj2pMONApSNSkhOYV")
#conn.request("GET","/df/servers/cain/characters/110078ca2514a8ba02f9d62bbc730806?apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
#서버에 GET 요청
#GET은 정보를 달라는것
#{"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
#이거는 http connection 문법인데,헤더에다가 클라이언트 아이디,시크릿을 추가했다

req = conn.getresponse()
print(req.status, req.reason) #200이 나와야 정상

cLen = req.getheader("Content-Length")  #헤더에서 Content-Length 즉 얼만큼 읽었는지 추출
print(req.read(int(cLen))) #그만큼 읽음


#한번읽으면 끝인가