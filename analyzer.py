from textblob import TextBlob
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# Download NLTK resources (only needed once)
nltk.download('vader_lexicon')
nltk.download('punkt')

class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze_sentiment_textblob(self, text):
        """Analyze sentiment using TextBlob"""
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    
    def analyze_sentiment_nltk(self, text):
        """Analyze sentiment using NLTK's VADER"""
        return self.sia.polarity_scores(text)['compound']
    
    def categorize_sentiment(self, score, threshold=0.2):
        """Categorize sentiment score into positive, neutral, negative"""
        if score > threshold:
            return 'positive'
        elif score < -threshold:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_articles(self, df):
        """Perform sentiment analysis on a dataframe of articles"""
        # Apply both sentiment analysis methods
        df['sentiment_textblob'] = df['text'].apply(self.analyze_sentiment_textblob)
        df['sentiment_nltk'] = df['text'].apply(self.analyze_sentiment_nltk)
        
        # Categorize sentiments
        df['sentiment_category'] = df['sentiment_nltk'].apply(
            lambda x: self.categorize_sentiment(x, ANALYSIS_CONFIG['sentiment_threshold'])
        )
        
        return df
    
    def visualize_sentiment_over_time(self, df):
        """Generate visualization of sentiment over time"""
        if 'date' not in df.columns:
            raise ValueError("DataFrame must contain 'date' column")
        
        # Ensure datetime format
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Resample by time interval
        resampled = df.resample(ANALYSIS_CONFIG['time_interval'])
        
        # Calculate mean sentiment over time
        sentiment_over_time = resampled['sentiment_nltk'].mean()
        
        # Plot
        plt.figure(figsize=(12, 6))
        sentiment_over_time.plot(
            kind='line',
            title='Sentiment Over Time',
            ylabel='Sentiment Score',
            xlabel='Date',
            grid=True
        )
        
        # Add horizontal line at zero
        plt.axhline(0, color='black', linestyle='--')
        
        return plt
    
    def visualize_sentiment_distribution(self, df):
        """Show distribution of sentiment categories"""
        plt.figure(figsize=(10, 6))
        sns.countplot(
            data=df,
            x='sentiment_category',
            order=['negative', 'neutral', 'positive']
        )
        plt.title('Distribution of Sentiment Categories')
        return plt
    
    def word_frequency_analysis(self, df, n=20):
        """Analyze most frequent words by sentiment"""
        from collections import Counter
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        import string
        
        # Get stopwords
        stop_words = set(stopwords.words('english'))
        
        # Initialize results
        results = {
            'positive': Counter(),
            'negative': Counter(),
            'neutral': Counter()
        }
        
        for _, row in df.iterrows():
            category = row['sentiment_category']
            text = row['text'].lower()
            
            # Tokenize and filter
            words = [
                word for word in word_tokenize(text) 
                if word not in stop_words 
                and word not in string.punctuation
                and word.isalpha()
            ]
            
            results[category].update(words)
        
        # Get top N words for each category
        top_words = {
            category: counter.most_common(n)
            for category, counter in results.items()
        }
        
        return top_words