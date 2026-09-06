import os
import json
import streamlit as st
import google.generativeai as genai
import sources

# Page Configuration
st.set_page_config(page_title="ThreatLens", page_icon="🛡️", layout="wide")

# Configure Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)


def synthesize_threat_intelligence(target: str, target_type: str, level: str, results: list) -> dict:
    """Synthesizes target telemetry using Gemini API into structured JSON output."""
    if not gemini_api_key:
        return {
            "overall_verdict": "Error",
            "risk_score": 0,
            "summary": "Gemini API key is not configured.",
            "key_findings": ["API key missing."],
            "recommendations": ["Set GEMINI_API_KEY in environment or Streamlit secrets."]
        }

    prompt = f"""
    You are an expert cybersecurity threat analyst. Synthesize the following data for target '{target}' ({target_type}).
    Tailor your language complexity, technical depth, and actionable guidance for a user with '{level}' knowledge level.

    Telemetry Data:
    {json.dumps(results, indent=2)}

    Return ONLY a valid JSON object matching this schema:
    {{
      "overall_verdict": "Clean" | "Suspicious" | "Malicious",
      "risk_score": <int 0-100>,
      "summary": "<concise level-tailored summary>",
      "key_findings": ["<finding 1>", "<finding 2>"],
      "recommendations": ["<action 1>", "<action 2>"]
    }}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        # Fallback scoring when AI synthesis fails
        max_score = max([r.get("risk_score", 0) for r in results], default=0)
        verdict = "Malicious" if max_score >= 60 else "Suspicious" if max_score >= 20 else "Clean"
        return {
            "overall_verdict": verdict,
            "risk_score": max_score,
            "summary": f"Automated evaluation completed (AI synthesis error: {str(e)}).",
            "key_findings": [f"{r['source']}: {r['verdict']}" for r in results],
            "recommendations": ["Review individual source responses below."]
        }


# ==========================================
# UI & Workflow
# ==========================================
st.title("🛡️ ThreatLens Security Evaluator")
st.markdown("Automated threat intelligence aggregation and Gemini AI synthesis.")

# Input Controls
col1, col2 = st.columns([3, 1])
with col1:
    target_input = st.text_input("Enter Target (IP, Domain, or URL)", placeholder="e.g. 8.8.8.8, example.com, https://bad-site.com")
with col2:
    knowledge_level = st.selectbox("Target Knowledge Level", ["Beginner", "Intermediate", "Expert"])

analyze_button = st.button("Analyze Target", type="primary", use_container_width=True)

if analyze_button and target_input:
    target_type = sources.detect_target_type(target_input)
    
    st.info(f"Detected Target Type: **{target_type.upper()}**")

    # Step 3: Dynamic Orchestration over Registry
    collected_results = []
    with st.spinner("Fetching intelligence from threat sources..."):
        for source_name, fetch_func in sources.SOURCES.items():
            result = fetch_func(target_input, target_type)
            collected_results.append(result)

    # Step 4: AI Synthesis
    with st.spinner("Synthesizing analysis with Gemini AI..."):
        synthesis = synthesize_threat_intelligence(target_input, target_type, knowledge_level, collected_results)

    st.divider()

    # Step 5: Render Results
    verdict = synthesis.get("overall_verdict", "Clean")
    risk_score = synthesis.get("risk_score", 0)

    # Color-coded Banner Display
    if verdict == "Malicious":
        st.error(f"### Verdict: {verdict} | Risk Score: {risk_score}/100")
    elif verdict == "Suspicious":
        st.warning(f"### Verdict: {verdict} | Risk Score: {risk_score}/100")
    else:
        st.success(f"### Verdict: {verdict} | Risk Score: {risk_score}/100")

    # AI Insight Card
    st.subheader(f"💡 Threat Insights ({knowledge_level} Mode)")
    st.write(synthesis.get("summary", ""))

    col_findings, col_recs = st.columns(2)
    with col_findings:
        st.markdown("**Key Findings**")
        for finding in synthesis.get("key_findings", []):
            st.markdown(f"* {finding}")

    with col_recs:
        st.markdown("**Actionable Recommendations**")
        for rec in synthesis.get("recommendations", []):
            st.markdown(f"* {rec}")

    st.divider()

    # Dynamic Raw Data Expanders
    st.subheader("📊 Source Telemetry")
    for res in collected_results:
        source_title = res.get("source", "Unknown Source")
        status = res.get("verdict", "Unknown")
        
        with st.expander(f"{source_title} (Status: {status})"):
            if res.get("error"):
                st.error(f"Error: {res['error']}")
            else:
                st.json(res.get("raw_data", {}))

elif analyze_button and not target_input:
    st.warning("Please enter a valid IP address, Domain, or URL to analyze.")
