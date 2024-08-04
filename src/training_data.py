import feedparser
import pandas as pd

complete_path = '../data/real_training_data.csv'

def getHeadlines(url):
    try:
        feed = feedparser.parse(url)
        headline_data = []
        for entry in feed.entries:
            headline = entry.title
            desc = entry.description
            combined_data = f"{headline}, {desc}"
            headline_data.append({'Data': combined_data})
        return headline_data
    except Exception as e:
        print(e)


rss_urls = [
    'http://rss.cnn.com/rss/cnn_latest.rss',
    'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
    'https://www.reuters.com/rssFeed/technology/',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910',
    'https://feeds.bbci.co.uk/news/technology/rss.xml',
    'https://feeds.bbci.co.uk/news/rss.xml',
    'https://feeds.bbci.co.uk/news/education/rss.xml',
    
]

all_headlines = []
for url in rss_urls:
    headlines = getHeadlines(url)
    all_headlines.extend(headlines)

df = pd.DataFrame(all_headlines)

df.to_csv(complete_path, index=False)