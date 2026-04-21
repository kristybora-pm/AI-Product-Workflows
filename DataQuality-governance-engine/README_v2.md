# DataQuality Governance Engine

**An agentic data quality tool for stock plan administrators — built from a decade of fintech experience.**

Stock plan administrators at enterprise companies manage thousands of participant records across dozens of corporate clients. Bad data — missing SSNs, stale addresses, mismatched legal names, missing country codes — quietly breaks tax reporting, vesting calculations, and regulatory filings.

This tool automates the entire exception management workflow:

- Scans participant records against a configurable rule engine
- Flags violations with severity tagging
- Generates next-best-action guidance per exception
- Drafts outreach emails grouped by company for the Relationship Manager to review
- Saves drafts directly to Gmail — no automated sending, the human stays in the loop

---

## Live Demo

> Coming soon — Streamlit Cloud deployment in progress

---

## How It Works

```
CSV / participant data
        ↓
  Rule Engine scan
        ↓
  Exception list
        ↓
  Next-best-action per violation
        ↓
  Draft email per company (grouped)
        ↓
  → Gmail drafts (RM reviews before sending)
```

---

## Rules Engine

Four rules are active out of the box:

| Rule | Trigger | Severity |
|------|---------|----------|
| Missing SSN | SSN field is blank | Critical |
| Missing country | Country code not set | Critical |
| Stale address | Address not updated in 5+ years | Warning |
| Name mismatch | Display name ≠ legal name on file | Warning |

---

## Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/DataQuality-Governance-Engine.git
cd DataQuality-Governance-Engine
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Free Tier vs. AI-Powered Mode

### What works for free (no API key needed)

This app runs fully without any API key. The next-best-action suggestions and batch email drafts are powered by a **hardcoded rule-based engine** — each suggestion is specific to the violation type and references the actual participant name and company.

This was a deliberate choice to keep the prototype accessible and free to run for demo purposes. The rule-based suggestions are transparent, predictable, and good enough to demonstrate the full end-to-end workflow.

### Upgrading to AI-powered suggestions

If you want to go beyond hardcoded templates — for example, to generate more contextual, personalised suggestions based on participant history, company-specific patterns, or nuanced exception combinations — you can integrate the **Anthropic Claude API**.

To enable this:

1. Get an API key at [console.anthropic.com](https://console.anthropic.com)
2. Add $5 in credits (enough for thousands of runs with Claude Haiku)
3. Open the sidebar in the app and paste your key

With an API key connected, the app automatically switches from rule-based to AI-generated suggestions. Every next-best-action and email draft is written by Claude, personalised to the specific participant, company, and violation context.

### Why credits are needed for AI mode

The Anthropic API is a paid service beyond its free tier. For this use case the costs are minimal:

- **Next-best-action per violation:** ~$0.001 per suggestion (Claude Haiku)
- **Batch email draft per company:** ~$0.003 per email
- **Full scan of 100 participants:** under $0.15 total

For a production deployment, fine-tuning or prompt engineering Claude to better understand your firm's specific data governance policies, compliance requirements, and communication style would improve output quality significantly — but that goes beyond the free tier.

---

## Uploading Your Own Data

Upload a CSV from the sidebar with these columns:

```
id, name, company, email, admin_email, ssn, country, address, addr_year, legal_name
```

See `sample_participants.csv` for a working example with synthetic data.

---

## Tech Stack

| Layer | Tool |
|-------|------|
| UI & app framework | Streamlit |
| AI suggestions (optional) | Anthropic Claude Haiku |
| Gmail draft integration | Anthropic MCP + Gmail API |
| Data handling | Pandas |
| Language | Python 3.10+ |

---

## Author

Built by a fintech product professional with 10 years of experience across equity compensation, wealth management, and data platform engineering.

[LinkedIn](https://linkedin.com/in/yourprofile) · [GitHub](https://github.com/yourusername)

---

*This is a portfolio prototype. Synthetic data only — no real participant information is used or stored.*
