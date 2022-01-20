import requests

resp = requests.get("https://www.taptap.com/webapiv2/apk/v1/list-by-app?app_id=139546&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D59%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D807d4770-751d-49c0-b49a-6ea259fecd72%26DT%3DPC")
print(resp.text)