from scraper import NewsScraper
from analyzer import SentimentAnalyzer
from config import NEWS_SOURCES, ANALYSIS_CONFIG
import pandas as pd
import os

def main():
    # Initialize components
    cnn_config = NEWS_SOURCES['CNN']
    scraper = NewsScraper(cnn_config)
    analyzer = SentimentAnalyzer()
    
    # User input
    query = input("Enter search query (e.g., 'climate change'): ")
    article_count = int(input("How many articles to analyze? (10-100): "))
    
    print(f"\nScraping articles about '{query}'...")
    articles_df = scraper.scrape_articles(query, count=article_count)
    
    if articles_df.empty:
        print("No articles found. Exiting.")
        return
    
    print("\nAnalyzing sentiment...")
    analyzed_df = analyzer.analyze_articles(articles_df)
    
    # Save results
    os.makedirs('results', exist_ok=True)
    filename = f"results/{query.replace(' ', '_')}_sentiment_analysis.csv"
    analyzed_df.to_csv(filename, index=False)
    print(f"\nResults saved to {filename}")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    time_plot = analyzer.visualize_sentiment_over_time(analyzed_df)
    time_plot.savefig(f"results/{query.replace(' ', '_')}_sentiment_over_time.png")
    
    dist_plot = analyzer.visualize_sentiment_distribution(analyzed_df)
    dist_plot.savefig(f"results/{query.replace(' ', '_')}_sentiment_distribution.png")
    
    # Word frequency analysis
    top_words = analyzer.word_frequency_analysis(analyzed_df)
    for category, words in top_words.items():
        print(f"\nTop words in {category} articles:")
        for word, count in words:
            print(f"{word}: {count}")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()