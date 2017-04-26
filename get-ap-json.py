import requests

url = "https://api.ciscospark.com/v1/rooms"

payload = "{\"title\" : \"Spark API via Postman\"}"
headers = {
    'authorization': "Bearer NWEyNWU1OGItMGU4Ni00MTE0LWE2N2MtYjBhNDZmYWZhYTVhMjZlYWNjNmQtODQ5",
    'content-type': "application/json; charset=utf-8",
    'cache-control': "no-cache",
    'postman-token': "573048e9-3389-4f92-afbc-891ebbecb16a"
    }

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)