#Base Twitter Class bangbang
#HTTP shit
import requests
from requests_oauthlib import OAuth1
import json

#Hash/enc shit
import hashlib
import hmac

#Rfor device id shit
import uuid
import random

class Twitter:
	def __init__(self):
		#Used for the Public Twitter API calls - Android Client Auth Creds
		self.login_key = "3nVuSoBZnx6U4vzUxf5w"
		self.login_secret = "Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys"
		
		#Used for the private Android mobile signup calls
		self.signup_key = "m9QsrrmJoANGROAiNKaC8g"
		self.signup_secret = "udnsc1IAyTQnkj0KPfZffb9usZ6ZqVoXcdD3oxIVo"
		self.register_url = "https://mobile.twitter.com/mobile_client_api/signup"
	
		#Client Configuration
		self.endpoint = "https://api.twitter.com/1.1/"
		self.response_type = ".json"
		self.clientVersion = "3.4.2"
		self.clientType = "TwitterAndroid"
		self.userAgent = "TwitterAndroid/3.4.2 (180) sdk/8 (unknown;generic;generic;sdk;0)"
		self.proxy = None
		self.deviceId = None
		
		#HTTP headers for Android client API calls (anything extra can be appended to the object easily)
		self.client_headers = {
			"User-Agent" : self.userAgent,
			"X-Client-UUID" : self.deviceId,
			"X-Twitter-Client" : self.clientType,
			"X-Twitter-Client-Version" : self.clientVersion,
			"Connection" : "Keep-Alive"
		}
		
		#I'm so fucking lazy
		self.hashtag = "%23"
		self.space = "%20"
		self.at = "%40"
		
		#Technical Account Variables
		self.rate_limit = None
		self.uid = None
		self.accessToken = None
		self.secret = None
		
		#Profile Account Variables
		self.screen_name = None
		self.password = None
		self.email = None
		self.fullname = None
		
		#Object to dump the profile info into
		self.profile_info = {}
	
	#Generate a new device Id for this Twitter instance - uuid4()
	def generateDeviceId(self):
		self.deviceId = str(uuid.uuid4())
		return self.deviceId

	#Set the deviceId for this Twitter instance
	def setDeviceId(self,deviceId):
		self.deviceId = deviceId
	
	#Sets the proxy to be used with this object
	def setProxy(self,proxy):
		self.proxy = proxy
	
	#Create an account on Twitter
	def signup(self,data):
		auth = OAuth1(self.signup_key,self.signup_secret)
		if self.deviceId == None:
			self.generateDeviceId()
		if self.proxy == None:
			r = requests.post(self.register_url, headers=self.client_headers, data=data, auth=auth)
		else:
			r = requests.post(self.register_url, headers=self.client_headers, data=data, auth=auth, proxies = self.proxy)
		if r.status_code == 200:
			if "oauth_token" in r.text:
				y = r.text.split("&")
				self.accessToken = y[0].replace("oauth_token=","")
				self.secret = y[1].replace("oauth_token_secret=","")
				self.uid = self.accessToken.split("-")[0]
				return True
			else:
				print "oAuth_Token not found in signup response."
				return False
		elif r.status_code == 403:
			response = json.loads(r.text.decode('utf8'))
			for error in response:
				print "Error: " + error
	
	#API member of Twitter class
	def api(self,method,path,data = None):
		auth = OAuth1(self.login_key, client_secret = self.login_secret,resource_owner_key = self.accessToken,resource_owner_secret = self.secret)
		url = self.endpoint + path
		if method == "GET":
			if self.proxy == None:
				r = requests.get(url, headers = self.client_headers, auth=auth)
			else:
				r = requests.get(url, headers = self.client_headers, auth=auth, proxies = self.proxy)
		elif method == "POST":
			if self.proxy == None:
				if data == None:
					r = requests.post(url, headers = self.client_headers, auth=auth)
				else:
					r = requests.post(url, headers = self.client_headers, auth=auth, data = data)
			else:
				if data == None:
					r = requests.post(url, headers = self.client_headers, auth=auth, proxies = self.proxy)
				else:
					r = requests.post(url, headers = self.client_headers, auth=auth, proxies = self.proxy, data = data)
		if r.status_code == 200:
			self.rate_limit = r.headers['x-rate-limit-remaining']
			response = json.loads(r.text.decode('utf8'))
			return response
		elif r.status_code == 403:
			response = json.loads(r.text.decode('utf8'))
			for error in response:
				print "Error: " + error
				return False
	
	#Fetch a users profile info - user_id OR screen_name is allowed for this method
	def getUser(self,user):
		response = self.api("GET","users/show.json?user_id=" + str(user))
		if response == False:
			print "Failed"
			return False
		else:
			return response


	#Search Twitter for whatever
	def search(self,query):
		response = self.api("GET","search/tweets.json?count=100&include_entities=false&q=" + str(query))
		if response == False:
			return False
		else:
			return response

	#Search tweets for query - "count" is set to 100. "pages" is generated automatically
	def scrapeSearch(self,query,pages):
		results = []
		tmp_max_id = None
		for page_num in range(0,pages):
			if page_num == 0:
				r = self.search(query)
				if r != False:
					results.append(r)
					for y in r['statuses']:
						tmp_max_id = y['id']
				else:
					return results
			else:
				r = self.search(query + "&max_id=" + str(tmp_max_id))
				if r != False:
					for y in r['statuses']:
						tmp_max_id = y['id']
				else:
					return results
		return results
