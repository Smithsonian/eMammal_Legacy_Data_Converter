import json
import urllib
import urllib2
# creds = urllib.urlencode({'username':'aallegretti', 'password':'BlueRaster2014!', 'exclude_deployments':True})
creds = urllib.urlencode({'username':'aallegretti', 'password': 'BlueRaster2014!', 'exclude_deployments':True})
print creds
# creds = urllib.urlencode({'username':'aallegretti', 'password':'BlueRaster2014!', 'exclude_deployments':True})
request = urllib2.Request('https://emammal.si.edu/emammal_api/deployment/login', data=creds)
request = urllib2.urlopen(request)
print request.read()
# response = unicode(request.read(), 'latin-1')
# response_json = json.loads(response)
# session_name = response_json.get('session_name')
# session_id = response_json.get('sessid')
