# AI Pipeline: Tailored Resume & Outreach Generator

## The Objective
Automate the highly manual process of tailoring executive resumes to specific fintech job descriptions while bypassing ATS filters.

## System Architecture
* **Inputs:** Target Job Description (Text) + Master Resume Data Lake (PDF).
* **Processing:** LLM extracts the top metrics, enforcing strict length constraints (max 400 words) and isolating experiences by company timeline.
* **Output Generation:** Automatically formats a clean, 1-page markdown document and drafts a customized 75-word outreach message highlighting a specific JD-to-resume crossover.
* **Browser Automation:** Leverages DOM-reading extensions (Simplify Copilot) to map Master Resume EEOC data and autofill Workday/Greenhouse demographic fields.
