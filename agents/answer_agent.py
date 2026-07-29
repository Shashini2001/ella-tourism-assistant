import os
from openai import OpenAI

from rag.retriever import retrieve

ANSWER_MODEL = "openai/gpt-4o-mini" 

DRAFT_SYSTEM_PROMPT = """You are a knowledgeable local travel assistant for the Ella
region of Sri Lanka. Answer the traveler's question using ONLY the provided context
chunks. If the context does not contain enough information to answer confidently,
say so plainly rather than inventing details. Keep answers practical and concise,
and mention specific tips (timing, cost, access) when the context provides them.
"""

REFLECTION_SYSTEM_PROMPT = """You are a careful editor reviewing a draft answer about
travel in the Ella region of Sri Lanka. Compare the DRAFT ANSWER against the SOURCE
CONTEXT it was supposed to be based on. Check for:
1. Any claim in the draft NOT supported by the source context (hallucination)
2. Missing useful details that ARE in the source context but were left out
3. Unclear or overly verbose phrasing

Then rewrite the answer as a corrected FINAL ANSWER that is accurate, grounded
strictly in the source context, and clear. Respond with ONLY the final answer text,
no commentary about the review process itself.
"""


class AnswerAgent:
    def __init__(self, api_key: str | None = None):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or os.environ.get("OPENROUTER_API_KEY"),
        )

    def _call_model(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=ANSWER_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()

    def answer(self, router_output: dict) -> dict:

        category = router_output["category"]
        query = router_output["refined_query"]

        search_category = None if category == "general" else category
        chunks = retrieve(query, category=search_category, k=4)

        if not chunks:
            chunks = retrieve(query, category=None, k=4)

        context_text = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in chunks
        )

        if not chunks:
            return {
                "answer": (
                    "I don't have verified information on that in my current "
                    "knowledge base. You may want to check official Sri Lanka "
                    "Tourism resources or ask a local guide directly."
                ),
                "sources": [],
                "category": category,
            }

        draft_prompt = f"Question: {query}\n\nContext:\n{context_text}"
        draft = self._call_model(DRAFT_SYSTEM_PROMPT, draft_prompt)

        reflection_prompt = (
            f"SOURCE CONTEXT:\n{context_text}\n\n"
            f"DRAFT ANSWER:\n{draft}\n\n"
            f"Please review and provide the corrected FINAL ANSWER."
        )
        final_answer = self._call_model(REFLECTION_SYSTEM_PROMPT, reflection_prompt)

        return {
            "answer": final_answer,
            "draft_answer": draft,  
            "sources": chunks,
            "category": category,
        }
