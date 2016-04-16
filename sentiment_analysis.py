# sentiment analysis 
# Exclaimer: This code is based on the script by Ravikiran Janardhana on Twitter analysis 
import re
import csv 
import nltk
import codecs


def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        	features['contains(%s)' % word] = (word in tweet_words)
    return features

def processTweet(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Remove all urls 
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Remove all tags by users 
    tweet = re.sub('@[^\s]+','',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = tweet.strip('\'"')

    return tweet
#end

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        w = processTweet(w)
        featureVector.append(w.lower())
    return featureVector
#end

with codecs.open('training_set.csv', encoding='utf-8', errors='replace') as f:
    inpTweets = csv.reader(f)
    featureList = []

	# Get tweet words
    tweets = []
    for row in inpTweets:
        sentiment = row[0]
        tweet = row[1]
        processedTweet = processTweet(tweet)
        featureVector = getFeatureVector(processedTweet)
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment));
	#end loop

	# Remove featureList duplicates
    featureList = list(set(featureList))

	# Extract feature vector for all tweets in one shote
    training_set = nltk.classify.util.apply_features(extract_features, tweets)

    NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

	# Test the classifier
    testTweet = 'Oh'
    processedTestTweet = processTweet(testTweet)
    print (NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet))))



