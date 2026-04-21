# Underwriting Exception Explainer

An agentic pipeline that translates mortgage lender decline reason codes into plain-language broker action plans.

---

## The Problem

When a lender declines a mortgage application, the broker receives a list of reason codes. Technical. Dense. Lender-specific. No translation. No action plan.

A broker stares at `GDS ratio 36.8% exceeds B-20 guideline` and has to figure out on their own what that means, what regulation it violates, who needs to do what, and by when.

That interpretation loop is entirely manual. It can take days. And during those days, deals die.

---

## How It Works

A 3-node agentic pipeline built to close the interpretation gap between a lender decision and a broker's next action.

```
[ Raw Lender Reason Codes ]
           |
           v
  Node 1: Parse Exception
  Structures raw reason codes into
  labelled findings with severity tags
  (hard stop / fixable / monitor)
           |
           v
  Node 2: Cross-Reference B-20
  Maps each finding to the relevant
  OSFI B-20 guideline or lender policy
  Adds plain-language explanation
           |
           v
  Node 3: Broker Action Plan
  Generates prioritized actions with
  owner, timeline, and resubmission
  likelihood score
           |
           v
  [ Structured Output ]
  Summary + Findings + Action Plan + KPI estimate
```

---

## Demo

**Input — raw lender decline notes**

![Input screenshot](screenshots/input.png)

**Output — structured exception analysis**

![Output screenshot](screenshots/output.png)

---

## Sample Output

Given a Scotia Mortgage Authority decline with 6 reason codes, the pipeline produces:

- Plain-language summary of why the file was declined
- Each finding mapped to its B-20 section or lender policy
- Severity classification per finding (hard stop / fixable / monitor)
- Broker tip for each finding, specific and actionable
- Prioritized action plan with owner and timeline
- Resubmission likelihood score
- KPI impact estimate: touchpoints saved, days saved, resubmit rate lift

**Notable finding from the demo case:** the pipeline surfaced an undisclosed student loan liability that the broker had missed on the original application, the exact issue that pushed TDS over the 44% limit and caused the decline.

---

## Tech Stack

- Claude (claude.ai) — pipeline execution and reasoning
- HTML / CSS / JavaScript — front-end display layer
- Anthropic API — no separate backend required
- No additional dependencies or build steps

---

## Constraints and Honest Notes

This is a prototype built as a PM learning exercise, not a production system.

- KPI numbers shown in the output are directional hypotheses, not validated data
- B-20 cross-referencing is AI-generated and should be verified against official OSFI documentation before any production use
- A production version would need real broker workflow instrumentation to validate time and touchpoint savings
- Running the HTML file locally requires an Anthropic API key at console.anthropic.com

---

## What I Would Instrument Next

If this went further, the success metrics I would track:

- Broker touchpoints per declined file before clean resubmission
- Time from decline notification to resubmission
- Resubmission conversion rate (declined to funded)
- Broker-reported confidence score after using the tool vs without

---

## The Honest Reflection

Claude built the implementation. I built the problem framing, the node architecture, the output schema, the use case targeting, and the product hypothesis.

That distinction is increasingly what PM work looks like.

---

## Author

Built by [Your Name](https://www.linkedin.com/in/yourprofile)

---

*Exploring the intersection of AI and financial services workflows.*
