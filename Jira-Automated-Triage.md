# AI Agent: Automated Jira Ticket Triage 

## The Problem
In complex financial portals like Equity Plans Manager (E*Trade, Shareworks), engineering and product teams lose valuable sprint capacity manually triaging support tickets. This "triage trap" drains engineering velocity as teams waste hours investigating whether an issue is a genuinely broken feature, a missing requirement, or simply a user knowledge gap.

## The Solution
An AI-agentic workflow built to intercept incoming Jira tickets, cross-reference the user's complaint against the Product Requirements Document (PRD), and definitively categorize the root cause before it reaches the engineering backlog.

## System Architecture (Gumloop & Atlassian API Integration)
This POC operates entirely via a two-way Atlassian API integration, eliminating manual data entry.
1. **Trigger & Extraction:** A Jira Issue Reader node continuously monitors a live Service Management board, extracting raw ticket descriptions and system Issue Keys.
2. **Data Context:** A static node holds the immutable Product Requirements Document (PRD) rules for RSU Vesting.
3. **Logic Engine (LLM):** The AI processes the batch of tickets, explicitly auditing the user's text against the PRD using deterministic logic to prevent hallucination.
4. **Automated Write-Back:** The system leverages the extracted Issue Keys to dynamically route the AI's categorization and justification back to the live Atlassian board as an internal ticket comment.

## Mock Data Context: RSU Vesting PRD
> **Rule 1: Balance Updates:** Upon an RSU vest date, the participant's "Available to Trade" share balance must automatically update within 24 hours of market open.
> **Rule 2: Tax Withholding Methods:** The platform ONLY supports "Net Settlement" (Sell-to-Cover) for tax withholding. Cash payments via linked bank accounts are not supported.
> **Rule 3: Estimated vs. Actual Taxes:** The portal displays an Estimated Tax Withholding using a flat 22% rate. Actual taxes may fluctuate based on FMV at the time of the transaction.

## Core System Prompt (Anti-Hallucination)
> You are a Strategic Technical Product Manager. Review the provided Jira ticket against the attached PRD. 
> 
> CRITICAL CONSTRAINTS - DO NOT HALLUCINATE:
> * You must rely strictly and exclusively on the text provided in the PRD. 
> * Do not invent business rules or assume external system behaviors. 
> * If the ticket references a feature not mentioned in the PRD, you must treat it as a Requirement Gap.
> 
> Categorize the root cause of the ticket into ONLY ONE of the following three buckets:
> 1. Tech Bug (System is failing to execute a defined PRD rule).
> 2. Requirement Gap (System is working as designed, but the user is requesting a feature explicitly not supported by the PRD).
> 3. Knowledge Gap (System is working as designed, but the user misunderstands the expected behavior outlined in the PRD).
> 
> Output the category in bold, followed by a one-sentence explanation of your reasoning referencing a specific PRD rule.

## Market Differentiation: Engineering Backlog Defense vs. Customer Deflection
While major ITSM platforms (like Atlassian Intelligence and Zendesk AI) now feature powerful native AI, their native agents are fundamentally optimized for *customer deflection*—reading knowledge bases to answer user "how-to" questions. 

This agentic flow introduces a dedicated **Engineering Backlog Defense**. Instead of simply answering the user, this architecture explicitly audits the user's technical complaint against an isolated, immutable source of truth (the PRD). It logically proves whether the system is experiencing a technical failure, a scoped limitation, or a user education gap. This strictly guards engineering sprint capacity, preventing functioning code from being falsely flagged as a bug.
