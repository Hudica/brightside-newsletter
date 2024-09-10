import feedparser
import pandas as pd
from urllib.parse import urlparse

csv_path = './headline_data/headlines.csv'

def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc[4:]
    return f"{domain}"

# Function to fetch and parse headlines from an RSS feed
def fetch_headlines_from_rss(url):
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            headline_text = entry.title
            headline_url = entry.link
            headline_desc = entry.description
            domain_name = get_domain_name(headline_url)  # Extract domain name from the URL
            thumbnail = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else 'No Thumbnail'
            articles.append({'Headline': headline_text, 'URL': headline_url, 'Domain': domain_name, 'Thumbnail': thumbnail, 'Description': headline_desc})
        return articles
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

# RSS feed URLs
rss_urls = [
    'http://rss.cnn.com/rss/cnn_latest.rss',
    'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910',
    'https://feeds.bbci.co.uk/news/technology/rss.xml',
    'https://feeds.bbci.co.uk/news/rss.xml',
    'https://feeds.bbci.co.uk/news/education/rss.xml',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=44877279',
    'http://rss.cnn.com/rss/cnn_latest.rss/',
    'https://feeds.npr.org/1001/rss.xml',
    'http://feeds.reuters.com/Reuters/domesticNews',
    'https://www.environmental-expert.com/rss/news-8/health-safety',
    'https://feeds.finance.yahoo.com/rss/2.0/headline?s=msft&region=US&lang=en-US',
    'https://www.sciencedaily.com/rss/top/technology.xml',
    'https://www.sciencedaily.com/rss/top/environment.xml',
    'https://www.sciencedaily.com/rss/top/society.xml',
    'https://www.cbsnews.com/latest/rss/main',
    'https://www.cbsnews.com/latest/rss/technology',
    'https://www.cbsnews.com/latest/rss/politics',
    'https://www.cbsnews.com/latest/rss/world',
    'https://www.cbsnews.com/latest/rss/space',
    'https://www.wired.com/feed/tag/ai/latest/rss',
    'https://www.wired.com/feed/tag/ai/latest/rss',
    'https://www.wired.com/feed/category/culture/latest/rss',
    'https://www.wired.com/feed/category/business/latest/rss',
    'https://news.un.org/feed/subscribe/en/news/all/rss.xml',
    'https://news.un.org/feed/subscribe/en/news/region/americas/feed/rss.xml',
    'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
    'https://feeds.a.dj.com/rss/RSSWSJD.xml',
    'https://rss.politico.com/politics-news.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
]

# Fetch headlines from each RSS feed
all_headlines = []
for url in rss_urls:
    headlines = fetch_headlines_from_rss(url)
    print(f"{headlines}")  # Debugging line
    all_headlines.extend(headlines)

# Check if headlines were fetched
if not all_headlines:
    print("No headlines were fetched. Please check the RSS feed URL or internet connection.")
else:
    # Convert the list of headlines to a DataFrame
    df = pd.DataFrame(all_headlines)

    # Remove commas from all headlines and URLs (and handle thumbnails)
    df['Headline'] = df['Headline'].str.replace(',', '')

    # Save the DataFrame to a CSV file
    df.to_csv(csv_path, index=False)

    print('Headlines have been successfully scraped and saved to headlines.csv')
