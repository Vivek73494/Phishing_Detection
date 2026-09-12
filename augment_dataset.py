import os
import sys
import re
import urllib.parse
import pandas as pd
import numpy as np

from feature_extractor import extract_url_features
from html_feature_extractor import extract_html_features
from predict_url import EXPECTED_COLUMNS

DATASET_FILE = "MLDataset.csv"

# Comprehensive list of diverse legitimate URLs (bare domains, login paths, regional subdomains, popular apps)
LEGITIMATE_TARGET_URLS = [
    # Pinterest domain & path variations
    "https://pinterest.com",
    "https://www.pinterest.com",
    "https://in.pinterest.com",
    "https://uk.pinterest.com",
    "https://pinterest.com/login",
    "https://pinterest.com/signup",
    "https://pinterest.com/ideas/",
    "https://www.pinterest.com/pin/123456789/",

    # Social & Tech Apex / Bare domains
    "https://google.com",
    "https://www.google.com",
    "https://google.com/accounts",
    "https://mail.google.com",
    "https://drive.google.com",
    "https://youtube.com",
    "https://www.youtube.com",
    "https://facebook.com",
    "https://www.facebook.com",
    "https://facebook.com/login",
    "https://instagram.com",
    "https://www.instagram.com",
    "https://instagram.com/accounts/login",
    "https://twitter.com",
    "https://x.com",
    "https://linkedin.com",
    "https://www.linkedin.com",
    "https://linkedin.com/login",
    "https://github.com",
    "https://www.github.com",
    "https://github.com/login",
    "https://github.com/signup",
    "https://gitlab.com",
    "https://bitbucket.org",
    "https://stackoverflow.com",
    "https://reddit.com",
    "https://www.reddit.com",
    "https://reddit.com/login",
    "https://quora.com",
    "https://medium.com",
    "https://wikipedia.org",
    "https://en.wikipedia.org",
    "https://de.wikipedia.org",
    "https://fr.wikipedia.org",
    "https://amazon.com",
    "https://www.amazon.com",
    "https://amazon.in",
    "https://netflix.com",
    "https://www.netflix.com",
    "https://netflix.com/login",
    "https://spotify.com",
    "https://www.spotify.com",
    "https://spotify.com/login",
    "https://apple.com",
    "https://www.apple.com",
    "https://microsoft.com",
    "https://www.microsoft.com",
    "https://login.live.com",
    "https://dropbox.com",
    "https://www.dropbox.com",
    "https://adobe.com",
    "https://www.adobe.com",
    "https://paypal.com",
    "https://www.paypal.com",
    "https://paypal.com/signin",
    "https://ebay.com",
    "https://www.ebay.com",
    "https://walmart.com",
    "https://target.com",
    "https://yahoo.com",
    "https://bing.com",
    "https://duckduckgo.com",
    "https://cloudflare.com",
    "https://wordpress.com",
    "https://tumblr.com",
    "https://twitch.tv",
    "https://discord.com",
    "https://slack.com",
    "https://zoom.us",
    "https://canva.com",
    "https://figma.com",
    "https://notion.so",
    "https://trello.com",
    "https://steampowered.com",
    "https://vimeo.com",
    "https://salesforce.com",
    "https://shopify.com",
    "https://w3schools.com",
    "https://geeksforgeeks.org",
    "https://coursera.org",
    "https://udemy.com",
    "https://archive.org",
    "https://news.ycombinator.com",
    "https://nytimes.com",
    "https://bbc.com",
    "https://cnn.com"
]

def generate_augmented_rows():
    print(f"Loading existing dataset from '{DATASET_FILE}'...", flush=True)
    df_existing = pd.read_csv(DATASET_FILE)
    print(f"Current shape: {df_existing.shape}", flush=True)
    
    existing_cols = list(df_existing.columns)
    
    extracted_rows = []
    
    print("\nStarting feature extraction for legitimate target URLs...", flush=True)
    for idx, url in enumerate(LEGITIMATE_TARGET_URLS, 1):
        print(f"[{idx}/{len(LEGITIMATE_TARGET_URLS)}] Processing: {url}", flush=True)
        try:
            u_feats = extract_url_features(url)["dataset_url_features"]
            h_feats = extract_html_features(url, timeout=5)["html_features"]
            
            # Combine 50 numerical features
            merged = {**u_feats, **h_feats}
            
            # Extract metadata text columns to match MLDataset schema
            parsed = urllib.parse.urlparse(url if "://" in url else "http://" + url)
            netloc = parsed.netloc.split(':')[0]
            parts = netloc.split('.')
            tld = parts[-1] if len(parts) > 1 else ""
            domain = parts[-2] if len(parts) > 1 else netloc
            
            row_dict = {
                "URL": url,
                "Domain": domain,
                "TLD": tld,
                "Title": domain.capitalize(),
                "label": 1  # Legitimate label
            }
            row_dict.update(merged)
            
            # Replicate row variations to boost weight for bare domain and login features (15 copies per URL with minor noise for tree generalization)
            for mult in range(15):
                sample_dict = row_dict.copy()
                if mult > 0:
                    # Add tiny feature noise for robustness across minor HTML line length shifts
                    sample_dict["LineOfCode"] = max(10, int(sample_dict.get("LineOfCode", 500) * np.random.uniform(0.95, 1.05)))
                    sample_dict["LargestLineLength"] = max(100, int(sample_dict.get("LargestLineLength", 50000) * np.random.uniform(0.95, 1.05)))
                extracted_rows.append(sample_dict)

        except Exception as err:
            print(f"  └─ Error processing {url}: {err}")
            
    print(f"\nExtracted {len(extracted_rows)} augmented feature rows.")
    
    df_new = pd.DataFrame(extracted_rows)
    
    # Ensure all columns match original dataset schema
    for col in existing_cols:
        if col not in df_new.columns:
            df_new[col] = 0
            
    df_new = df_new[existing_cols]
    
    # Concatenate, deduplicate by URL, and save back to MLDataset.csv
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=['URL'], keep='last')
    df_combined.to_csv(DATASET_FILE, index=False)
    
    print(f"Successfully updated '{DATASET_FILE}'!")
    print(f"New dataset shape: {df_combined.shape}")
    print(f"Label breakdown:\n{df_combined['label'].value_counts()}")

if __name__ == "__main__":
    generate_augmented_rows()
