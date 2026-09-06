import os
import re
import base64
import requests
import whois
import streamlit as st

# ==========================================
# Input Type Helper
# ==========================================
def detect_target_type(target: str) -> str:
    """Detects whether the target input is an IP, Domain, or URL."""
    target = target.strip()
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    url_pattern = r"^https?://"

    if re.match(ip_pattern, target):
        return "ip"
    elif re.match(url_pattern, target):
        return "url"
    else:
        return "domain"

# ==========================================
# Data Source Extractors
# ==========================================
@st.cache_data(ttl=3600)
def get_virustotal(target: str, target_type: str) -> dict:
    """Fetches threat analysis data from VirusTotal API v3."""
    api_key = os.getenv("VIRUSTOTAL_API_KEY") or st.secrets.get("VIRUSTOTAL_API_KEY", "")
    
    if not api_key:
        return {
            "source": "VirusTotal",
            "verdict": "Error",
            "risk_score": 0,
            "raw_data": {},
            "error": "VIRUSTOTAL_API_KEY missing from environment/secrets."
        }

    headers = {"x-apikey": api_key}
    
    try:
        if target_type == "ip":
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{target}"
        elif target_type == "domain":
            url = f"https://www.virustotal.com/api/v3/domains/{target}"
        elif target_type == "url":
            url_id = base64.urlsafe_b64encode(target.encode()).decode().strip("=")
            url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        else:
            raise ValueError(f"Unsupported target type: {target_type}")

        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 404:
            return {
                "source": "VirusTotal",
                "verdict": "Clean",
                "risk_score": 0,
                "raw_data": {"message": "No record found on VirusTotal"},
                "error": None
            }
            
        resp.raise_for_status()
        data = resp.json().get("data", {}).get("attributes", {})
        
        stats = data.get("last_analysis_stats", {})
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)
        total = sum(stats.values()) or 1
        
        calculated_score = int(((malicious + suspicious * 0.5) / total) * 100)
        
        if malicious > 2:
            verdict = "Malicious"
        elif malicious > 0 or suspicious > 0:
            verdict = "Suspicious"
        else:
            verdict = "Clean"
            
        return {
            "source": "VirusTotal",
            "verdict": verdict,
            "risk_score": min(calculated_score, 100),
            "raw_data": {
                "stats": stats,
                "reputation": data.get("reputation", 0),
                "tags": data.get("tags", [])
            },
            "error": None
        }

    except Exception as e:
        return {
            "source": "VirusTotal",
            "verdict": "Error",
            "risk_score": 0,
            "raw_data": {},
            "error": str(e)
        }


@st.cache_data(ttl=3600)
def get_whois(target: str, target_type: str) -> dict:
    """Fetches registration and ownership metadata via WHOIS."""
    try:
        query_target = target
        if target_type == "url":
            query_target = re.sub(r"^https?://", "", target).split("/")[0].split(":")[0]

        w = whois.whois(query_target)

        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        expiration_date = w.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        raw_info = {
            "registrar": w.registrar,
            "creation_date": str(creation_date) if creation_date else "Unknown",
            "expiration_date": str(expiration_date) if expiration_date else "Unknown",
            "country": w.country or "Unknown",
            "emails": w.emails if isinstance(w.emails, list) else [w.emails] if w.emails else []
        }

        verdict = "Clean"
        risk_score = 0
        
        if not w.registrar:
            verdict = "Suspicious"
            risk_score = 30

        return {
            "source": "WHOIS",
            "verdict": verdict,
            "risk_score": risk_score,
            "raw_data": raw_info,
            "error": None
        }

    except Exception as e:
        return {
            "source": "WHOIS",
            "verdict": "Error",
            "risk_score": 0,
            "raw_data": {},
            "error": str(e)
        }

# ==========================================
# Central Sources Registry
# ==========================================
SOURCES = {
    "VirusTotal": get_virustotal,
    "WHOIS": get_whois
}
