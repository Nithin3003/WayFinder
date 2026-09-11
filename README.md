# WayFinder | Universal Intent Bridge

WayFinder (Universal Intent Bridge Core) is an AI-driven platform that translates unstructured human goals into structured, actionable institutional action plans. It helps users navigate complex processes across government services, healthcare, social aid, and employment support.

---

## Key Features

* **Natural Goal Parsing:** Converts conversational user prompts into structured tasks, urgency scores, and summaries.
* **Deterministic Action Plans:** Categorizes steps into clear stages (`ELIGIBILITY`, `DOCUMENTATION`, `SUBMISSION`, `FOLLOW_UP`).
* **Document Tracking:** Highlights required documentation and missing critical information for each step.
* **Official Communication Generation:** Automatically drafts emails, letters, and forms needed for submission.
* **Gemini Core Integration with Fallback:** Uses `gemini-2.5-flash` for real-time natural language reasoning, with an offline simulation fallback engine for high availability.

---

## Tech Stack

* **Backend:** FastAPI, Python 3.10+, Pydantic, Uvicorn
* **AI Core:** Google Generative AI (`google-generativeai`)
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API)

<video src="https://github.com/Nithin3003/WayFinder/blob/main/Screen%20Recording%202026-09-11%20143437.mp4" controls="controls" style="max-width: 100%;">
</video>
