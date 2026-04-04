import ollama
import json
import time


# ================================
# RETRY HANDLER
# ================================
def safe_generate(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = ollama.chat(
                model="mistral",
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]

        except Exception as e:
            wait = 5 * (attempt + 1)
            print(f"Error. Retrying in {wait}s...")
            time.sleep(wait)

    return None


# ================================
# SAFE JSON PARSER
# ================================
def parse_json_safely(raw):
    if not raw:
        return {}

    raw = raw.strip()

    # remove markdown
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw

    try:
        data = json.loads(raw)

        # correct format
        if isinstance(data, dict) and "generated_email" in data:
            return data

        # weird format like {"Hi ..."}
        if isinstance(data, dict):
            val = list(data.values())[0]
            return {"generated_email": val}

    except:
        pass

    # fallback
    return {"generated_email": raw}


# ================================
# ENRICHMENT PROMPT
# ================================
def build_enrich_prompt(name, idea):
    return f"""
Analyze this startup deeply:

Name: {name}
Description: {idea}

Rules:
- Identify a SPECIFIC operational bottleneck
- Focus on workflows, scaling, internal friction
- Avoid generic statements
- Mention exact failure points in user flow or system behavior

Return ONLY valid JSON:
{{
  "pain_point": "...",
  "automation_idea": "..."
}}
"""


def enrich_lead(lead):
    try:
        prompt = build_enrich_prompt(lead["name"], lead["idea"])
        raw = safe_generate(prompt)

        if not raw:
            raise Exception("Empty response")

        raw = raw.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]

        result = json.loads(raw)

        return {
            "pain_point": result.get("pain_point", ""),
            "automation_idea": result.get("automation_idea", "")
        }

    except:
        return {
            "pain_point": "Ambiguity in user intent causes breakdowns in internal workflows as the system scales.",
            "automation_idea": "Introduce structured processing layers to standardize inputs before execution."
        }


# ================================
# EMAIL PROMPT
# ================================
def build_email_prompt(name, idea, pain_point, automation_idea):
    return f"""
You are writing a sharp, founder-level cold email.

Startup:
{name}

What they do:
{idea}

Pain point:
{pain_point}

Automation idea:
{automation_idea}

━━━━━━━━━━━━━━━━━━

STEP 0: Extract ONE concrete, real usage detail from the idea
(e.g. actual user query, workflow step, system action)

STEP 1: Turn that into a sharp observation
STEP 2: Identify where it breaks operationally
STEP 3: Suggest ONE precise automation fix

━━━━━━━━━━━━━━━━━━

STRICT RULES:
- 80–120 words
- Start with: Hi {name} Team
- First line MUST include a real example or mechanism
- Avoid generic words: platform, solution, system, tool
- No fluff

Return ONLY valid JSON:
{{
  "generated_email": "..."
}}
"""


# ================================
# QUALITY FILTERS
# ================================
def is_generic(text):
    generic_phrases = [
        "platform",
        "solution",
        "interesting",
        "great work",
        "i noticed",
        "this space",
        "your startup",
        "innovative",
        "cutting-edge"
    ]

    weak_openers = [
        "i came across",
        "i saw",
        "i found",
    ]

    text_lower = text.lower()

    return (
        any(p in text_lower for p in generic_phrases) or
        any(text_lower.startswith(w) for w in weak_openers)
    )


def lacks_specificity(text):
    vague_words = [
        "system",
        "process",
        "tool",
        "analytics",
        "dashboard",
        "management",
        "workflow"
    ]

    return any(word in text.lower() for word in vague_words)


# ================================
# EMAIL GENERATION
# ================================
def generate_email(lead):
    try:
        prompt = build_email_prompt(
            lead["name"],
            lead["idea"],
            lead.get("pain_point", ""),
            lead.get("automation_idea", "")
        )

        raw = safe_generate(prompt)

        if not raw:
            raise Exception("Empty response")

        result = parse_json_safely(raw)
        email = result.get("generated_email", "")

        # retry if weak
        if is_generic(email) or lacks_specificity(email):
            print("Retrying due to weak output...")

            prompt += "\n\nIMPORTANT: Be extremely specific. Use a real user action or system step."

            raw = safe_generate(prompt)
            result = parse_json_safely(raw)

        return result

    except Exception as e:
        print("Email error:", e)
        return {
            "generated_email": f"""Hi {lead.get('name', 'Team')},

Your workflow likely breaks at specific points as usage scales.

A strong improvement would be structuring inputs before they hit core systems.

Happy to share ideas if useful.

– Ayush"""
        }


# ================================
# MAIN PIPELINE
# ================================
def analyze_and_generate(lead):
    enriched = enrich_lead(lead)
    lead.update(enriched)

    email = generate_email(lead)
    lead.update(email)

    return lead