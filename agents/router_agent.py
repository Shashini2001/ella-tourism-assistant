import os
import json
from groq import Groq

ROUTER_MODEL = "llama-3.1-8b-instant"

VALID_CATEGORIES = ["attractions", "hotels", "transport", "culture", "general"]

SYSTEM_PROMPT = f"""You are a query routing and planning assistant for a Sri Lankan
tourism system focused on the Ella region. Given a traveler's question, you must:

1. Classify it into exactly one category from this list: {VALID_CATEGORIES}
   - "attractions": hikes, viewpoints, waterfalls, sightseeing spots
   - "hotels": accommodation, resorts, guesthouses, hostels
   - "transport": trains, buses, tuk-tuks, getting to/around Ella
   - "culture": food, etiquette, festivals, history, local customs
   - "general": anything that doesn't clearly fit the above, or spans multiple categories

2. Rewrite the question as a clear, standalone "refined_query" suitable for
   searching a knowledge base. Resolve vague pronouns and add implicit context
   about Ella, Sri Lanka where helpful, but keep it concise (one sentence).

Respond ONLY with valid JSON in this exact format, no extra text:
{{"category": "<one of {VALID_CATEGORIES}>", "refined_query": "<rewritten question>"}}
"""


class RouterAgent:
    def __init__(self, api_key: str | None = None):
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))

    def route(self, user_question: str) -> dict:
    
        response = self.client.chat.completions.create(
            model=ROUTER_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question},
            ],
            temperature=0.1,
            max_tokens=200,
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(raw)
            category = parsed.get("category", "general")
            if category not in VALID_CATEGORIES:
                category = "general"
            refined_query = parsed.get("refined_query", user_question)
        except (json.JSONDecodeError, AttributeError):
            category = "general"
            refined_query = user_question

        return {
            "original_question": user_question,
            "category": category,
            "refined_query": refined_query,
        }
