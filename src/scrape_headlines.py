import feedparser
import pandas as pd

csv_path = '../headline_data/headlines.csv'

# Function to fetch and parse headlines from an RSS feed
def fetch_headlines_from_rss(url):
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            headline_text = entry.title
            headline_url = entry.link
            headline_desc = entry.description
            # Some feeds include a thumbnail, accessed differently depending on the feed
            thumbnail = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else 'No Thumbnail'
            articles.append({'Headline': headline_text, 'URL': headline_url, 'Thumbnail': thumbnail, 'Description': headline_desc})
        return articles
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

# RSS feed URLs
rss_urls = [
    'http://rss.cnn.com/rss/cnn_latest.rss',
    'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
    'https://www.reuters.com/rssFeed/technology/',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910',
    'https://feeds.bbci.co.uk/news/technology/rss.xml',
    'https://feeds.bbci.co.uk/news/rss.xml',
    'https://feeds.bbci.co.uk/news/education/rss.xml',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=44877279',
    
]

# Fetch headlines from each RSS feed
all_headlines = []
for url in rss_urls:
    headlines = fetch_headlines_from_rss(url)
    print(f"Headlines from {url}: {headlines}")  # Debugging line
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
