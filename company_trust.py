import requests
import re
import urllib.parse
from datetime import datetime

# Optional import for whois
try:
    import whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False

SUSPICIOUS_TLDS = {'.xyz', '.tk', '.ml', '.ga', '.cf', '.gq', '.top', '.work', '.info', '.biz'}
FREE_EMAIL_DOMAINS = {'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com', 'zoho.com', 'protonmail.com', 'yandex.com'}

def clean_url(url):
    """
    Cleans URL by ensuring it has a protocol.
    """
    if not url:
        return ""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def extract_domain(url):
    """
    Extracts the base domain from a URL.
    """
    if not url:
        return ""
    try:
        parsed = urllib.parse.urlparse(clean_url(url))
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.lower()
    except Exception:
        return ""

def check_website_availability(url):
    """
    Checks if website responds to HTTP requests.
    """
    cleaned = clean_url(url)
    if not cleaned:
        return False, None, ""
    try:
        # User-agent header to avoid bot blocking
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(cleaned, timeout=4, headers=headers)
        return r.status_code == 200, r.status_code, r.url
    except Exception as e:
        print(f"Website availability check failed for {url}: {e}")
        return False, None, ""

def check_ssl(url):
    """
    Checks if connection is encrypted (HTTPS).
    """
    cleaned = clean_url(url)
    return cleaned.startswith('https://')

def check_domain_age(domain):
    """
    Checks the age of the domain using WHOIS.
    """
    if not domain or not HAS_WHOIS:
        return False, 0.0, "WHOIS lookups not available (offline or missing whois library)"
        
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        
        if not creation_date:
            return False, 0.0, "Creation date not found in WHOIS data"
            
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if not isinstance(creation_date, datetime):
            return False, 0.0, "Invalid creation date format in WHOIS"
            
        age_days = (datetime.now() - creation_date).days
        age_years = age_days / 365.25
        
        is_old = age_years >= 2.0
        return is_old, round(age_years, 1), f"Domain is active for {round(age_years, 1)} years"
    except Exception as e:
        return False, 0.0, f"WHOIS query failed: {str(e)}"

def check_suspicious_tld(domain):
    """
    Checks if domain has a suspicious Top Level Domain (TLD).
    """
    if not domain:
        return False
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            return True
    return False

def validate_email_domain(email, company_name):
    """
    Checks if the email is official or suspicious.
    """
    if not email or '@' not in email:
        return False, "Invalid email address"
        
    domain = email.split('@')[-1].lower()
    
    if domain in FREE_EMAIL_DOMAINS:
        return False, f"Uses free public email provider ({domain})"
        
    # Check if company name is in the domain name
    cleaned_company = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())
    cleaned_domain = domain.split('.')[0]
    
    if cleaned_company in cleaned_domain or cleaned_domain in cleaned_company:
        return True, f"Uses official domain '{domain}' matching company name"
    else:
        return True, f"Uses custom domain '{domain}' (verify relationship to {company_name})"

def calculate_trust_score(company_name, website_url=None, contact_email=None):
    """
    Performs multi-factor trust verification and calculates a score (0-100).
    """
    score = 40.0  # Base score for any company
    checks = []
    
    # 1. Company Name check
    if company_name and len(company_name.strip()) > 1:
        score += 10.0
        checks.append({
            "name": "Company Name Presence",
            "passed": True,
            "detail": f"Company '{company_name}' is valid",
            "points": 10
        })
    else:
        checks.append({
            "name": "Company Name Presence",
            "passed": False,
            "detail": "Invalid or missing company name",
            "points": 0
        })

    # 2. Website Checks
    domain = ""
    if website_url:
        domain = extract_domain(website_url)
        is_avail, code, final_url = check_website_availability(website_url)
        if is_avail:
            score += 15.0
            checks.append({
                "name": "Website Availability",
                "passed": True,
                "detail": f"Website is active and reachable (HTTP {code})",
                "points": 15
            })
        else:
            score -= 10.0
            checks.append({
                "name": "Website Availability",
                "passed": False,
                "detail": f"Website could not be reached (offline or blocked)",
                "points": -10
            })
            
        # SSL Check
        if check_ssl(website_url):
            score += 10.0
            checks.append({
                "name": "SSL Secure Connection",
                "passed": True,
                "detail": "Website uses secure HTTPS connection",
                "points": 10
            })
        else:
            score -= 5.0
            checks.append({
                "name": "SSL Secure Connection",
                "passed": False,
                "detail": "Website uses insecure HTTP connection",
                "points": -5
            })
            
        # TLD Check
        if check_suspicious_tld(domain):
            score -= 15.0
            checks.append({
                "name": "TLD Risk Analysis",
                "passed": False,
                "detail": f"Domain ends in a suspicious TLD ({domain.split('.')[-1]}) commonly associated with spam/malware",
                "points": -15
            })
        else:
            score += 5.0
            checks.append({
                "name": "TLD Risk Analysis",
                "passed": True,
                "detail": f"Domain uses a standard safe TLD (.com, .org, .in, etc.)",
                "points": 5
            })
            
        # Domain Age Check
        is_old, age, detail = check_domain_age(domain)
        if is_old:
            score += 10.0
            checks.append({
                "name": "Domain Age",
                "passed": True,
                "detail": detail,
                "points": 10
            })
        else:
            # Neutral if whois failed, minor penalty if domain is fresh (less than 2 years)
            if age > 0:
                score += 2.0
                checks.append({
                    "name": "Domain Age",
                    "passed": False,
                    "detail": f"Domain is fresh ({age} years), verify business background",
                    "points": 2
                })
            else:
                checks.append({
                    "name": "Domain Age",
                    "passed": True,
                    "detail": detail,
                    "points": 0
                })
    else:
        checks.append({
            "name": "Website Provided",
            "passed": False,
            "detail": "No company website URL provided for verification",
            "points": 0
        })

    # 3. Email Check
    if contact_email:
        is_valid_email, email_detail = validate_email_domain(contact_email, company_name)
        if is_valid_email:
            score += 10.0
            checks.append({
                "name": "Contact Email Domain",
                "passed": True,
                "detail": email_detail,
                "points": 10
            })
        else:
            score -= 10.0
            checks.append({
                "name": "Contact Email Domain",
                "passed": False,
                "detail": email_detail,
                "points": -10
            })
    else:
        checks.append({
            "name": "Contact Email Provided",
            "passed": False,
            "detail": "No contact email provided for domain verification",
            "points": 0
        })

    # Check for established known corporate websites
    # E.g., if domain is google.com or tcs.com, give them a high score
    known_domains = {'tcs.com', 'infosys.com', 'wipro.com', 'google.com', 'flipkart.com', 'microsoft.com', 'amazon.com'}
    if domain in known_domains:
        score = 98.0
        checks.append({
            "name": "Verified Employer Registry",
            "passed": True,
            "detail": "This is a verified major enterprise domain",
            "points": 30
        })

    # Final score normalization (cap between 0 and 100)
    final_score = min(max(round(score, 1), 0.0), 100.0)
    
    if final_score >= 75:
        risk_level = "Low Risk"
    elif final_score >= 45:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"
        
    # Build explanation reasons summary
    reasons = []
    for check in checks:
        if not check["passed"] and check["points"] <= 0:
            reasons.append(check["detail"])
            
    if not reasons:
        reasons.append("All automated verification checks passed successfully.")
        
    return {
        "company_name": company_name,
        "website_url": website_url,
        "contact_email": contact_email,
        "trust_score": final_score,
        "risk_level": risk_level,
        "checks": checks,
        "reasons": reasons
    }
