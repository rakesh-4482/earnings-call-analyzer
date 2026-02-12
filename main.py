from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import PyPDF2
import io
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def analyze_transcript(text):
    text_lower = text.lower()

    positive_words = [
        "strong", "growth", "record", "improved",
        "robust", "confidence", "expansion",
        "positive", "momentum", "opportunity"
    ]

    negative_words = [
        "decline", "pressure", "challenge",
        "slowdown", "risk", "uncertainty",
        "headwinds", "weakness", "declined"
    ]

    guidance_keywords = [
        "guidance", "outlook", "forecast",
        "expect", "anticipate", "next quarter",
        "next year", "fy", "full year"
    ]

    growth_keywords = [
        "initiative", "launch", "expansion",
        "new product", "new market", "investment",
        "strategy", "rollout"
        ]
    
    capacity_keywords = [
        "capacity utilization",
        "utilization rate",
        "plant capacity",
        "facility capacity",
        "manufacturing capacity",
        "capacity expansion",
        "installed capacity"
    ]

    # 1️⃣ Split text into sentences FIRST
    sentences = re.split(r'[.\n!?]+', text)

    # 2️⃣ Score calculation
    positive_score = sum(text_lower.count(word) for word in positive_words)
    negative_score = sum(text_lower.count(word) for word in negative_words)

    # 3️⃣ Determine tone
    if positive_score > negative_score * 1.5:
        tone = "Optimistic"
    elif negative_score > positive_score * 1.5:
        tone = "Pessimistic"
    elif positive_score > negative_score:
        tone = "Cautious"
    else:
        tone = "Neutral"


    # 4️⃣ Determine confidence
    difference = abs(positive_score - negative_score)

    if difference > 10:
        confidence = "High"
    elif difference > 5:
        confidence = "Medium"
    else:
        confidence = "Low"

    # 5️⃣ Extract key positives
    key_positives = [
        s.strip() for s in sentences
        if len(s.strip()) > 40 and any(word in s.lower() for word in positive_words)
    ]

    # 6️⃣ Extract key concerns
    key_concerns = [
        s.strip() for s in sentences
        if len(s.strip()) > 40 and any(word in s.lower() for word in negative_words)
    ]

    # 7️⃣ Extract forward guidance
    forward_guidance = []
    for s in sentences:
        clean_s = s.strip()
        if len(clean_s) > 40:
            for word in guidance_keywords:
                if re.search(r'\b' + re.escape(word) + r'\b', clean_s.lower()):
                    forward_guidance.append(clean_s)
                    break
    
    growth_initiatives = []
    for s in sentences:
        clean_s = s.strip()
        if len(clean_s) > 40:
            for word in growth_keywords:
                if re.search(r'\b' + re.escape(word) + r'\b', clean_s.lower()):
                    growth_initiatives.append(clean_s)
                    break
    capacity_trends = []
    for s in sentences:
        clean_s = s.strip()
        if len(clean_s) > 40:
            for word in capacity_keywords:
                if re.search(r'\b' + re.escape(word) + r'\b', clean_s.lower()):
                    capacity_trends.append(clean_s)
                    break
    
    word_count = len(text.split())
    sentence_count = len(sentences)

    return {
        "tone": tone, 
        "confidence_level": confidence,
        "key_positives": key_positives[:5],
        "key_concerns": key_concerns[:5],
        "forward_guidance": forward_guidance[:5],
        "growth_initiatives": growth_initiatives[:5],
        "capacity_utilization_trends": capacity_trends[:5],
        "document_stats": {
            "word_count": word_count,
            "sentence_count": sentence_count
            }
        }



@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...)):

    # ✅ File type validation
    if not file.filename.lower().endswith(".pdf"):
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "results": {
                    "tone": "N/A",
                    "confidence_level": "N/A",
                    "key_positives": [],
                    "key_concerns": [],
                    "forward_guidance": [],
                    "growth_initiatives": [],
                    "capacity_utilization_trends": [],
                    "error": "Only PDF files are supported."
                }
            }
        )

    contents = await file.read()

    pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))

    full_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # ✅ Minimum length validation
    if len(full_text.strip()) < 500:
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "results": {
                    "tone": "Insufficient Data",
                    "confidence_level": "Low",
                    "key_positives": [],
                    "key_concerns": [],
                    "forward_guidance": [],
                    "growth_initiatives": [],
                    "capacity_utilization_trends": [],
                    "error": "Document too short for meaningful analysis."
                }
            }
        )

    results = analyze_transcript(full_text)

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "results": results
        }
    )


