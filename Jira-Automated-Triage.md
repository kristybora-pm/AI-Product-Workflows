# AI Agent: Automated Jira Ticket Triage 

## The Problem
In complex financial portals like Equity Plans Manager (E*Trade,Shareworks), engineering & product teams lose valuable sprint capacity manually triaging support tickets to determine if an issue is a broken feature, a missing requirement, or a user knowledge gap.

## The Solution
An AI-agentic workflow built to intercept incoming Jira tickets, cross-reference the user's complaint against the Product Requirements Document (PRD), and definitively categorize the root cause before it reaches the engineering backlog.

## System Architecture (Gumloop)
1. **Trigger:** Jira Issue Reader pulls new ticket descriptions.
2. **Data Lake:** Document Reader ingests the specific PRD (e.g., RSU Vesting & Tax Withholding rules).
3. **Logic Engine (LLM):** Compares the ticket explicitly against the PRD.
4. **Action:** Categorizes as `Tech Bug`, `Requirement Gap`, or `Knowledge Gap` and updates the ticket.

## Core System Prompt (Anti-Hallucination)
"You are a Strategic Technical Product Manager. Review the provided Jira ticket against the attached PRD. 
CRITICAL CONSTRAINTS: You must rely strictly and exclusively on the text provided in the PRD. Do not invent business rules or assume external system behaviors. If the ticket references a feature not mentioned in the PRD, you must treat it as a Requirement Gap..."
