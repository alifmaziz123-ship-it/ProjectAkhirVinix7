import pandas as pd
import re
import os
from collections import Counter, defaultdict
from datetime import datetime

# Simple Indonesian stopwords (not exhaustive)
STOPWORDS = set([
    'yang','dan','di','ke','dari','ini','itu','untuk','sangat','pada','kali','aja','aja',
    'dengan','adalah','atau','tersebut','juga','kita','saya','cukup','lagi','ga','gak',
    'tidak','nya','ya','yang','ada','di','ke','dari','ini','itu','karena','tapi'
])

def load_dataframe():
    path1 = 'datagabung_5y.csv'
    path2 = 'datagabung.csv'
    if os.path.exists(path1):
        df = pd.read_csv(path1, encoding='utf-8')
    elif os.path.exists(path2):
        df = pd.read_csv(path2, encoding='utf-8')
    else:
        raise FileNotFoundError('Neither datagabung_5y.csv nor datagabung.csv found')
    return df

def parse_dates(df):
    if 'publishedAtDate' in df.columns:
        df['publishedAtDate_parsed'] = pd.to_datetime(df['publishedAtDate'], errors='coerce', utc=True)
    else:
        df['publishedAtDate_parsed'] = pd.NaT
    return df

def sentiment_from_stars(stars):
    try:
        s = int(stars)
    except Exception:
        return 'Netral'
    if s >= 4:
        return 'Positif'
    if s == 3:
        return 'Netral'
    return 'Negatif'

def tokenize(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    # remove urls and punctuation
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r"[^a-z0-9ąćęłńóśżźáéíóúâêîôûäëïöü'-]+", ' ', text)
    tokens = [t for t in text.split() if t and t not in STOPWORDS and len(t) > 1]
    return tokens

def build_data():
    df = load_dataframe()
    df = parse_dates(df)

    # Determine period
    dates = df['publishedAtDate_parsed'].dropna()
    if not dates.empty:
        min_date = dates.min().tz_convert(None)
        max_date = dates.max().tz_convert(None)
        period = f"{min_date.date()} - {max_date.date()}"
    else:
        period = "Unknown"

    # Stars distribution
    if 'stars' in df.columns:
        df['stars_int'] = pd.to_numeric(df['stars'], errors='coerce').fillna(0).astype(int)
    else:
        df['stars_int'] = 0

    stars_counts = df['stars_int'].value_counts().to_dict()
    stars_dist = {str(i): int(stars_counts.get(i, 0)) for i in range(1,6)}

    # Sentiment by stars heuristic
    df['sentiment'] = df['stars_int'].apply(sentiment_from_stars)
    sentiment_counts = df['sentiment'].value_counts().to_dict()
    sentiment_counts = {k: int(sentiment_counts.get(k, 0)) for k in ['Positif','Netral','Negatif']}

    total_data = len(df)

    # Yearly stats
    df['year'] = df['publishedAtDate_parsed'].dt.year.fillna(0).astype(int)
    years = sorted([y for y in df['year'].unique() if y > 0])
    yearly_sent = {'Positif': [], 'Netral': [], 'Negatif': []}
    avg_rating = []
    counts = []
    for y in years:
        sub = df[df['year'] == y]
        counts.append(int(len(sub)))
        avg_rating.append(float(sub['stars_int'].mean()) if len(sub) > 0 else 0.0)
        for s in ['Positif','Netral','Negatif']:
            yearly_sent[s].append(int((sub['sentiment'] == s).sum()))

    # Monthly for latest year present
    latest_year = years[-1] if years else datetime.now().year
    months = list(range(1,13))
    month_names = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
    monthly_counts = {s: [0]*12 for s in ['Positif','Netral','Negatif']}
    sub_latest = df[df['year'] == latest_year].copy()
    if not sub_latest.empty:
        sub_latest.loc[:, 'month'] = sub_latest['publishedAtDate_parsed'].dt.month.fillna(0).astype(int)
        for m in months:
            subm = sub_latest[sub_latest['month'] == m]
            for s in ['Positif','Netral','Negatif']:
                monthly_counts[s][m-1] = int((subm['sentiment'] == s).sum())

    # Top words per sentiment
    top_words = {'Positif': [], 'Negatif': [], 'Netral': []}
    for s in ['Positif','Netral','Negatif']:
        texts = df[df['sentiment'] == s]['text'].dropna().astype(str).tolist() if 'text' in df.columns else []
        counter = Counter()
        for t in texts:
            counter.update(tokenize(t))
        for word, cnt in counter.most_common(12):
            top_words[s].append({'word': word, 'count': int(cnt)})

    # Negative themes: top 7 negative words
    neg_themes = {w['word']: w['count'] for w in top_words['Negatif'][:7]}

    # Samples: pick up to 5 most recent per sentiment
    samples = {s: [] for s in ['Positif','Netral','Negatif']}
    for s in ['Positif','Netral','Negatif']:
        sub = df[df['sentiment'] == s].sort_values('publishedAtDate_parsed', ascending=False).head(5)
        for _, row in sub.iterrows():
            samples[s].append({
                'stars': int(row.get('stars_int', 0)),
                'date': (row['publishedAtDate_parsed'].date().isoformat() if pd.notna(row['publishedAtDate_parsed']) else ''),
                'text': str(row.get('text', ''))[:800]
            })

    # Attempt to preserve model metrics from existing static data if available
    try:
        from data import DATA as OLD_DATA
        model_no_weight = OLD_DATA.get('model_no_weight', {})
        model_weighted = OLD_DATA.get('model_weighted', {})
        model_balanced = OLD_DATA.get('model_balanced', {})
    except Exception:
        model_no_weight = {}
        model_weighted = {}
        model_balanced = {}

    DATA = {
        'meta': {
            'title': 'D\'Las Lembah Asri Serang Purbalingga',
            'source': 'Google Maps Reviews',
            'total_data': int(total_data),
            'train_size': int(max(0, int(total_data * 0.8))),
            'test_size': int(max(0, int(total_data * 0.2))),
            'period': period
        },
        'distribution': {
            'sentiment': sentiment_counts,
            'stars': stars_dist
        },
        'model_no_weight': model_no_weight,
        'model_weighted': model_weighted,
        'model_balanced': model_balanced,
        'yearly': {
            'years': years,
            'avg_rating': avg_rating,
            'count': counts,
            'sentiment_orig': yearly_sent,
        },
        'monthly_2024': {
            'months': months,
            'month_names': month_names,
            'Positif': monthly_counts['Positif'],
            'Netral': monthly_counts['Netral'],
            'Negatif': monthly_counts['Negatif']
        },
        'neg_themes': neg_themes,
        'top_words': top_words,
        'samples': samples
    }

    return DATA


DATA = build_data()
