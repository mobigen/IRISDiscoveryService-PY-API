# IRISDiscoveryService-PY-API
angora에 job request를 보내고 response를 받을수 있게 해주는 python package

## 설치법
```
pip install git+https://github.com/mobigen/IRISDiscoveryService-PY-API.git

or

pip3 install git+https://github.com/mobigen/IRISDiscoveryService-PY-API.git
```

## 사용법
```
import service_api
sql_api = service_api.DiscoveryService()
conn = sql_api.connect(host="", port=0, user_id="", user_passwd="")

cursor = conn.cursor()

cursor.execute(
    q="",
    size=0, save=True)


cursor.response_data()
cursor.fetchall()
cursor.description()

cursor.close()
```
