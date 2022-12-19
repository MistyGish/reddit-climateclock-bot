import praw
import requests
from datetime import datetime
from dateutil import parser
import tokens
import os

r = requests.get('https://api.climateclock.world/v2/clock.json')

data = r.json()

carbon = data["data"]["modules"]["carbon_deadline_1"]["timestamp"]
carbon = parser.parse(carbon)

timezone = carbon.tzinfo
diff = carbon - datetime.now(timezone)
# print(diff)
# print(carbon)

# calculate countdown
days = diff.days
years = days / 365
years = int(years)
#months = (days - years * 365) / 30
days = days % 365

# logging in to account
reddit = praw.Reddit(client_id = tokens.client_id,
                    client_secret = tokens.client_secret,
                    username = tokens.username,
                    password = tokens.password,
                    user_agent = tokens.user_agent)

subreddits_list = "test+bottest"
subreddits = reddit.subreddit(subreddits_list)

def run_bot(reddit, comments_replied_to):
    keywords = ["climate change", "global warming"] # search for these strings in the subreddits_list 
    for comment in subreddits.comments():
        for keyword in keywords:
            if keyword in comment.body and comment.id not in comments_replied_to: 
            #and comment.author != reddit.user.me():
                reply_text = "There is " + str(years) + " years and " + str(days) + " days to limit global warming to 1.5 degrees Celcius"
                comment.reply(body = reply_text)
                comments_replied_to.append(comment.id)

                with open("replied_comments.txt", "a") as f:
                    f.write(comment.id + "\n")
                print(reply_text)


def saved_comments(): # create a text file, if one does not exist, to track comments that have been replied to
    if not os.path.isfile("C:\\Users\\Julia\\Documents\\redditpybot\\replied_comments.txt"):
        comments_replied_to = []
    else:
        with open("replied_comments.txt", "r") as f:
            comments_replied_to = r.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = filter(None, comments_replied_to)
    
    return comments_replied_to

comments_replied_to = saved_comments()
print(comments_replied_to)

while True:
    run_bot(reddit, comments_replied_to)