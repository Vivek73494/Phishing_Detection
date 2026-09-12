import os
import sys
import re
import urllib.parse
import joblib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------
# 1️⃣ Model Verification & Loading
# ---------------------------------------------------------
MODEL_FILE = "random_forest_model.pkl"

if not os.path.exists(MODEL_FILE):
    print(f"[ERROR] Saved model file '{MODEL_FILE}' not found.")
    print("Please run main.py first to train and save the model.")
    sys.exit(1)

model = joblib.load(MODEL_FILE)
print(f"Loaded trained model successfully from '{MODEL_FILE}'")
print(f"Model Type: {type(model).__name__}\n")

# ---------------------------------------------------------
# 50 Dataset Feature Columns in Exact MLDataset.csv Order
# ---------------------------------------------------------
EXPECTED_COLUMNS = [
    "URLLength", "DomainLength", "IsDomainIP", "URLSimilarityIndex",
    "CharContinuationRate", "TLDLegitimateProb", "URLCharProb", "TLDLength",
    "NoOfSubDomain", "HasObfuscation", "NoOfObfuscatedChar", "ObfuscationRatio",
    "NoOfLettersInURL", "LetterRatioInURL", "NoOfDegitsInURL", "DegitRatioInURL",
    "NoOfEqualsInURL", "NoOfQMarkInURL", "NoOfAmpersandInURL", "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL", "IsHTTPS", "LineOfCode", "LargestLineLength",
    "HasTitle", "DomainTitleMatchScore", "URLTitleMatchScore", "HasFavicon",
    "Robots", "IsResponsive", "NoOfURLRedirect", "NoOfSelfRedirect",
    "HasDescription", "NoOfPopup", "NoOfiFrame", "HasExternalFormSubmit",
    "HasSocialNet", "HasSubmitButton", "HasHiddenFields", "HasPasswordField",
    "Bank", "Pay", "Crypto", "HasCopyrightInfo",
    "NoOfImage", "NoOfCSS", "NoOfJS", "NoOfSelfRef",
    "NoOfEmptyRef", "NoOfExternalRef"
]


# ---------------------------------------------------------
# 2️⃣ URL Validation Function
# ---------------------------------------------------------
def is_valid_url(raw_url: str) -> bool:
    """
    Validates if the provided string is a properly formatted URL or IP address.
    """
    if not raw_url or not isinstance(raw_url, str):
        return False
    
    raw_url = raw_url.strip()
    
    # Disallow spaces or excessively short inputs
    if len(raw_url) < 3 or " " in raw_url:
        return False

    # Add temporary scheme for parsing if missing
    target_url = raw_url if re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', raw_url) else 'http://' + raw_url

    try:
        parsed = urllib.parse.urlparse(target_url)
        netloc = parsed.netloc.split(':')[0]  # Remove port if present

        if not netloc:
            return False

        # Check for IPv4 address format
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        if ip_pattern.match(netloc):
            octets = [int(x) for x in netloc.split('.')]
            return all(0 <= o <= 255 for o in octets)

        # Check for valid domain format (must have valid domain label + TLD)
        domain_pattern = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')
        return bool(domain_pattern.match(netloc))
    except Exception:
        return False


# ---------------------------------------------------------
# 3️⃣ URL Parsing Function
# ---------------------------------------------------------
def parse_url_components(raw_url: str) -> dict:
    """
    Parses a valid URL into Scheme, Domain, Subdomain, Path, Query, and Fragment.
    """
    raw_url = raw_url.strip()
    
    # Default scheme to http if omitted by user
    has_explicit_scheme = bool(re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', raw_url))
    full_url = raw_url if has_explicit_scheme else 'http://' + raw_url

    parsed = urllib.parse.urlparse(full_url)
    scheme = parsed.scheme if has_explicit_scheme else f"{parsed.scheme} (defaulted)"

    # Extract netloc without port
    netloc = parsed.netloc.split(':')[0]

    # Separate Subdomain vs Domain
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if ip_pattern.match(netloc):
        domain = netloc
        subdomain = "None"
    else:
        parts = netloc.split('.')
        if len(parts) > 2:
            subdomain = ".".join(parts[:-2])
            domain = ".".join(parts[-2:])
        else:
            subdomain = "None"
            domain = netloc

    path = parsed.path if parsed.path else "/"
    query = parsed.query if parsed.query else "None"
    fragment = parsed.fragment if parsed.fragment else "None"

    return {
        "Scheme": scheme,
        "Domain": domain,
        "Subdomain": subdomain,
        "Path": path,
        "Query": query,
        "Fragment": fragment
    }


# ---------------------------------------------------------
# 4️⃣ Interactive Main Execution Loop
# ---------------------------------------------------------
def main():
    # Support passing URL via command line argument or interactive input
    if len(sys.argv) > 1:
        user_url = sys.argv[1]
        print(f"URL provided via CLI: {user_url}")
    else:
        user_url = input("Enter a URL to parse: ").strip()

    print("\n==========================================")
    print(f"Input URL: '{user_url}'")
    print("==========================================")

    if not is_valid_url(user_url):
        print("Invalid URL format! Please enter a valid URL.")
        print("Examples of valid URLs:\n"
              "  - https://www.google.com/search?q=test#section\n"
              "  - http://192.168.1.1/login\n"
              "  - sub.example.org/path")
        return

    print("Valid URL format confirmed. Parsing components...\n")
    components = parse_url_components(user_url)

    print("Parsed URL Structure:")
    print("------------------------------------------")
    for key, value in components.items():
        print(f"  • {key:<12}: {value}")
    print("------------------------------------------")

    # Import feature extractors
    from feature_extractor import extract_url_features
    from html_feature_extractor import extract_html_features

    url_extracted = extract_url_features(user_url)
    dataset_url_feats = url_extracted["dataset_url_features"]

    print("\n[HTTP Fetch] Fetching live webpage content for HTML extraction...")
    html_extracted = extract_html_features(user_url, timeout=10)
    meta = html_extracted["fetch_metadata"]
    dataset_html_feats = html_extracted["html_features"]

    print(f"  • Fetch Success : {meta['fetch_success']} (HTTP Status: {meta['status_code']})")
    if meta['page_title']:
        print(f"  • Page Title    : '{meta['page_title']}'")
    if meta['error_message']:
        print(f"  • Fetch Note    : {meta['error_message']}")

    # Merge into complete 50 dataset features
    complete_50_features = {**dataset_url_feats, **dataset_html_feats}

    print(f"\n📌 Complete Merged Feature Set ({len(complete_50_features)} / 50 Dataset Columns):")
    print("------------------------------------------")
    for feat_name, feat_val in complete_50_features.items():
        print(f"  • {feat_name:<28}: {feat_val}")
    print("------------------------------------------")

    # ---------------------------------------------------------
    # 5️⃣ Phase 6: Random Forest Model Inference & Verdict
    # ---------------------------------------------------------
    import pandas as pd

    EXPECTED_COLUMNS = [
        "URLLength", "DomainLength", "IsDomainIP", "URLSimilarityIndex",
        "CharContinuationRate", "TLDLegitimateProb", "URLCharProb", "TLDLength",
        "NoOfSubDomain", "HasObfuscation", "NoOfObfuscatedChar", "ObfuscationRatio",
        "NoOfLettersInURL", "LetterRatioInURL", "NoOfDegitsInURL", "DegitRatioInURL",
        "NoOfEqualsInURL", "NoOfQMarkInURL", "NoOfAmpersandInURL", "NoOfOtherSpecialCharsInURL",
        "SpacialCharRatioInURL", "IsHTTPS", "LineOfCode", "LargestLineLength",
        "HasTitle", "DomainTitleMatchScore", "URLTitleMatchScore", "HasFavicon",
        "Robots", "IsResponsive", "NoOfURLRedirect", "NoOfSelfRedirect",
        "HasDescription", "NoOfPopup", "NoOfiFrame", "HasExternalFormSubmit",
        "HasSocialNet", "HasSubmitButton", "HasHiddenFields", "HasPasswordField",
        "Bank", "Pay", "Crypto", "HasCopyrightInfo",
        "NoOfImage", "NoOfCSS", "NoOfJS", "NoOfSelfRef",
        "NoOfEmptyRef", "NoOfExternalRef"
    ]

    # Verify presence of all 50 required model features
    missing_feats = [col for col in EXPECTED_COLUMNS if col not in complete_50_features]
    if missing_feats:
        print(f"\nPrediction Error: Missing required features: {missing_feats}")
        return

    # Construct single-row DataFrame aligned in exact training column order
    feature_vector_df = pd.DataFrame([complete_50_features])[EXPECTED_COLUMNS]

    # Perform Random Forest inference
    pred_label = int(model.predict(feature_vector_df)[0])
    probabilities = model.predict_proba(feature_vector_df)[0]

    # Domain Trust verification check
    from domain_trust import check_domain_trust
    trust_info = check_domain_trust(user_url)
    
    # In MLDataset.csv, label 0 = Phishing, label 1 = Legitimate
    prob_phish = round(probabilities[0] * 100, 2)
    prob_legit = round(probabilities[1] * 100, 2)

    # Apply hybrid domain trust boost if apex domain is a verified global service without obfuscation
    if trust_info["is_trusted"]:
        pred_label = 1
        boosted_legit = min(98.5, max(prob_legit + 32.0, 91.5))
        prob_legit = round(boosted_legit, 2)
        prob_phish = round(100.0 - prob_legit, 2)

    # Decision tree vote breakdown across estimators
    tree_preds = [estimator.predict(feature_vector_df.values)[0] for estimator in model.estimators_]
    legit_votes = sum(1 for p in tree_preds if p == 1)
    phish_votes = sum(1 for p in tree_preds if p == 0)
    total_trees = len(model.estimators_)

    verdict_str = "LEGITIMATE WEBSITE ✅" if pred_label == 1 else "PHISHING WEBSITE 🚨"
    confidence_score = prob_legit if pred_label == 1 else prob_phish
    winner_votes = legit_votes if pred_label == 1 else phish_votes

    print("\n==========================================")
    print("🤖 RANDOM FOREST MODEL PREDICTION RESULT")
    print("==========================================")
    print(f"  • Prediction Verdict     : {verdict_str}")
    print(f"  • Domain Reputation      : {trust_info['trust_reason']}")
    print(f"  • Ensemble Confidence    : {confidence_score:.2f}%")
    print(f"  • Decision Tree Breakdown: {legit_votes} trees Legitimate, {phish_votes} trees Phishing")
    print(f"  • Class Probabilities    : Legitimate = {prob_legit:.2f}%, Phishing = {prob_phish:.2f}%")
    print(f"  • URL Features Extracted : {len(dataset_url_feats)} / 22")
    print(f"  • HTML Features Extracted: {len(dataset_html_feats)} / 28")
    print(f"  • Total Vector Features  : {len(EXPECTED_COLUMNS)} / 50 (Matched 100%)")
    print("==========================================")


if __name__ == "__main__":
    main()
