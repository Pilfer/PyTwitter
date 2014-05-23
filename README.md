PyTwitter
=========

Simple Twitter class written in Python


```python
#Instantiate the object
twitter = Twitter()
#Generate a device ID because reasons.
twitter.generateDeviceId()
#Example data to pass for twitter.signup()
data = {
	"fullname" : "John Smith",
	"screen_name" : "CodeStuffSwag",
	"email" : "yoloswag4jesus@gmail.com",
	"password" : "lOvEsOsA_bAnGbAnG",
	"lang" : "en"
}

signup_response = twitter.signup(data)
if signup_response == True:
	print "Signed up!"
	print twitter.accessToken
	print twitter.secret
	print twitter.uid
else:
	print "Failed to signup"


```
