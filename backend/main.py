import os
import json
import re
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Initialize FastAPI App
app = FastAPI(
    title="Universal Intent Bridge Core",
    description="Translating unstructured human goals into complex institutional actions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IntentRequest(BaseModel):
    user_input: str
    user_context: Optional[dict] = None

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
gemini_available = False

if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_available = True
    except Exception as e:
        print(f"[IntentBridge] Gemini SDK init note: {e}")

SYSTEM_PROMPT = """You are the reasoning core of "Universal Intent Bridge", an AI system designed to act as a universal intermediary between citizen goals and complex institutional frameworks (Government, Healthcare, Social Services, Employment, Financial Aid).

YOUR CORE RESPONSIBILITIES:
1. Extract the core goal, constraints, missing information, and urgency level from unstructured human input.
2. Determine eligibility requirements and appropriate institutional pathways.
3. Formulate an adaptive step-by-step action plan using a structured state engine (Tasks: Discovered -> Eligible -> Documents Ready -> Applied -> Completed).
4. Translate institutional jargon into clear, plain language instructions.
5. Generate deterministic JSON payloads for downstream system integration and UI rendering.

CRITICAL SAFETY & TRUTH RULES:
- Never fabricate official government policies or legal criteria.
- Clearly separate verified facts from AI-generated guidance.
- Require explicit user confirmation before any consequential action (e.g., submitting an application).

REQUIRED OUTPUT FORMAT (STRICT JSON ONLY, NO MARKDOWN, NO EXPLANATION CODEBLOCKS):
{
  "intent_summary": "Concise statement of what the user wants to accomplish",
  "urgency": "LOW | MEDIUM | HIGH | CRITICAL",
  "missing_critical_info": ["Item 1 needed to proceed", "Item 2 needed to proceed"],
  "action_plan": [
    {
      "id": "task_1",
      "title": "Action title",
      "category": "ELIGIBILITY | DOCUMENTATION | SUBMISSION | FOLLOW_UP",
      "status": "COMPLETED | IN_PROGRESS | BLOCKED | NEEDS_INFO",
      "plain_explanation": "Simple explanation of what this step does",
      "required_documents": ["Doc A", "Doc B"]
    }
  ],
  "generated_artifacts": {
    "draft_email_or_letter": "Pre-filled text or script for official communications",
    "checklist": ["Step 1", "Step 2"]
  },
  "followup_question": "Direct, empathetic question asking for missing information"
}
"""

def simulate_bridge_intent(user_input: str) -> Dict[str, Any]:
    """Fallback simulation engine for bulletproof demo performance."""
    inp_lower = user_input.lower()

    if any(k in inp_lower for k in ["job", "unemployment", "resume", "layoff", "fired", "work"]):
        summary = "File for state unemployment benefits, update professional resume, and register for government job transition support."
        urgency = "HIGH"
        missing = ["Date of last employment", "Employer separation notice or termination letter"]
        action_plan = [
            {
                "id": "task_1",
                "title": "Verify State Unemployment Insurance (UI) Eligibility",
                "category": "ELIGIBILITY",
                "status": "COMPLETED",
                "plain_explanation": "Check if your earnings over the past 4 quarters meet the minimum wage baseline for state UI.",
                "required_documents": ["Pay Stubs (Last 3 months)", "W-2 / Tax Returns"]
            },
            {
                "id": "task_2",
                "title": "Gather Official Employment Separation Documents",
                "category": "DOCUMENTATION",
                "status": "NEEDS_INFO",
                "plain_explanation": "Obtain your official separation letter or severance agreement from your employer.",
                "required_documents": ["Employer Termination Notice", "Government ID"]
            },
            {
                "id": "task_3",
                "title": "Submit State UI Claim on Citizen Portal",
                "category": "SUBMISSION",
                "status": "IN_PROGRESS",
                "plain_explanation": "Draft and submit your online claim to trigger weekly benefit payments.",
                "required_documents": ["Direct Deposit Bank Details"]
            },
            {
                "id": "task_4",
                "title": "Enroll in Public Career Transition & Training Allowance",
                "category": "FOLLOW_UP",
                "status": "BLOCKED",
                "plain_explanation": "Register with local workforce development for free skill re-training subsidies.",
                "required_documents": ["Proof of UI Claim Registration"]
            }
        ]
        draft_letter = "To: State Department of Labor Triage Office\nSubject: Urgent Claim Application - Unemployment Insurance & Job Transition\n\nDear Officer,\n\nI am writing to initiate my application for Unemployment Insurance benefits following my recent separation from employment. Attached are my proof of identity and income statements. Please confirm the receipt of my claim.\n\nSincerely,\n[Citizen Name]"
        checklist = ["File UI claim on portal", "Upload pay stubs", "Set up direct deposit", "Attend mandatory career orientation"]
        followup = "Could you please confirm the exact date of your last working day and whether you received an official separation letter?"

    elif any(k in inp_lower for k in ["elderly", "mother", "father", "senior", "medicare", "prescription", "health", "pension"]):
        summary = "Access senior public healthcare registry, prescription subsidies, and elder care assistance programs."
        urgency = "MEDIUM"
        missing = ["Senior Citizen ID / Aadhar Number", "Current monthly prescription list"]
        action_plan = [
            {
                "id": "task_1",
                "title": "Verify Senior Health Insurance & Subsidy Tier",
                "category": "ELIGIBILITY",
                "status": "COMPLETED",
                "plain_explanation": "Determine eligibility for 100% covered geriatric healthcare and medication subsidies.",
                "required_documents": ["Senior Citizen ID Card", "Proof of Age (70+)"]
            },
            {
                "id": "task_2",
                "title": "Compile Doctor Prescription & Medical History",
                "category": "DOCUMENTATION",
                "status": "IN_PROGRESS",
                "plain_explanation": "Gather current doctor prescriptions to register for free monthly pharmacy home delivery.",
                "required_documents": ["Registered Doctor Prescriptions", "Hospital Diagnostic Reports"]
            },
            {
                "id": "task_3",
                "title": "Submit Senior Wellness & Pharmacy Subsidy Application",
                "category": "SUBMISSION",
                "status": "IN_PROGRESS",
                "plain_explanation": "Submit application to the Public Health Department's Senior Welfare wing.",
                "required_documents": ["Bank Account Details for Subsidy Transfer"]
            }
        ]
        draft_letter = "To: Public Health Department - Senior Welfare Division\nSubject: Enrollment Request - Senior Healthcare & Prescription Subsidy Program\n\nRespected Sir/Madam,\n\nI am requesting senior citizen healthcare benefits and prescription coverage for my mother (Age 78). Attached are her age proof and medical records.\n\nThank you,\n[Applicant Name]"
        checklist = ["Gather age proof document", "Compile pharmacy prescriptions", "Submit online healthcare card form"]
        followup = "Does your mother already hold a government senior citizen card or primary health ID number?"

    elif any(k in inp_lower for k in ["rent", "housing", "eviction", "landlord", "shelter"]):
        summary = "Apply for emergency rental assistance and temporary eviction stay via Municipal Housing Board."
        urgency = "CRITICAL"
        missing = ["Formal eviction notice or landlord demand letter", "Lease agreement copy"]
        action_plan = [
            {
                "id": "task_1",
                "title": "File Emergency Notice of Hardship with Housing Board",
                "category": "ELIGIBILITY",
                "status": "COMPLETED",
                "plain_explanation": "Initiate an emergency stay against eviction due to temporary medical debt hardship.",
                "required_documents": ["Lease Agreement", "Notice from Landlord"]
            },
            {
                "id": "task_2",
                "title": "Gather Unpaid Rent Statement & Medical Debt Proof",
                "category": "DOCUMENTATION",
                "status": "IN_PROGRESS",
                "plain_explanation": "Provide evidence showing unexpected medical expenses causing temporary rent shortfall.",
                "required_documents": ["Medical Bills", "Bank Account Statement"]
            },
            {
                "id": "task_3",
                "title": "Direct Disbursement to Landlord via Housing Stabilization Fund",
                "category": "SUBMISSION",
                "status": "BLOCKED",
                "plain_explanation": "Submit direct landlord payment authorization to resolve rent arrears.",
                "required_documents": ["Landlord W-9 / Tax ID Form"]
            }
        ]
        draft_letter = "To: Municipal Emergency Housing Committee\nSubject: URGENT: Emergency Rental Assistance & Hardship Stay Request\n\nDear Housing Commissioner,\n\nI am filing for emergency rental assistance under the Housing Stabilization Fund to prevent immediate eviction due to unforeseen medical debt.\n\nSincerely,\n[Tenant Name]"
        checklist = ["File emergency stay petition", "Submit medical debt bills", "Get landlord W-9 information"]
        followup = "Has your landlord served a formal written notice to quit or filed a court case?"

    else:
        summary = f"Process citizen intent: '{user_input[:80]}...'"
        urgency = "MEDIUM"
        missing = ["Specific location or municipality", "Supporting document copy"]
        action_plan = [
            {
                "id": "task_1",
                "title": "Identify Institutional Pathway & Requirements",
                "category": "ELIGIBILITY",
                "status": "COMPLETED",
                "plain_explanation": "Analyze public department rules and eligibility criteria.",
                "required_documents": ["Government Identity Card"]
            },
            {
                "id": "task_2",
                "title": "Prepare Supporting Documentation Package",
                "category": "DOCUMENTATION",
                "status": "IN_PROGRESS",
                "plain_explanation": "Format and verify all necessary certificates and application forms.",
                "required_documents": ["Proof of Residence", "Income Certificate"]
            },
            {
                "id": "task_3",
                "title": "Execute Formal Application Submission",
                "category": "SUBMISSION",
                "status": "NEEDS_INFO",
                "plain_explanation": "File application through official portal or dispatch officer.",
                "required_documents": ["Signed Declaration Form"]
            }
        ]
        draft_letter = "To: Institutional Customer Service Desk\nSubject: Official Application & Inquiry\n\nDear Team,\n\nI am submitting a request regarding my citizen service application. Please find attached the necessary documentation.\n\nSincerely,\n[Citizen Name]"
        checklist = ["Verify institutional portal", "Collect identity documents", "Submit online ticket"]
        followup = "Could you provide additional context or specify which government department or city this request is for?"

    return {
        "intent_summary": summary,
        "urgency": urgency,
        "missing_critical_info": missing,
        "action_plan": action_plan,
        "generated_artifacts": {
            "draft_email_or_letter": draft_letter,
            "checklist": checklist
        },
        "followup_question": followup
    }

@app.get("/api/v1/bridge/health")
async def health_check():
    return {
        "status": "ONLINE",
        "service": "Universal Intent Bridge Core v1.0",
        "gemini_sdk_active": gemini_available,
        "mode": "GEMINI_LIVE" if gemini_available else "HIGH_FIDELITY_SIMULATION"
    }

@app.post("/api/v1/bridge/intent")
async def parse_intent(request: IntentRequest):
    try:
        if not request.user_input or not request.user_input.strip():
            raise HTTPException(status_code=400, detail="User input cannot be empty.")

        structured_output = None

        if gemini_available:
            try:
                import google.generativeai as genai
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                System Rules:
                {SYSTEM_PROMPT}

                User Input:
                "{request.user_input}"

                Existing Context:
                {json.dumps(request.user_context or {})}

                Analyze the input, determine the goal, generate an action plan, identify missing information, and produce strict JSON.
                """

                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json", "temperature": 0.2}
                )

                clean_text = response.text.strip()
                if clean_text.startswith("```json"):
                    clean_text = re.sub(r"^```json\s*", "", clean_text)
                    clean_text = re.sub(r"\s*```$", "", clean_text)

                structured_output = json.loads(clean_text)
            except Exception as g_err:
                print(f"[IntentBridge] Gemini call warning: {g_err}. Using simulation engine fallback.")
                structured_output = None

        if not structured_output:
            structured_output = simulate_bridge_intent(request.user_input)

        return {
            "status": "success",
            "data": structured_output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static web files if index.html exists in project root or parent
static_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if os.path.exists(os.path.join(static_root, "index.html")):
    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(static_root, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
