# News Sentiment Analyzer

## Overview
A Python tool that scrapes news websites and performs sentiment analysis to track emotional trends over time. Extracts article content, analyzes tone (positive/negative/neutral), and visualizes patterns.

## Key Features
- **Multi-source scraping**: Configured for CNN, BBC, Reuters
- **Dual NLP analysis**: Uses both TextBlob and VADER models
- **Time-based trends**: Weekly/monthly sentiment charts
- **Word frequency**: Top terms by sentiment category
- **Ethical scraping**: Respects robots.txt with rate limiting

## Quick Start
```bash
git clone https://github.com/yourusername/news-sentiment-analyzer.git
cd news-sentiment-analyzer
pip install -r requirements.txt
python main.py
```

## Configuration
Edit `config.py` to:
- Add new news sources
- Adjust sentiment thresholds
- Change time intervals (daily/weekly/monthly)

## Sample Outputs
- `results/sentiment_over_time.png`
- `results/word_frequency.csv`
- Console summary reports

## Requirements
Python 3.8+ with packages:
- BeautifulSoup4, Newspaper3k (scraping)
- TextBlob, NLTK (NLP)
- Pandas, Matplotlib (analysis)

## License
MIT License - Free for academic/commercial use with attribution
