# 🚀 LeadForge AI

**Discover startups. Analyze their pain. Generate personalized cold emails. All locally.**

An intelligent B2B outreach automation tool powered by local LLMs.  
No paid APIs. No rate limits. No data sent to third parties.

---

## ⚙️ How It Works

Step-by-step:

1. Fetch startup profiles from public APIs (Crunchbase, etc.)
2. Clean and structure messy data
3. Analyze using a local LLM to find pain points & opportunities
4. Generate personalized cold emails instantly
5. Export results as CSV for your CRM or email tool

---

## 🏗️ Architecture

| Component     | Purpose |
|--------------|--------|
| Scraper      | Fetches startup data from public sources |
| Processor    | Cleans, validates, and structures data |
| AI Engine    | Local LLM analysis using Ollama + Mistral/Llama |
| Generator    | Creates personalized emails with context |
| UI           | Streamlit dashboard for interaction |
| Storage      | CSV export for CRM integration |

---

## 🚀 Quick Start

### 📦 Prerequisites

- Python 3.9+
- Ollama installed → https://ollama.com
- ~4GB RAM minimum

---

### 🛠️ Installation

```bash
# 1. Clone the repo
git clone https://github.com/Ayush-kr-007/leadforge-ai
cd leadforge-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Ollama with a model
ollama run mistral
# (or use llama3:8b for better quality if you have 8GB+ RAM)

# 4. Run the app
streamlit run app.py
```
---
### App will open at: http://localhost:8501

## 🧑‍💻 Usage
1. Click "Find Startups" → retrieves startup profiles
2. (Optional) Filter by industry, stage, location
3. Click "Generate Insights" → AI analyzes each startup
4. Review insights & generated emails
5. Export to CSV

---
📊 Example Output
STARTUP: Advaita Cybernetics Private Limited

🎯 PAIN POINT:
The primary operational bottleneck for Advaita Cybernetics Private Limited could be the complex and highly specialized nature of their flagship product, TrinetraAI. The development and optimization of a spiking neural network (SNN) architecture that accurately mirrors human brain functionality is an intricate process with many potential failure points. This includes the modeling of 86 billion neurons with spike-timing-dependent plasticity (STDP), hippocampal memory, spreading activation for domain routing, first-principles reasoning from typed axioms, and biological sleep cycles for memory consolidation and creative synthesis. The time-consuming and resource-intensive research and development required to perfect these components may lead to delays in product deployment and scalability issues.

💡 AUTOMATION IDEA:
To alleviate this operational bottleneck, Advaita Cybernetics could consider implementing an automated machine learning (AutoML) system for the optimization of their SNN architecture. By utilizing AutoML, they can automate the process of model selection, hyperparameter tuning, and neural network architecture design. This would significantly reduce the time and resources required to perfect each component of TrinetraAI, thereby expediting the development process, improving scalability, and potentially reducing internal friction.

📧 PERSONALIZED EMAIL:
---
Hi ADVAITA CYBERNETICS PRIVATE LIMITED Team,

Considering the intricate modeling of 86 billion neurons with spike-timing-dependent plasticity (STDP) in TrinetraAI, manual optimization is a time-consuming and resource-intensive process. This could lead to delays in product deployment and scalability issues.

To alleviate this operational bottleneck, we suggest implementing an automated machine learning (AutoML) system for optimizing the STDP modeling within your SNN architecture. AutoML can automate model selection, hyperparameter tuning, and neural network architecture design, significantly reducing time and resources required, thereby expediting development and improving scalability.
Best,  
Ayush
---

### 💡 What I Learned Building This
1. Local LLMs Have Trade-offs

✅ No API costs, full privacy, no rate limits
❌ Slower inference, less consistent output

*👉 Lesson: System design matters more than model choice

2. Prompt Engineering > Model Size
Good prompts > bigger models
Structured JSON outputs are unreliable locally

*👉 Lesson: Invest in prompt iteration

3. Caching & Batching Are Critical
Avoid re-processing the same startup
Batch for efficiency
Save everything
4. Real-World Data Is Messy
APIs have inconsistent schemas
Missing data is common

*👉 Lesson: Output quality depends on input quality

###⚙️ Configuration

Edit in config.py or via UI:

# LLM Model
LLM_MODEL = "mistral"  # or "llama3:8b"

# Data Sources
STARTUP_API = "https://api.crunchbase.com/..."

# Output Settings
EXPORT_FORMAT = "csv"
SAVE_DIR = "./outputs"

###⚠️ Limitations
Generic emails sometimes
Slower than cloud APIs (~2–5 sec/startup)
Output quality depends on data
JSON parsing may fail

*👉 Workaround: Regenerate or tweak prompts in ai_engine.py

###⚖️ Legal & Ethical Use
✅ Allowed
Educational use
Small-scale targeted outreach
Prototyping ideas
❌ Not Allowed
Mass spam
Data harvesting
Misleading communication
Violating laws (CAN-SPAM, GDPR, etc.)

###👉 You are responsible for compliance.

###🔐 Privacy & Security
100% local processing
No external API calls
No tracking or analytics
Fully open-source
###🛣️ Roadmap
Better personalization
Feedback loop for regeneration
Email editing UI
CRM integrations (Salesforce, HubSpot)
Batch processing
More data sources
A/B testing framework
*🤝 Contributing
Open an issue
Submit a PR
Share feedback

###🙋 FAQ

How accurate is the AI?
→ Good for ideas, not perfect emails

Can I use this commercially?
→ Yes, but follow local email laws

Emails sound generic?
→ Improve prompts or regenerate

Can I use another LLM?
→ Yes! Try llama3:8b, neural-chat, etc.


