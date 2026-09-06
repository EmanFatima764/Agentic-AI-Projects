# 🤖 Smart Lead AI

**AI-powered lead research and personalized outreach automation using advanced web scraping and generative AI.**

---

## 🚀 Try the Live App

**[→ Launch Smart Lead AI on Streamlit](https://smartleadai-wws2riguac5x9gjxbldypd.streamlit.app/)** ⭐

Experience the full lead research and email generation workflow in action. Just enter a business website URL!

---

## 📌 Project Overview

Smart Lead AI automates the lead research and outreach workflow. Traditional lead research is time-consuming and repetitive—visiting websites, gathering business information, analyzing company operations, and drafting personalized emails can take 15-20 minutes per prospect.

Smart Lead AI solves this by automating the entire pipeline:

1. **Extract** — Scrapes comprehensive website data (title, meta description, body content)
2. **Analyze** — Uses Google Gemini AI to understand the business and identify pain points
3. **Generate** — Creates personalized, compelling cold email pitches tailored to each prospect
4. **Store** — Saves lead intelligence to Google Sheets for CRM integration and team collaboration

The result: lead research that used to take 15-20 minutes per company is now completed in under 60 seconds.

---

## 🚀 Features

### 🌐 Website Data Extraction
Smart Lead AI uses **Playwright** (a modern browser automation framework) to scrape websites with JavaScript rendering support. The scraper:
- Launches a headless Chrome browser
- Waits for network requests to complete before extracting data
- Captures page title, meta description, and full visible text content
- Handles network failures and timeouts gracefully
- Limits extracted content to prevent oversized payloads

### 🤖 AI-Powered Lead Analysis & Email Generation
Powered by **Google Gemini 3.6 Flash**, the AI engine:
- Analyzes scraped website content to understand the business model
- Generates a 2-sentence company summary
- Identifies a specific pain point or growth opportunity
- Writes a compelling 3-sentence personalized cold email pitch
- Executes with low latency for real-time feedback

The AI uses carefully engineered prompts positioning the LLM as a "world-class B2B sales expert" to ensure high-quality output.

### ✉️ Personalized Email Generation
Rather than generic templates, Smart Lead AI generates emails that:
- Reference specific details from the prospect's website
- Demonstrate research and understanding of their business
- Identify potential pain points in their industry/operations
- Present a compelling value proposition
- Follow sales best practices (short, conversational, action-oriented)

### 📊 Google Sheets Integration
Lead data is automatically saved to Google Sheets with:
- **URL** — Target website
- **Title** — Page title/company name
- **Meta Description** — Company description
- **AI Analysis & Pitch** — Full AI-generated summary and email

Authentication uses Google service account credentials (OAuth 2.0) for secure API access. Teams can share a single sheet and see all researched leads in real-time.

### ⚡ Automated Workflow
The complete pipeline runs seamlessly:
- User provides a website URL via Streamlit UI
- Website data is extracted automatically
- AI processes the data and generates analysis
- Results are displayed instantly
- User can download as CSV or save to Google Sheets
- Full process completes in under 60 seconds

---

## 🛠️ Technologies Used

| Technology | Purpose | Version/Details |
| --- | --- | --- |
| **Python** | Core application logic | 3.10+ |
| **Streamlit** | Interactive web UI and dashboard | Latest |
| **Playwright** | Headless browser automation & web scraping | Latest |
| **Google Gemini API** | Generative AI (gemini-3.6-flash) for analysis & email generation | Latest |
| **google-genai** | Python SDK for Google Gemini | Latest |
| **gspread** | Google Sheets API client library | Latest |
| **google-auth** | Google authentication (OAuth 2.0 service account) | Latest |
| **Pandas** | Data manipulation & CSV export | Latest |
| **python-dotenv** | Environment variable management | Latest |
| **openpyxl** | Excel file support (dependency) | Latest |

**System Dependencies** (in `packages.txt` for cloud deployment):
- Chromium browser dependencies for Playwright (libnss3, libnspr4, libatk, libcups2, libdrm2, etc.)

---

## 🗂️ Project Structure

```
SmartLeadAI/
│
├── app.py                 # Main Streamlit application (UI & orchestration)
├── scraper.py            # Website scraping logic using Playwright
├── ai_engine.py          # AI analysis & email generation using Google Gemini
├── sheets.py             # Google Sheets integration
│
├── requirements.txt      # Python package dependencies
├── packages.txt          # System package dependencies (for cloud deployment)
├── .gitignore            # Git ignore rules (env files, credentials, cache)
│
└── README.md            # This file
```

### File Descriptions

- **app.py** — Streamlit interface. Accepts URL input, orchestrates scraping → AI processing → results display, provides CSV download
- **scraper.py** — Playwright browser automation. Launches headless Chrome, navigates to URL, extracts title/description/content
- **ai_engine.py** — Gemini API integration. Sends scraped data with crafted prompt, receives AI-generated summary and email
- **sheets.py** — Google Sheets API client. Saves lead data rows to authenticated Google Sheet using service account credentials

---

## 🔄 Lead Generation Workflow

```
┌─────────────────────────────────┐
│   User Enters Website URL       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Playwright Browser Launch     │
│   (Headless Chromium)           │
└────────────┬─────���──────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Website Scraping              │
│   (Title, Meta, Content)        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Data Validation & Parsing     │
│   (Limit to 1500 chars)         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Send to Google Gemini API     │
│   (Engineered B2B Sales Prompt) │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   AI Generates:                 │
│   - Company Summary (2 sent)    │
│   - Pain Point Analysis         │
│   - Cold Email Pitch (3 sent)   │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Display Results in Streamlit  │
│   - Website Info (left column)  │
│   - AI Analysis (right column)  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   User Options:                 │
│   • Download as CSV             │
│   • Save to Google Sheets       │
└─────────────────────────────────┘
```

---

## 🧠 AI Processing

Smart Lead AI leverages **Google Gemini 3.6 Flash** (a frontier-grade generative AI model) for fast, accurate business analysis.

### Prompt Engineering Strategy

The AI engine uses a carefully crafted system prompt that positions the model as a "world-class B2B sales expert." This priming:
- Ensures sales-focused analysis over generic summaries
- Improves personalization and relevance of cold emails
- Encourages identification of genuine business pain points
- Results in higher open rates and response rates on generated emails

### Input to AI

The prompt sends:
- **Website URL** — Reference point for context
- **Page Title** — Company/service name
- **Meta Description** — Official company tagline
- **First 1500 Characters** — Body content (web content, products, services)

### AI Output

The model generates structured analysis:
1. **Summary** — Exactly 2 sentences explaining what the company does
2. **Pain Point** — Specific identified opportunity or challenge
3. **Personalized Email** — Exactly 3-sentence cold email pitch

### Processing & Validation

- Response text is stripped of extra whitespace
- Output is returned as plain text (not requiring JSON parsing in current version)
- Errors are caught and displayed to user without crashing the application

### Why Gemini 3.6 Flash?

- **Speed** — Ultra-low latency for real-time UI feedback (~2-3 seconds per lead)
- **Accuracy** — Strong performance on business analysis and sales writing tasks
- **Cost** — Token-efficient pricing for high-volume lead research
- **Quality** — Produces professional, compelling cold emails

---

## 📊 Google Sheets Integration

Smart Lead AI stores all researched leads in a shared Google Sheet for team collaboration and CRM integration.

### Authentication Flow

```
Service Account Credentials (credentials.json)
               ↓
Google OAuth 2.0 (Service Account)
               ↓
Google Sheets API (gspread)
               ↓
Append Lead Row to Sheet
```

### Google Sheets Setup

1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account
4. Download service account JSON credentials → save as `credentials.json`
5. Share your Google Sheet with the service account email address
6. Reference sheet name in the function call

### Data Columns Stored

| Column | Data | Type |
| --- | --- | --- |
| A | URL | String (website URL) |
| B | Title | String (page title/company name) |
| C | Meta Description | String (company description from SEO meta) |
| D | AI Analysis & Pitch | String (full AI-generated summary + email) |

### API Details

- **Library** — `gspread` (Python Google Sheets client)
- **Auth Method** — OAuth 2.0 service account
- **Scope** — `https://www.googleapis.com/auth/spreadsheets`
- **Operation** — `append_row()` (adds new row to first worksheet)
- **Error Handling** — Returns success/error status without breaking application flow

---

## ⚙️ Installation Guide

### 1���⃣ Clone Repository

```bash
git clone https://github.com/EmanFatima764/SmartLeadAI.git
cd SmartLeadAI
```

### 2️⃣ Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Streamlit (web UI framework)
- Playwright (browser automation)
- Google Gemini API client
- gspread & google-auth (Google Sheets access)
- Pandas (data manipulation)
- python-dotenv (environment variables)
- openpyxl (Excel support)

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Getting Your Gemini API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key" in a new project
3. Copy the key and paste into `.env`

**Alternative:** Store `GEMINI_API_KEY` in Streamlit secrets (`~/.streamlit/secrets.toml`) for production deployments.

### 5️⃣ Configure Google Sheets (Optional)

If you want to save leads to Google Sheets:

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project

2. **Enable Google Sheets API**
   - Search for "Google Sheets API"
   - Click "Enable"

3. **Create Service Account**
   - Go to APIs & Services → Credentials
   - Click "Create Credentials" → Service Account
   - Name: `SmartLeadAI`
   - Create and continue

4. **Generate JSON Key**
   - Click the created service account
   - Go to Keys tab
   - Click "Add Key" → Create new key → JSON
   - Download and save as `credentials.json` in project root

5. **Share Google Sheet**
   - Create a new Google Sheet (or use existing one)
   - Share it with the service account email (found in `credentials.json`)
   - Grant Editor access
   - Note the sheet name for use in `sheets.py`

### 6️⃣ Install Browser Dependencies (for local development)

Playwright will automatically download Chromium, but you may need system dependencies:

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y $(cat packages.txt)
```

**On macOS:**
```bash
brew install --cask chromium
```

**On Windows:**
Playwright typically handles this automatically.

### 7️⃣ Run Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📈 Application Preview

### User Interface Workflow

**Step 1: URL Input**
```
⚡ SmartLead AI - Lead Intelligence System

Enter a business website URL and the system will scan the website, 
analyze the information with AI, and create a personalized cold email pitch.

[URL input field: https://example.com]  [Start Analysis Button]
```

**Step 2: Processing**
```
1/2: Scraping the website...
[spinner]

2/2: AI is analyzing the lead and creating a personalized email pitch...
[spinner]
```

**Step 3: Results Display**
```
─────────────────────────────────────────────
🎯 Results

📌 Website Information:              🤖 AI Analysis & Email Pitch:
Title: Example Domain               You are a world-class B2B sales expert.
Meta Description: Illustration      [AI-generated analysis]:
                                     
                                     Summary: ...
                                     Pain Point: ...
                                     Email Pitch: ...
─────────────────────────────────────────────

[📥 Download Results as CSV Button]
```

**Step 4: Export Options**
- Download as CSV for local storage and email templates
- Manually save to Google Sheets using `sheets.py` function

### Expected Output Example

```
URL: https://example.com
Title: Example Domain
Meta Description: Illustration domain for documents
AI Analysis & Pitch:

1. **Summary:** Example.com provides a reference domain for illustrative purposes in technical documentation and internet standards. It's used globally as a standard placeholder for examples and [...]

2. **Pain Point:** As a non-commercial informational domain, Example.com lacks monetization opportunities and advanced feature development that could enhance its utility for developers and techni[...]

3. **Personalized Email Pitch:** I noticed Example.com is the go-to reference domain for millions of developers worldwide. Could we explore creating premium documentation templates or certificati[...]
```

---

## 📋 Example Workflow

**Scenario:** You're a B2B SaaS sales rep researching prospects for outreach.

```
INPUT: https://www.myprospect.com

↓ [Smart Lead AI processes]

STEP 1: Website Scraping
  ✓ Title: "MyProspect - AI-Powered Customer Analytics"
  ✓ Description: "Helping SaaS teams understand customer behavior"
  ✓ Content: [1500 chars of product info, features, pricing page text]

STEP 2: AI Analysis
  ✓ Processing with Gemini AI...
  ✓ Analyzing business model, customer focus, technology stack

STEP 3: Results Generated
  ✓ Summary: "MyProspect is a customer analytics platform for SaaS teams..."
  ✓ Pain Point: "Current solution lacks real-time event tracking..."
  ✓ Email: "Hi MyProspect team, I saw you're helping SaaS teams [research-informed pitch]..."

STEP 4: Export
  ✓ Download as CSV for email templates
  ✓ Append to Google Sheets for team tracking
  ✓ Ready to send personalized outreach!

Total Time: ~45 seconds
```

---

## 👨‍💻 Developer

**Eman Fatima**
- GitHub: [@EmanFatima764](https://github.com/EmanFatima764)
- Repository: [SmartLeadAI](https://github.com/EmanFatima764/SmartLeadAI)

---

## 📝 License

This project is open source. Check the repository for license details.

---

## 🔗 Quick Links

- [🚀 Live App](https://smartleadai.streamlit.app/) — Try it now!
- [Google AI Studio](https://aistudio.google.com/) — Get Gemini API key
- [Google Cloud Console](https://console.cloud.google.com/) — Set up service account
- [Playwright Docs](https://playwright.dev/) — Browser automation reference
- [Streamlit Docs](https://docs.streamlit.io/) — UI framework reference
- [gspread Docs](https://docs.gspread.org/) — Google Sheets API reference

---

**Smart Lead AI** — Automating lead research for modern sales teams. ⚡
