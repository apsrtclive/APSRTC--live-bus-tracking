import urllib.request, json
req = urllib.request.Request('https://apsrtc-tracker-1122-a6g5hfbag5cxftg4.centralindia-01.azurewebsites.net/api/user/login', data=json.dumps({'username': 'MP', 'password': '11'}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    res = urllib.request.urlopen(req)
    print(res.getcode())
    print(res.read().decode())
except Exception as e:
    print(e.code if hasattr(e, 'code') else e)
    print(e.read().decode() if hasattr(e, 'read') else '')
