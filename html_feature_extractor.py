"""
Real-Time HTML & Webpage Behaviour Feature Extraction Module.
MCA Research Project - Phase 5

Fetches live webpage HTML via HTTP/HTTPS, parses DOM structure using BeautifulSoup,
and extracts the 28 HTML/Behavioral features matching MLDataset.csv schema.
Includes comprehensive error handling for timeouts, SSL errors, and connection failures.
"""

import urllib.parse
import re
from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress insecure HTTPS warning when verify=False fallback is triggered
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The 28 HTML/Behavioral dataset feature names in exact column order
HTML_FEATURE_NAMES = [
    "LineOfCode",
    "LargestLineLength",
    "HasTitle",
    "DomainTitleMatchScore",
    "URLTitleMatchScore",
    "HasFavicon",
    "Robots",
    "IsResponsive",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
    "HasDescription",
    "NoOfPopup",
    "NoOfiFrame",
    "HasExternalFormSubmit",
    "HasSocialNet",
    "HasSubmitButton",
    "HasHiddenFields",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfImage",
    "NoOfCSS",
    "NoOfJS",
    "NoOfSelfRef",
    "NoOfEmptyRef",
    "NoOfExternalRef"
]


def _string_similarity(a: str, b: str) -> float:
    """
    Computes similarity score (0.0 to 100.0) between two strings.
    """
    if not a or not b:
        return 0.0
    return round(SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100.0, 2)


def fetch_webpage_html(url_string: str, timeout: int = 10) -> tuple:
    """
    Safely fetches live webpage HTML using requests with timeout & SSL fallback.
    Returns: (html_text, redirect_history_urls, status_code, error_message)
    """
    url_str = url_string.strip()
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', url_str):
        url_str = "http://" + url_str

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        response = requests.get(url_str, headers=headers, timeout=timeout, allow_redirects=True)
        redirect_urls = [r.url for r in response.history]
        return response.text, redirect_urls, response.status_code, ""
    except requests.exceptions.SSLError:
        # Fallback with SSL verification disabled
        try:
            response = requests.get(url_str, headers=headers, timeout=timeout, allow_redirects=True, verify=False)
            redirect_urls = [r.url for r in response.history]
            return response.text, redirect_urls, response.status_code, ""
        except Exception as ssl_err:
            return "", [], 0, f"SSL Error: {str(ssl_err)}"
    except requests.exceptions.Timeout:
        return "", [], 0, f"Connection Timeout ({timeout}s)"
    except requests.exceptions.ConnectionError:
        return "", [], 0, "Connection Refused / Domain Unreachable"
    except Exception as e:
        return "", [], 0, f"HTTP Fetch Error: {str(e)}"


def extract_html_features(url_string: str, timeout: int = 10) -> dict:
    """
    Extracts all 28 HTML/Behavioral features from a live URL.
    Returns a dictionary containing:
    - 'html_features': Dict of 28 numerical features matching MLDataset.csv
    - 'fetch_metadata': Status code, redirect count, error message, page title
    """
    html_text, redirect_history, status_code, fetch_error = fetch_webpage_html(url_string, timeout=timeout)

    # Pre-fill default fallback feature values (used if page unreachable)
    features = {feat: 0 for feat in HTML_FEATURE_NAMES}

    if fetch_error or not html_text:
        return {
            "html_features": features,
            "fetch_metadata": {
                "status_code": status_code,
                "redirect_count": len(redirect_history),
                "error_message": fetch_error or "Empty HTML body",
                "page_title": "",
                "fetch_success": False
            }
        }

    # Parse HTML with BeautifulSoup
    try:
        soup = BeautifulSoup(html_text, "html.parser")
    except Exception:
        soup = None

    lines = html_text.splitlines()
    line_count = len(lines)
    max_line_len = max([len(l) for l in lines], default=0)

    # If HTML is minified (few lines with huge line length), use prettified DOM formatting to calculate true structural lines of code
    if soup and (max_line_len > 500 or line_count < 100) and len(html_text) > 2000:
        line_count = len(soup.prettify().splitlines())

    features["LineOfCode"] = line_count
    features["LargestLineLength"] = max_line_len

    parsed_url = urllib.parse.urlparse(url_string if "://" in url_string else "http://" + url_string)
    domain = parsed_url.netloc.split(':')[0]
    
    # Extract clean domain brand name (e.g. 'youtube.com' -> 'youtube', 'www.google.co.uk' -> 'google')
    domain_parts = domain.replace('www.', '').split('.')
    brand_name = domain_parts[0] if len(domain_parts) >= 2 else domain

    # 3. HasTitle & Title similarity scores
    title_text = ""
    if soup and soup.title and soup.title.string:
        title_text = soup.title.string.strip()

    features["HasTitle"] = 1 if title_text else 0
    
    # Brand-aware title matching: compare full domain, clean brand name, and title
    if title_text:
        domain_match = _string_similarity(domain, title_text)
        brand_match = _string_similarity(brand_name, title_text)
        is_brand_in_title = brand_name.lower() in title_text.lower() or title_text.lower() in brand_name.lower()
        
        if is_brand_in_title and len(brand_name) > 2:
            features["DomainTitleMatchScore"] = 100.0
            features["URLTitleMatchScore"] = 100.0
        else:
            features["DomainTitleMatchScore"] = max(domain_match, brand_match)
            features["URLTitleMatchScore"] = max(_string_similarity(url_string, title_text), brand_match)
    else:
        features["DomainTitleMatchScore"] = 0.0
        features["URLTitleMatchScore"] = 0.0

    if soup:
        # 6. HasFavicon
        favicon_tags = soup.find_all("link", rel=lambda r: r and "icon" in r.lower() if r else False)
        features["HasFavicon"] = 1 if favicon_tags else 0

        # 7. Robots
        robots_meta = soup.find("meta", attrs={"name": re.compile(r'robots', re.I)})
        features["Robots"] = 1 if (robots_meta or 'robots' in html_text.lower()) else 0

        # 8. IsResponsive
        viewport_meta = soup.find("meta", attrs={"name": re.compile(r'viewport', re.I)})
        features["IsResponsive"] = 1 if (viewport_meta or "@media" in html_text) else 0

        # 11. HasDescription
        desc_meta = soup.find("meta", attrs={"name": re.compile(r'description', re.I)})
        features["HasDescription"] = 1 if desc_meta else 0

        # 12. NoOfPopup (window.open or alert scripts)
        script_text = " ".join([s.get_text() for s in soup.find_all("script")])
        popup_count = len(re.findall(r'window\.open\(|alert\(', script_text))
        features["NoOfPopup"] = popup_count

        # 13. NoOfiFrame
        features["NoOfiFrame"] = len(soup.find_all("iframe"))

        # Form analysis
        forms = soup.find_all("form")
        ext_form = 0
        has_submit = 0
        has_hidden = 0
        has_password = 0

        for form in forms:
            action = form.get("action", "")
            if action:
                action_domain = urllib.parse.urlparse(urllib.parse.urljoin(url_string, action)).netloc.split(':')[0]
                if action_domain and action_domain != domain:
                    ext_form = 1
            
            if form.find_all("input", type=re.compile(r'submit', re.I)) or form.find_all("button"):
                has_submit = 1

        if soup.find_all("input", type=re.compile(r'hidden', re.I)):
            has_hidden = 1
        if soup.find_all("input", type=re.compile(r'password', re.I)):
            has_password = 1

        features["HasExternalFormSubmit"] = ext_form
        features["HasSubmitButton"] = has_submit
        features["HasHiddenFields"] = has_hidden
        features["HasPasswordField"] = has_password

        # 15. HasSocialNet & Comprehensive DOM Reference Extraction
        social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com', 't.me']
        has_social = 0
        self_ref = 0
        empty_ref = 0
        ext_ref = 0

        # Extract references across <a>, <link>, <script>, <area>, <form> tags
        all_refs = soup.find_all(True, href=True) + soup.find_all(True, src=True)
        seen_urls = set()

        for tag in all_refs:
            ref_val = (tag.get("href") or tag.get("src") or "").strip()
            if not ref_val or ref_val == "#" or ref_val.startswith("javascript:"):
                empty_ref += 1
            elif ref_val not in seen_urls:
                seen_urls.add(ref_val)
                abs_href = urllib.parse.urljoin(url_string, ref_val)
                href_domain = urllib.parse.urlparse(abs_href).netloc.split(':')[0]

                if any(s in href_domain for s in social_domains):
                    has_social = 1

                if href_domain == domain or (brand_name and brand_name in href_domain):
                    self_ref += 1
                elif href_domain:
                    ext_ref += 1

        features["HasSocialNet"] = has_social
        features["NoOfSelfRef"] = self_ref
        features["NoOfEmptyRef"] = empty_ref
        features["NoOfExternalRef"] = ext_ref

        # Resource counts (including SVG, picture sources, meta image, custom web component images)
        img_tags = len(soup.find_all("img"))
        svg_tags = len(soup.find_all("svg"))
        meta_imgs = len(soup.find_all("meta", property=re.compile(r'image', re.I)))
        custom_imgs = len(soup.find_all(re.compile(r'img|image|yt-img', re.I)))
        features["NoOfImage"] = max(img_tags, img_tags + svg_tags + meta_imgs + custom_imgs)

        features["NoOfCSS"] = len(soup.find_all("link", rel=lambda r: r and "stylesheet" in r if r else False)) + len(soup.find_all("style"))
        features["NoOfJS"] = len(soup.find_all("script"))

    # Redirect metrics
    features["NoOfURLRedirect"] = len(redirect_history)
    self_redirects = 0
    for red_url in redirect_history:
        red_domain = urllib.parse.urlparse(red_url).netloc.split(':')[0]
        if red_domain == domain or red_domain.replace('www.', '') == domain.replace('www.', '') or (brand_name and brand_name in red_domain):
            self_redirects += 1
    features["NoOfSelfRedirect"] = self_redirects

    # Keyword indicators (case-insensitive search in visible text)
    page_text = soup.get_text().lower() if soup else html_text.lower()
    features["Bank"] = 1 if any(k in page_text for k in ['bank', 'login', 'account', 'verify', 'financial']) else 0
    features["Pay"] = 1 if any(k in page_text for k in ['pay', 'payment', 'paypal', 'credit', 'card', 'checkout']) else 0
    features["Crypto"] = 1 if any(k in page_text for k in ['crypto', 'bitcoin', 'btc', 'wallet', 'ethereum', 'eth', 'binance']) else 0
    features["HasCopyrightInfo"] = 1 if ('©' in html_text or 'copyright' in page_text or '&copy;' in html_text) else 0

    return {
        "html_features": features,
        "fetch_metadata": {
            "status_code": status_code,
            "redirect_count": len(redirect_history),
            "error_message": "",
            "page_title": title_text,
            "fetch_success": True
        }
    }


if __name__ == "__main__":
    import sys
    test_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.google.com"

    print(f"\nExtracting HTML features for: '{test_url}'")
    print("=" * 60)

    extracted = extract_html_features(test_url, timeout=5)
    meta = extracted["fetch_metadata"]

    print(f"Fetch Status   : Success={meta['fetch_success']} (Code {meta['status_code']})")
    print(f"Page Title     : '{meta['page_title']}'")
    print(f"Error Message  : '{meta['error_message']}'")

    print("\n📌 Extracted Dataset HTML Features (28 Covered):")
    print("-" * 60)
    for k, v in extracted["html_features"].items():
        print(f"  • {k:<28}: {v}")
    print("=" * 60)
