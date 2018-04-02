from src.tweet import Tweet
from src.preprocessing import Preprocessor
tweettext1 = "Today is a beautiful day!"
tweettext2 = "#NOCOLLUTION BY TRUMP IS THE FINDING, RULING, AND FACT! 😂😂😂😂😂"
tweettext3 = "The Lamb says he's with Trump but Voted against #TaxCuts for all Americans and will stand with the Devious Democrats constructing the #TaxHike Plan as we speak."

tweets = [Tweet(tweettext1), Tweet(tweettext2), Tweet(tweettext3)]
p = Preprocessor()
for tweet in tweets:
    print(tweet.text)
p.process(tweets)
for tweet in tweets:
    print(tweet.text)