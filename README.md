# Earnings Call Structured Analyzer

## Live Demo
https://earnings-call-analyzer-8qug.onrender.com

(Note: Hosted on Render free tier. First request may take ~30–60 seconds due to cold start.)

---

## Overview

This project implements a minimal internal research portal slice where AI is used as a structured research tool rather than an open-ended chatbot.

The system processes uploaded earnings call transcripts and produces analyst-ready structured insights.

---

## System Flow

1. User uploads a PDF transcript
2. Backend extracts text using PyPDF2
3. Text is split into sentences
4. Deterministic keyword-based scoring is applied
5. Structured insights are generated
6. Results are displayed in a clean UI

---

## Extracted Insights

- Management Tone (Optimistic / Cautious / Neutral / Pessimistic)
- Confidence Level (High / Medium / Low)
- Key Positives
- Key Concerns
- Forward Guidance
- Growth Initiatives
- Capacity Utilization Trends
- Document Statistics (word & sentence count)

---

## Design Philosophy

This implementation intentionally avoids open-ended generative AI to ensure:

- Deterministic behavior
- No hallucination
- Traceable logic
- Analyst reliability

Whole-word regex matching is used to prevent substring false positives.

Sentence-length filtering is applied to remove noise.

---

## Key Engineering Decisions

- Deterministic rule-based extraction over generative summarization
- Lightweight dependency stack for deployment stability
- Input validation for file type and document length
- Structured HTML output instead of raw JSON
- Public deployment on Render

---

## Limitations

- Rule-based logic may miss nuanced sentiment
- Does not yet differentiate prepared remarks vs Q&A
- Currently supports PDF only

---

## Future Improvements

- Add semantic sentiment model with guardrails
- Multi-document support
- Export to Excel
- Transcript section classification
- Dashboard scoring visualization
