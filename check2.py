import urllib.request
req = urllib.request.Request('https://apsrtc-tracker-1122-a6g5hfbag5cxftg4.centralindia-01.azurewebsites.net/api/dashboard')
print(urllib.request.urlopen(req).read().decode())
