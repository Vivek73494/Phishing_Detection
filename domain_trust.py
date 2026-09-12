"""
Domain Trust & Whitelist Verification Module
MCA Research Project - Hybrid Phishing Detection

Provides top global domain validation to eliminate false positives on apex domains
and legitimate login portals for top-tier global services.
"""

import urllib.parse
import re

# Top global verified apex domains (Tranco / Umbrella Top Tier)
TRUSTED_GLOBAL_DOMAINS = {
    "pinterest.com", "pinterest.co.uk", "pinterest.ca", "pinterest.fr", "pinterest.de", "pinterest.cl",
    "google.com", "google.co.in", "google.co.uk", "google.ca", "youtube.com", "gmail.com",
    "yahoo.com", "yahoo.co.in", "yahoo.co.uk", "ymail.com", "bing.com", "duckduckgo.com",
    "facebook.com", "instagram.com", "whatsapp.com", "messenger.com",
    "twitter.com", "x.com", "linkedin.com", "reddit.com", "quora.com", "medium.com", "tumblr.com",
    "github.com", "gitlab.com", "bitbucket.org", "stackoverflow.com",
    "wikipedia.org", "wikimedia.org", "w3schools.com", "geeksforgeeks.org",
    "amazon.com", "amazon.in", "amazon.co.uk", "ebay.com", "walmart.com", "target.com", "flipkart.com",
    "netflix.com", "spotify.com", "apple.com", "microsoft.com", "live.com", "office.com", "outlook.com",
    "dropbox.com", "adobe.com", "paypal.com", "stripe.com", "cloudflare.com", "wordpress.com",
    "discord.com", "slack.com", "zoom.us", "canva.com", "figma.com", "notion.so", "trello.com",
    "twitch.tv", "vimeo.com", "salesforce.com", "shopify.com", "coursera.org", "udemy.com",
    "archive.org", "ycombinator.com", "nytimes.com", "bbc.com", "cnn.com"
}

def extract_apex_domain(url_string: str) -> str:
    """Extracts clean apex domain (e.g., 'in.pinterest.com' -> 'pinterest.com')."""
    if not url_string:
        return ""
    url_str = url_string.strip()
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', url_str):
        url_str = "http://" + url_str
    
    try:
        parsed = urllib.parse.urlparse(url_str)
        netloc = parsed.netloc.split(':')[0].lower().replace('www.', '')
        
        # Check for IP address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', netloc):
            return netloc
            
        parts = netloc.split('.')
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return netloc
    except Exception:
        return ""

def check_domain_trust(url_string: str) -> dict:
    """
    Evaluates whether a URL belongs to a verified global trusted domain.
    Returns:
      {
         'is_trusted': bool,
         'apex_domain': str,
         'trust_reason': str
      }
    """
    apex = extract_apex_domain(url_string)
    
    # Check for obfuscation tricks like user:pass@trusted.com or %40
    raw_lower = url_string.lower()
    if "@" in raw_lower or "%40" in raw_lower:
        return {
            "is_trusted": False,
            "apex_domain": apex,
            "trust_reason": "Contains potential URL obfuscation (@ symbol)"
        }
        
    if apex in TRUSTED_GLOBAL_DOMAINS:
        return {
            "is_trusted": True,
            "apex_domain": apex,
            "trust_reason": f"Verified global apex domain ({apex})"
        }
        
    return {
        "is_trusted": False,
        "apex_domain": apex,
        "trust_reason": "Standard unverified domain"
    }
