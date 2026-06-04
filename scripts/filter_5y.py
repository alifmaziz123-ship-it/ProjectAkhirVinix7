import pandas as pd
from datetime import datetime, timedelta

INPUT = 'datagabung.csv'
OUTPUT = 'datagabung_5y.csv'

def parse_iso(dt):
    try:
        return pd.to_datetime(dt, utc=True)
    except Exception:
        return pd.NaT

def main():
    df = pd.read_csv(INPUT, encoding='utf-8')
    # Parse publishedAtDate (e.g. 2024-10-10T07:54:25.351Z)
    if 'publishedAtDate' not in df.columns:
        print('publishedAtDate column not found in', INPUT)
        return

    df['publishedAtDate_parsed'] = df['publishedAtDate'].apply(parse_iso)

    # Cutoff = today - 5 years
    today = datetime(2026, 6, 4)
    cutoff = pd.Timestamp(datetime(today.year - 5, today.month, today.day), tz='UTC')

    df_filtered = df[df['publishedAtDate_parsed'] >= cutoff].copy()

    # Drop helper column before saving
    df_filtered = df_filtered.drop(columns=['publishedAtDate_parsed'])

    df_filtered.to_csv(OUTPUT, index=False, encoding='utf-8-sig')
    print(f'Wrote {len(df_filtered):,} rows to {OUTPUT}')

if __name__ == '__main__':
    main()
