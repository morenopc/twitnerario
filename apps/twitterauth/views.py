from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
 
from oauthtwitter import OAuthApi
import oauth
 
CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'YOUR_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'YOUR_SECRET')
 
def twitter_signin(request):
	twitter = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET)
	request_token = twitter.getRequestToken()
	request.session['request_token'] = request_token.to_string()
	signin_url = twitter.getSigninURL(request_token)
	return HttpResponseRedirect(signin_url)
 
def twitter_return(request):
	request_token = request.session.get('request_token', None)
 
	# If there is no request_token for session,
	#    means we didn't redirect user to twitter
	if not request_token:
		# Redirect the user to the login page,
		# So the user can click on the sign-in with twitter button
		return HttpResponse("We didn't redirect you to twitter...")
 
	token = oauth.OAuthToken.from_string(request_token)
 
	# If the token from session and token from twitter does not match
	#   means something bad happened to tokens
	if token.key != request.GET.get('oauth_token', 'no-token'):
		del request.session['request_token']
		# Redirect the user to the login page
		return HttpResponse("Something wrong! Tokens do not match...")
 
	twitter = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, token)
	access_token = twitter.getAccessToken()
 
	request.session['access_token'] = access_token.to_string()
	auth_user = authenticate(access_token=access_token)
 
	# if user is authenticated then login user
	if auth_user:
		login(request, auth_user)
	else:
		# We were not able to authenticate user
		# Redirect to login page
		del request.session['access_token']
		del request.session['request_token']
		return HttpResponse("Unable to authenticate you!")
 
	# authentication was successful, use is now logged in
	return HttpResponse("You are logged in")
