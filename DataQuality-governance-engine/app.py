import streamlit as st
import pandas as pd
import anthropic
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Plan Governance Engine",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Sora:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
.main { background: #f4f5f9; }
.block-container { padding: 2rem 2.5rem; max-width: 1400px; }
.app-title { font-size: 26px; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 4px; }
.app-title span { color: #1a56db; }
.app-sub { font-size: 13px; color: #8b92b0; margin-bottom: 24px; }
.stat-card { background: white; border: 1px solid #dde0ee; border-radius: 10px; padding: 18px; }
.stat-num { font-family: 'DM Mono', monospace; font-size: 28px; font-weight: 600; line-height: 1; }
.stat-label { font-size: 11px; color: #8b92b0; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }
.stat-danger .stat-num { color: #dc2626; }
.stat-warn .stat-num   { color: #d97706; }
.stat-ok .stat-num     { color: #059669; }
.stat-blue .stat-num   { color: #1a56db; }
.tag { display: inline-block; font-family: 'DM Mono', monospace; font-size: 10px; font-weight: 500; padding: 2px 8px; border-radius: 4px; margin-right: 4px; }
.tag-ssn     { background: #fef2f2; color: #dc2626; }
.tag-country { background: #fffbeb; color: #d97706; }
.tag-address { background: #f5f3ff; color: #7c3aed; }
.tag-name    { background: #ecfeff; color: #0891b2; }
.nba-box { background: #f8f9ff; border: 1px solid #dde0ee; border-radius: 8px; padding: 14px; font-size: 13px; line-height: 1.7; color: #3d4259; margin-top: 8px; }
.issue-header { font-family: 'DM Mono', monospace; font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 4px; }
.issue-ssn     { color: #dc2626; border-left: 3px solid #dc2626; padding-left: 10px; }
.issue-country { color: #d97706; border-left: 3px solid #d97706; padding-left: 10px; }
.issue-address { color: #7c3aed; border-left: 3px solid #7c3aed; padding-left: 10px; }
.issue-name    { color: #0891b2; border-left: 3px solid #0891b2; padding-left: 10px; }
.draft-header { background: #f4f5f9; border: 1px solid #dde0ee; border-radius: 8px; padding: 10px 14px; font-size: 12px; color: #3d4259; margin-bottom: 12px; }
.success-pill { display: inline-block; background: #ecfdf5; color: #059669; border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 500; }
.warn-pill    { display: inline-block; background: #fffbeb; color: #d97706; border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 500; }
.divider { border: none; border-top: 1px solid #dde0ee; margin: 20px 0; }
[data-testid="stExpander"] { border: 1px solid #dde0ee !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
CURRENT_YEAR = 2026
STALE_THRESHOLD = 5

# ── Synthetic data ─────────────────────────────────────────────────────────────
DEFAULT_PARTICIPANTS = [
    {"id": "P001", "name": "Sarah Chen", "company": "Nexvera Corp", "email": "s.chen@nexvera.com", "admin_email": "admin@nexvera.com", "ssn": "", "country": "US", "address": "142 Oak Ave, Austin TX 78701", "addr_year": 2019, "legal_name": "Sarah L Chen"},
    {"id": "P002", "name": "Marcus Webb", "company": "Orbion Technologies", "email": "m.webb@orbion.io", "admin_email": "admin@orbion.io", "ssn": "532-88-1204", "country": "", "address": "88 Franklin St, Boston MA 02110", "addr_year": 2021, "legal_name": "Marcus Webb"},
    {"id": "P003", "name": "Priya Nair", "company": "Lumitex Inc", "email": "p.nair@lumitex.com", "admin_email": "plans@lumitex.com", "ssn": "", "country": "", "address": "9 Birch Ln, Chicago IL 60601", "addr_year": 2018, "legal_name": "Priya Nair"},
    {"id": "P004", "name": "James Okafor", "company": "Syncwave", "email": "j.okafor@syncwave.com", "admin_email": "equity@syncwave.com", "ssn": "701-44-9923", "country": "NG", "address": "15 Elm Rd, New York NY 10001", "addr_year": 2017, "legal_name": "James A. Okafor-Bello"},
    {"id": "P005", "name": "Elena Vasquez", "company": "Driftline Systems", "email": "e.vasquez@driftline.com", "admin_email": "hr@driftline.com", "ssn": "889-02-4417", "country": "US", "address": "3301 Pine Blvd, Seattle WA 98101", "addr_year": 2022, "legal_name": "Elena Vasquez"},
    {"id": "P006", "name": "Tom Ridgeway", "company": "Nexvera Corp", "email": "t.ridgeway@nexvera.com", "admin_email": "admin@nexvera.com", "ssn": "", "country": "GB", "address": "22 Victoria St, Austin TX 78702", "addr_year": 2016, "legal_name": "Thomas Ridgeway"},
    {"id": "P007", "name": "Ayesha Malik", "company": "Orbion Technologies", "email": "a.malik@orbion.io", "admin_email": "admin@orbion.io", "ssn": "244-71-8830", "country": "", "address": "Floor 2, 100 King St, Toronto", "addr_year": 2020, "legal_name": "Ayesha Malik"},
    {"id": "P008", "name": "Devon Brooks", "company": "Helixon Ltd", "email": "d.brooks@helixon.com", "admin_email": "stockplans@helixon.com", "ssn": "910-55-2201", "country": "US", "address": "501 Maple Dr, Denver CO 80201", "addr_year": 2015, "legal_name": "Devon Brooks Jr."},
    {"id": "P009", "name": "Mei Tanaka", "company": "Lumitex Inc", "email": "mei.tanaka@lumitex.com", "admin_email": "plans@lumitex.com", "ssn": "", "country": "JP", "address": "7-2 Shibuya, Tokyo", "addr_year": 2023, "legal_name": "Mei Tanaka"},
    {"id": "P010", "name": "Chris Oduya", "company": "Syncwave", "email": "c.oduya@syncwave.com", "admin_email": "equity@syncwave.com", "ssn": "603-29-7741", "country": "US", "address": "88 Lakeview Terrace, Miami FL 33101", "addr_year": 2021, "legal_name": "Christopher Oduya"},
]

# ── Rule-based fallback suggestions ───────────────────────────────────────────
RULE_SUGGESTIONS = {
    "ssn": (
        "Contact {name} directly at {company} to collect their Social Security Number "
        "using a secure data collection form — never via email. Once received, update "
        "the SSN field in the participant portal immediately, as this is required for "
        "W-2/1099 tax reporting and any equity award transactions."
    ),
    "country": (
        "Verify {name}'s country of residence by cross-referencing their address on file "
        "or contacting the {company} HR administrator. Update the country code in the "
        "participant record before the next vesting event, as this determines tax treaty "
        "eligibility and withholding rates for equity awards."
    ),
    "address": (
        "Reach out to {name} at {company} to confirm their current mailing address, as "
        "the record has not been updated in over 5 years. An accurate address is required "
        "for tax document delivery (W-2, 1099-B) and to meet broker compliance requirements "
        "for account statements."
    ),
    "name": (
        "The display name and legal name for {name} at {company} do not match — this must "
        "be resolved before any share transactions or tax filings. Ask the {company} HR "
        "administrator to provide a legal name confirmation document (passport or government ID) "
        "and update the legal name field in the participant record accordingly."
    ),
}


def rule_based_suggestion(rule_type, name, company):
    template = RULE_SUGGESTIONS.get(rule_type, RULE_SUGGESTIONS["ssn"])
    return template.format(name=name, company=company)


def rule_based_email(company, admin_email, participants_issues):
    lines = "\n".join(
        f"  - {pi['name']} ({pi['id']}): {'; '.join(e['found'] for e in pi['exceptions'])}"
        for pi in participants_issues
    )
    return (
        f"Dear {company} Stock Plan Administrator,\n\n"
        f"I hope this message finds you well. As part of our regular data quality review, "
        f"we have identified several participant records in your stock plan file that require "
        f"your attention to ensure compliance with tax reporting and regulatory requirements.\n\n"
        f"The following participants need updates:\n\n"
        f"{lines}\n\n"
        f"Accurate and up-to-date participant information is essential for correct tax withholding, "
        f"W-2/1099 preparation, and regulatory filings. Errors or omissions can result in penalties "
        f"for both the participant and your organisation.\n\n"
        f"Please update the relevant records in the participant portal by end of this week. "
        f"If you have any questions or need assistance, do not hesitate to reach out to your "
        f"dedicated relationship manager.\n\n"
        f"Thank you for your prompt attention to this matter.\n\n"
        f"Your Relationship Manager Team"
    )


# ── Claude helpers ─────────────────────────────────────────────────────────────
def get_client():
    api_key = st.session_state.get("api_key", "").strip()
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def get_nba(p, ex):
    client = get_client()
    if client:
        try:
            prompt = (
                f"You are a stock plan data governance assistant. Write a concise next-best-action "
                f"(2-3 sentences, plain text, no markdown, no bullets) for a stock plan administrator.\n\n"
                f"Participant: {p['name']} ({p['id']}), Company: {p['company']}\n"
                f"Issue: {ex['label']}\nDetails: {ex['found']}\n\nBe specific. Reference the participant by name."
            )
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        except Exception:
            pass
    return rule_based_suggestion(ex["type"], p["name"], p["company"])


def get_email_draft(company, admin_email, participants_issues):
    client = get_client()
    if client:
        try:
            lines = "\n".join(
                f"- {pi['name']} ({pi['id']}): {'; '.join(e['found'] for e in pi['exceptions'])}"
                for pi in participants_issues
            )
            prompt = (
                f"You are a relationship manager at a financial services firm writing to a stock plan administrator.\n\n"
                f"Company: {company}\nAdministrator email: {admin_email}\n\n"
                f"Participants needing updates:\n{lines}\n\n"
                f"Write a professional, warm email asking them to update these records. "
                f"List each participant and their issue clearly. Mention tax reporting and regulatory compliance. "
                f"Ask them to respond by end of week. Sign off as 'Your Relationship Manager Team'. "
                f"Plain text only, no markdown, no asterisks. Under 300 words."
            )
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        except Exception:
            pass
    return rule_based_email(company, admin_email, participants_issues)


# ── Rule engine ────────────────────────────────────────────────────────────────
def get_exceptions(p):
    ex = []
    if not p.get("ssn"):
        ex.append({"type": "ssn", "label": "Missing SSN", "found": "SSN field is blank"})
    if not p.get("country"):
        ex.append({"type": "country", "label": "Missing country", "found": "Country code not set"})
    age = CURRENT_YEAR - int(p.get("addr_year", CURRENT_YEAR))
    if age >= STALE_THRESHOLD:
        ex.append({"type": "address", "label": "Stale address", "found": f"Address last updated {p['addr_year']} ({age} yrs ago)"})
    if p.get("name", "").lower() != p.get("legal_name", "").lower():
        ex.append({"type": "name", "label": "Name mismatch", "found": f'Display: "{p["name"]}" vs Legal: "{p["legal_name"]}"'})
    return ex


def tag_html(ex_type, label):
    return f'<span class="tag tag-{ex_type}">{label}</span>'


# ── Session state ──────────────────────────────────────────────────────────────
if "participants" not in st.session_state:
    st.session_state.participants = DEFAULT_PARTICIPANTS
if "nba_cache" not in st.session_state:
    st.session_state.nba_cache = {}
if "draft_cache" not in st.session_state:
    st.session_state.draft_cache = {}
if "gmail_sent" not in st.session_state:
    st.session_state.gmail_sent = set()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.text_input(
        "Anthropic API key (optional)",
        type="password",
        help="Get a free key at console.anthropic.com — app works without it using rule-based suggestions",
        key="api_key"
    )
    if st.session_state.get("api_key"):
        st.success("API key set — AI suggestions enabled ✓")
    else:
        st.info("No API key — using smart rule-based suggestions")

    st.markdown("---")
    st.markdown("### 📂 Upload your own CSV")
    st.markdown("Columns: `id, name, company, email, admin_email, ssn, country, address, addr_year, legal_name`")
    uploaded = st.file_uploader("Upload CSV", type="csv")
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.session_state.participants = df.to_dict("records")
            st.session_state.nba_cache = {}
            st.session_state.draft_cache = {}
            st.success(f"Loaded {len(df)} participants")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

    if st.button("Reset to demo data"):
        st.session_state.participants = DEFAULT_PARTICIPANTS
        st.session_state.nba_cache = {}
        st.session_state.draft_cache = {}
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Rules active")
    st.markdown("🔴 Missing SSN  \n🟡 Missing country  \n🟣 Stale address (>5 yrs)  \n🔵 Name mismatch")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-title">Stock Plan <span>Governance</span> Engine</div>
<div class="app-sub">Exception detection · AI next-best-action · Batch Gmail drafts for RM review</div>
""", unsafe_allow_html=True)

# ── Compute exceptions ─────────────────────────────────────────────────────────
participants = st.session_state.participants
all_exceptions = {p["id"]: get_exceptions(p) for p in participants}
flagged = [p for p in participants if all_exceptions[p["id"]]]
clean = [p for p in participants if not all_exceptions[p["id"]]]
total_violations = sum(len(v) for v in all_exceptions.values())

# ── Stats row ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card stat-blue"><div class="stat-num">{len(participants)}</div><div class="stat-label">Total participants</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card stat-danger"><div class="stat-num">{len(flagged)}</div><div class="stat-label">With exceptions</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card stat-warn"><div class="stat-num">{total_violations}</div><div class="stat-label">Total violations</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card stat-ok"><div class="stat-num">{len(clean)}</div><div class="stat-label">Clean records</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Exception Dashboard", "📧 Batch Resolve → Gmail Drafts", "📥 Export"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Exception Dashboard
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    filter_opts = ["All exceptions", "Missing SSN", "Missing country", "Stale address", "Name mismatch"]
    fmap = {
        "All exceptions": None,
        "Missing SSN": "ssn",
        "Missing country": "country",
        "Stale address": "address",
        "Name mismatch": "name",
    }
    active_filter = st.selectbox("Filter by rule", filter_opts, label_visibility="collapsed")
    fkey = fmap[active_filter]
    display = flagged if not fkey else [p for p in flagged if any(e["type"] == fkey for e in all_exceptions[p["id"]])]

    if not display:
        st.info("No exceptions for this filter.")
    else:
        header = st.columns([1.2, 1.4, 1.2, 0.8, 0.8, 2, 0.8])
        for col, lbl in zip(header, ["Participant", "Company", "Email", "SSN", "Country", "Exceptions", ""]):
            col.markdown(f"<span style='font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:.07em;color:#8b92b0'>{lbl}</span>", unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        for p in display:
            ex = all_exceptions[p["id"]]
            cols = st.columns([1.2, 1.4, 1.2, 0.8, 0.8, 2, 0.8])
            with cols[0]:
                st.markdown(f"**{p['name']}**  \n<span style='font-family:monospace;font-size:11px;color:#8b92b0'>{p['id']}</span>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"<span style='font-size:12px'>{p['company']}</span>", unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f"<span style='font-size:11px;color:#3d4259'>{p['email']}</span>", unsafe_allow_html=True)
            with cols[3]:
                if p.get("ssn"):
                    st.markdown(f"<span style='font-family:monospace;font-size:11px'>{p['ssn']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:#dc2626;font-family:monospace;font-size:11px;font-style:italic'>— missing</span>", unsafe_allow_html=True)
            with cols[4]:
                if p.get("country"):
                    st.markdown(f"<span style='font-family:monospace;font-size:11px'>{p['country']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:#dc2626;font-family:monospace;font-size:11px;font-style:italic'>— missing</span>", unsafe_allow_html=True)
            with cols[5]:
                tags = "".join(tag_html(e["type"], e["label"]) for e in ex)
                st.markdown(tags, unsafe_allow_html=True)
            with cols[6]:
                if st.button("Detail →", key=f"detail_{p['id']}"):
                    current = st.session_state.get(f"expand_{p['id']}", False)
                    st.session_state[f"expand_{p['id']}"] = not current

            if st.session_state.get(f"expand_{p['id']}", False):
                with st.container():
                    st.markdown("<div style='background:#f8f9ff;border:1px solid #dde0ee;border-radius:10px;padding:16px;margin:8px 0 12px 0'>", unsafe_allow_html=True)
                    for e in ex:
                        st.markdown(f"<div class='issue-header issue-{e['type']}'>{e['label']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:12px;color:#3d4259;margin-bottom:6px'>{e['found']}</div>", unsafe_allow_html=True)
                        cache_key = f"{p['id']}-{e['type']}"
                        if cache_key not in st.session_state.nba_cache:
                            with st.spinner("Generating next-best-action…"):
                                st.session_state.nba_cache[cache_key] = get_nba(p, e)
                        st.markdown(f"<div class='nba-box'>💡 {st.session_state.nba_cache[cache_key]}</div>", unsafe_allow_html=True)
                        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    if clean:
        with st.expander(f"✅ {len(clean)} clean records"):
            for p in clean:
                st.markdown(f"**{p['name']}** ({p['id']}) — {p['company']}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Batch Resolve
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("**How it works:** One email drafted per company grouping all participant exceptions. Each draft saves to Gmail for RM review before sending.")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    companies = {}
    for p in flagged:
        ex = all_exceptions[p["id"]]
        if p["company"] not in companies:
            companies[p["company"]] = {"admin_email": p["admin_email"], "participants": []}
        companies[p["company"]]["participants"].append({"name": p["name"], "id": p["id"], "exceptions": ex})

    if not companies:
        st.info("No exceptions found — nothing to draft.")
    else:
        if st.button("🚀 Generate all drafts", type="primary"):
            for company, data in companies.items():
                if company not in st.session_state.draft_cache:
                    with st.spinner(f"Drafting email for {company}…"):
                        st.session_state.draft_cache[company] = get_email_draft(
                            company, data["admin_email"], data["participants"]
                        )
            st.rerun()

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        for company, data in companies.items():
            status_label = "✓ In Gmail drafts" if company in st.session_state.gmail_sent else "⏳ Pending RM review"
            with st.expander(f"📬 {company} — {len(data['participants'])} participant(s)  •  {status_label}"):

                if company not in st.session_state.draft_cache:
                    if st.button("Generate draft", key=f"gen_{company}"):
                        with st.spinner("Drafting…"):
                            st.session_state.draft_cache[company] = get_email_draft(
                                company, data["admin_email"], data["participants"]
                            )
                        st.rerun()
                else:
                    draft = st.session_state.draft_cache[company]
                    st.markdown(
                        f"<div class='draft-header'>"
                        f"<strong>To:</strong> {data['admin_email']}<br>"
                        f"<strong>Subject:</strong> Action Required: Participant Data Updates — {company}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    edited = st.text_area("Edit before saving:", value=draft, height=280, key=f"edit_{company}")
                    st.session_state.draft_cache[company] = edited

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if company not in st.session_state.gmail_sent:
                            if st.button("📨 Save to Gmail drafts", key=f"gmail_{company}", type="primary"):
                                with st.spinner("Saving to Gmail…"):
                                    try:
                                        client = get_client()
                                        if client:
                                            subject = f"Action Required: Participant Data Updates — {company}"
                                            gmail_prompt = (
                                                f"Create a Gmail draft (do NOT send it).\n\n"
                                                f"To: {data['admin_email']}\n"
                                                f"Subject: {subject}\n"
                                                f"Body:\n{edited}\n\n"
                                                f"Confirm in one sentence that the draft was saved."
                                            )
                                            client.messages.create(
                                                model="claude-sonnet-4-6",
                                                max_tokens=200,
                                                mcp_servers=[{"type": "url", "url": "https://gmailmcp.googleapis.com/mcp/v1", "name": "gmail"}],
                                                messages=[{"role": "user", "content": gmail_prompt}]
                                            )
                                            st.session_state.gmail_sent.add(company)
                                            st.success("✓ Draft saved to Gmail — ready for RM review")
                                        else:
                                            st.warning("Add your Anthropic API key in the sidebar to enable Gmail saving.")
                                    except Exception as e:
                                        st.error(f"Gmail error: {e}")
                                st.rerun()
                        else:
                            st.markdown("<span class='success-pill'>✓ Saved to Gmail drafts</span>", unsafe_allow_html=True)
                    with col2:
                        if st.button("🔄 Regenerate", key=f"regen_{company}"):
                            with st.spinner("Regenerating…"):
                                st.session_state.draft_cache[company] = get_email_draft(
                                    company, data["admin_email"], data["participants"]
                                )
                            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Export
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Download exception report")

    rows = []
    for p in flagged:
        for e in all_exceptions[p["id"]]:
            rows.append({
                "Participant ID": p["id"],
                "Name": p["name"],
                "Company": p["company"],
                "Email": p["email"],
                "Admin Email": p["admin_email"],
                "Rule": e["label"],
                "Details": e["found"],
                "Severity": "Critical" if e["type"] in ("ssn", "country") else "Warning",
                "Scanned At": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

    if rows:
        df_export = pd.DataFrame(rows)
        st.dataframe(df_export, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download exceptions_report.csv",
            data=df_export.to_csv(index=False),
            file_name="exceptions_report.csv",
            mime="text/csv",
            type="primary",
        )
    else:
        st.success("No exceptions found — all records are clean!")
