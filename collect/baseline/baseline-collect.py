import tweepy
import datetime

consumerKey = 'eHKiFHZhsW9kAnxa90WyXzBnh'
consumerSecret = 'e1YAOtAiuB94nnnNPij70UkNQqjp8hSRk8BaQKYVtKS5zSPbdW'
accessToken = '778998688765112320-S4THC4k0brJocWuCGQV698aQHxEFzl4'
accessTokenSecret = 'I1KKdQgEnVgJp7xTm4idweTYXRNUaheplCgDHOzBPYO9P'

class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        f = open('temp_tweets/' + str(datetime.datetime.now()).replace(':', '.') + '.json', 'w')
        f.write(data)
        f.close()
        
        return True

    def on_error(self, status):
        f = open('errorlong.txt', 'w')
        f.write(str(datetime.datetime.now())+str(status))
        f.close()


l = StdOutListener()
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

stream = tweepy.Stream(auth, l)
stream.sample(languages=['in', 'en', 'ms'])

