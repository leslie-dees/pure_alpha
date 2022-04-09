import tweepy
import config as config
import pandas as pd



def get_tweet_data(my_id_enter):
    """
    Creates a csv file of all tweet fields specified in the Paginator
    params:
    >my_id_enter: id information returned by get_user_data. run get_user_data with a given screen name and input the result in here
    return vals:
    >csv of all info witihn the tweets
    -id -> tweet id
    -date -> date that the tweet was made
    -this_is_reply -> True if the tweet was a reply to another tweet. False if the tweet was a retweet or an original
    -text -> the text contained in the tweet
    -retweets -> number of retweets
    -replies -> number of replies
    -likes -> number of likes
    -quotes -> number of times the tweet was quoted
    -attachments -> attachments in the tweet, gifs, pics
    -entities -> urls, hashtags, mentions
    """
    my_id = int(my_id_enter[1])
    
    column_names = ['id', 'date', 'this_is_reply', 'text', 'retweets', 'replies', 'likes', 'quotes','attachments', 'entities']
    df = pd.DataFrame(columns = column_names)

    client = tweepy.Client(bearer_token=config.BEARER_TOKEN, wait_on_rate_limit = True)
    NoneType = type(None)
    
    for tweet in tweepy.Paginator(client.get_users_tweets, id = my_id, max_results = 100, tweet_fields=['id', 'created_at', 'in_reply_to_user_id', 'public_metrics', 'attachments', 'text', 'entities']).flatten(limit=1000):
        rowAdd = pd.DataFrame({
            'id':[tweet.id],
            'date':[tweet.created_at],
            'this_is_reply': [type(tweet.in_reply_to_user_id) != NoneType],
            'text':[tweet.text],
            'retweets':[tweet.public_metrics['retweet_count']],
            'replies':[tweet.public_metrics['reply_count']],
            'likes':[tweet.public_metrics['like_count']],
            'quotes':[tweet.public_metrics['quote_count']],
            'attachments':[tweet.attachments],
            'entities':[tweet.entities]
        })

        df = pd.concat([df, rowAdd], ignore_index = True, axis=0)

    df.to_csv(str(my_id_enter[0])+'.csv')    



def get_user_data(screen_name):
    """
    params:
    >screen_name: twitter screen name for a single user (do not include the @)
    return vals:
    >returns a list of values associated with the user
    -[0]: screen name of the user
    -[1]: id of the user
    -[2]: followers count of the user
    -[3]: following count of the user
    """
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN, wait_on_rate_limit = True)
    twitterid = client.get_user(username=screen_name, user_fields='public_metrics')

    return [screen_name, twitterid.data.id, twitterid.data.public_metrics['followers_count'], twitterid.data.public_metrics['following_count']]



#my_id = get_user_data('badccvoid')
#print(my_id)


#thingy = get_tweet_data(my_id)
#print(thingy)
