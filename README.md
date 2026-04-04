# 🚀 LeadForge AI

**Discover startups. Analyze their pain. Generate personalized cold emails — all locally.**

An intelligent B2B outreach automation tool powered by local LLMs.  
No paid APIs. No rate limits. No data sent to third parties.

---

## ⚙️ How It Works

1. Fetch startup profiles from public APIs (e.g., Crunchbase)  
2. Clean and structure messy data  
3. Analyze using a local LLM to find pain points & opportunities  
4. Generate personalized cold emails instantly  
5. Export results as CSV for your CRM or email tool  

---

## 🧠 Why This Exists

Most outreach tools:
- rely on expensive APIs
- generate generic templates
- don’t actually understand the business

LeadForge AI is different:
- runs fully locally (zero cost)
- analyzes each startup before generating emails
- focuses on signal, not spam

---
## 🏗️ Architecture

| Component  | Purpose |
|-----------|--------|
| Scraper   | Fetches startup data from public sources |
| Processor | Cleans, validates, and structures data |
| AI Engine | Local LLM analysis using Ollama + Mistral/Llama |
| Generator | Creates personalized emails with context |
| UI        | Streamlit dashboard for interaction |
| Storage   | CSV export for CRM integration |

---

## 🚀 Quick Start

### 📦 Prerequisites

- Python 3.9+
- Ollama installed → https://ollama.com  
- ~4GB RAM minimum  

---

### 🛠️ Installation

    # 1. Clone the repo
    git clone https://github.com/Ayush-kr-007/leadforge-ai
    cd leadforge-ai

    # 2. Install dependencies
    pip install -r requirements.txt

    # 3. Start Ollama with a model
    ollama run mistral
    # OR (better quality if you have 8GB+ RAM)
    # ollama run llama3:8b

    # 4. Run the app
    streamlit run app.py

---

### 🌐 App URL
http://localhost:8501

---

## 🧑‍💻 Usage

1. Click **"Find Startups"** → retrieves startup profiles  
2. (Optional) Filter by industry, stage, location  
3. Click **"Generate Insights"** → AI analyzes each startup  
4. Review insights & generated emails  
5. Export to CSV  

---

## 📊 Example Output

**STARTUP:** Advaita Cybernetics Private Limited  

<img width="1916" height="705" alt="image" src="https://github.com/user-attachments/assets/56f64ffc-4641-4ce0-8411-1ecb50b1eb49" />


### 📧 Personalized Email

    Hi ADVAITA CYBERNETICS PRIVATE LIMITED Team,

    Considering the intricate modeling of 86 billion neurons with spike-timing-dependent plasticity (STDP) in TrinetraAI, manual optimization is a time-consuming and resource-intensive process. This could lead to delays in product deployment and scalability issues.
    
    To alleviate this operational bottleneck, we suggest implementing an automated machine learning (AutoML) system for optimizing the STDP modeling within your SNN architecture. AutoML can automate model selection, hyperparameter tuning, and neural network architecture design, significantly reducing time and resources required, thereby expediting development and improving scalability.

    Best,  
    Ayush

---

## 💡 What I Learned Building This

### 1. Local LLMs Have Trade-offs
- No API costs, full privacy, no rate limits  
- Slower inference, less consistent output  

👉 Lesson: System design matters more than model size  

---

### 2. Prompt Engineering > Model Size
- Good prompts outperform bigger models  
- Structured JSON outputs are unreliable locally  

👉 Lesson: Invest heavily in prompt design  

---

### 3. Caching & Batching Are Critical
- Avoid re-processing the same startup  
- Batch requests for efficiency  
- Persist outputs  

---

### 4. Real-World Data Is Messy
- APIs have inconsistent schemas  
- Missing data is common  

👉 Lesson: Output quality depends on input quality  

---

## ⚙️ Configuration

Edit in `config.py` or via UI:

    # LLM Model
    LLM_MODEL = "mistral"  # or "llama3:8b"

    # Data Source
    STARTUP_API = "https://api.crunchbase.com/..."

    # Output Settings
    EXPORT_FORMAT = "csv"
    SAVE_DIR = "./outputs"

---

## ⚠️ Limitations

- Emails may sound generic  
- Slower than cloud APIs (~2–5 sec/startup)  
- Output quality depends on data quality  
- JSON parsing may fail  

👉 Workaround: Regenerate or tweak prompts in `ai_engine.py`  

---

## ⚖️ Legal & Ethical Use

### ✅ Allowed
- Educational use  
- Small-scale targeted outreach  
- Prototyping ideas  

### ❌ Not Allowed
- Mass spam  
- Data harvesting  
- Misleading communication  
- Violating laws (CAN-SPAM, GDPR, etc.)  

👉 You are responsible for compliance.

---

## 🔐 Privacy & Security

- 100% local processing  
- No external API calls  
- No tracking or analytics  
- Fully open-source  

---

## 🛣️ Roadmap

- Better personalization  
- Feedback loop for regeneration  
- Email editing UI  
- CRM integrations (Salesforce, HubSpot)  
- Batch processing improvements  
- More data sources  
- A/B testing framework  

---

## 🤝 Contributing

- Open an issue  
- Submit a PR  
- Share feedback  

---

## 🙋 FAQ

**Q: How accurate is the AI?**  
→ Good for ideas, not perfect emails  

**Q: Can I use this commercially?**  
→ Yes, but follow local email laws  

**Q: Emails sound generic?**  
→ Improve prompts or regenerate  

**Q: Can I use another LLM?**  
→ Yes! Try llama3:8b, neural-chat, etc.  
