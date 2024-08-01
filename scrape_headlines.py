import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch and parse headlines from a news website
def fetch_headlines(url, headline_tag, headline_class=None):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.content, 'html.parser')
        if headline_class:
            headlines = soup.find_all(headline_tag, class_=headline_class)
        else:
            headlines = soup.find_all(headline_tag)
        return [headline.get_text().strip() for headline in headlines]
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

# Define the websites and the corresponding tags and classes for headlines
news_sites = [
    {'url': 'https://www.bbc.com/news', 'tag': 'h3', 'class': 'gs-c-promo-heading__title'},
    {'url': 'https://www.bbc.com/innovation', 'tag': 'h3', 'class': 'gs-c-promo-heading__title'},
    {'url': 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen', 'tag': 'h3', 'class': 'ipQwMb ekueJc RD0gLb'},
    {'url': 'https://edition.cnn.com/', 'tag': 'h3', 'class': 'cd__headline-text'},
    {'url': 'https://www.reuters.com/', 'tag': 'h3', 'class': 'MediaStoryCard__title__1h6gk'},
    {'url': 'https://www.nytimes.com/', 'tag': 'h3', 'class': 'css-xxaj7r e1xfvim30'},
    {'url': 'https://www.theguardian.com/science', 'tag': 'h3', 'class': 'fc-item__title'},
    {'url': 'https://www.nbcnews.com/', 'tag': 'h2', 'class': 'styles_headline__1df1Z'},
    {'url': 'https://www.foxnews.com/', 'tag': 'h2', 'class': 'title title-color-default'},
    {'url': 'https://www.cbsnews.com/', 'tag': 'h4', 'class': 'item__hed'},
    {'url': 'https://www.usatoday.com/', 'tag': 'h3', 'class': 'gnt_m_flm_a'},
    {'url': 'https://www.washingtonpost.com/', 'tag': 'h2', 'class': 'font--headline'},
    {'url': 'https://www.bloomberg.com/', 'tag': 'h1', 'class': 'lede-text-v2__hed'},
    {'url': 'https://www.nationalgeographic.com/', 'tag': 'h2', 'class': 'Section__Title'},
    {'url': 'https://www.sciencenews.org/', 'tag': 'h2', 'class': 'post-title'},
    {'url': 'https://www.scientificamerican.com/', 'tag': 'h2', 'class': 't_article-title'},
    {'url': 'https://www.nature.com/', 'tag': 'h3', 'class': 'c-card__title'},
    {'url': 'https://www.newscientist.com/', 'tag': 'h2', 'class': 'card__title'}
]

# Fetch headlines and store them in a list
all_headlines = []
for site in news_sites:
    headlines = fetch_headlines(site['url'], site['tag'], site.get('class'))
    print(f"Headlines from {site['url']}: {headlines}")  # Debugging line
    for headline in headlines:
        all_headlines.append({'Headline': headline, ' Website': ' ' + site['url']})

# Check if headlines were fetched
if not all_headlines:
    print("No headlines were fetched. Please check the website structure or internet connection.")
else:
    # Convert the list of headlines to a DataFrame
    df = pd.DataFrame(all_headlines)

    # Save the DataFrame to a CSV file
    df.to_csv('headlines.csv', index=False)

    print('Headlines have been successfully scraped and saved to headlines.csv')
