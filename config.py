# Websites to scrape (example with CNN)
NEWS_SOURCES = {
    'CNN': {
        'base_url': 'https://www.cnn.com',
        'search_url': 'https://www.cnn.com/search?q={query}&size={count}&from={start}&page={page}',
        'article_selector': 'div.container__field-links a',
        'title_selector': 'h1.headline__text',
        'content_selector': 'div.article__content',
        'date_selector': 'div.timestamp',
        'date_format': '%H:%M %M %d, %Y'
    }
}

# Analysis parameters
ANALYSIS_CONFIG = {
    'sentiment_threshold': 0.2,
    'time_interval': 'W'  # Weekly analysis
}