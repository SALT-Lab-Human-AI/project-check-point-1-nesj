# 🧠 Carely — AI Companion for Elderly Care
 
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/e0f9324b4595c8e0fcc0ebb17bc47ad0a5d5745a/Logo.png" alt="Carely Logo" width="300"/>
</p>


> [CarelyAI Checkpoint 4 Presentation Link](https://docs.google.com/presentation/d/1X4oD7xJF3b4pqJkYbaCJkRoW8yDsamfF/edit?usp=sharing&ouid=111228501674454550833&rtpof=true&sd=true)
>
> [CarelyAI App Link](https://carely-final.streamlit.app/)

> **By: Nivedita Bharti, Jasmitha Duvvuru, Emmima Gnanaraj, Srivalli Lanka**

> **Carely** is an empathetic, AI-powered companion designed to assist elderly individuals with **daily health routines, medication reminders, emotional support, and caregiver coordination.**  
> Built with privacy, simplicity, and reliability at its core — Carely combines **LLM-based dialogue, structured scheduling, and memory-aware personalization** into one seamless experience.
 
---
 
## 🌟 Project Overview
 

It integrates an **AI companion** that interacts naturally with older adults while offering a **portal system** to monitor health trends and notify caregivers via alerts in case of emergency detection.
 
### **Core Objectives**
- Deliver **empathetic and safe** conversational support for seniors  
- Automate **medication reminders**, **wellness check-ins**, and **alert handling**  
- Enable caregivers to **track trends** and receive real-time emergency notifications  
- Build an extensible, privacy-preserving, low-cost architecture using open tools
 
---
 
## 🧩 System Architecture
 
### **Frontend**
 
| Component | Description |
|------------|-------------|
| **Framework** | Streamlit — enables rapid UI prototyping |
| **Portal** | portal design (Patient) |
| **Session State** | Streamlit’s built-in session for authentication & persistence |
| **Visualization** | Plotly charts for medication adherence & sentiment trends |
| **Voice Input** | Speech-to-text via `streamlit-mic-recorder` |
| **Accessibility** | Simple, clear language; one-click quick-action buttons |
 
 
---
 
### **Backend**
 
| Layer | Component / Design Choice |
|--------|----------------------------|
| **Framework** | FastAPI — lightweight REST API for backend services |
| **AI Engine** | Groq API using `Llama--3.3-70b-versatile` |
| **Central Agent** | `CompanionAgent` orchestrates all LLM calls, sentiment/emergency detection, and memory updates |
| **Scheduler** | `APScheduler` manages reminders, daily summaries, and alerts |
| **Authentication** | SHA-256 hashed credentials with role-based access control |
| **Architecture Pattern** | Modular CRUD design for separation of concerns |
| **Memory Management** | Multi-layer memory system (see below) |
 
---
 
### 🧠 **Multi-Layer Memory System**
 
| Type | Purpose | Storage |
|------|----------|----------|
| **Short-Term Memory** | Retrieves last 10 chat exchanges for contextual continuity | SQLite |
| **Long-Term Memory** | Semantic recall of older chats | ChromaDB (all-MiniLM-L6-v2 embeddings) |
| **Episodic Memory** | Daily summaries auto-generated at 11:59 PM CT | ChromaDB |
| **Structured Memory** | User profiles, medication schedules, and events | SQLite tables |
| **Scheduler Layer** | Automates periodic updates and context refresh | APScheduler |
 
**Why This Design:**  
Combines structured and semantic recall — enabling contextual, personalized chat without relying on costly external APIs.  
Episodic summaries allow day-to-day continuity similar to human memory.
 
---
 
### 📊 **Data & Storage Design**
 
| Component | Description |
|------------|-------------|
| **Database Engine** | SQLite (lightweight, zero-config) |
| **ORM** | SQLModel (Pydantic-based type safety) |
| **Entities** | User, Medication, Reminder, Conversation, PersonalEvent, CaregiverAlert |
| **Relationships** | `CaregiverPatientAssignment` links caregiver ↔ patient |
| **JSON Fields** | Store flexible metadata (preferences, schedules) |
| **Vector DB** | ChromaDB for semantic embedding retrieval |
| **Local Storage** | All data self-contained; no cloud dependency |
 
---
 
### 🧠 **LLM Model and Configuration**
 
| Attribute | Details |
|------------|----------|
| **Model** | **Groq API — Llama-3.3-70b-versatile** |
| **Integration** | `CompanionAgent` orchestrates all AI calls |
| **Prompting Strategy** | Elderly-friendly tone, empathetic phrasing, ≤4 sentences (≤230 tokens) per response |
| **Fine-Tuning** | None (prompt engineering only) |
| **Why Llama-3.3?** | Open-weights, low latency, cost-free for prototyping |
| **Why Groq?** | Hardware-accelerated inference delivering real-time responses |
 
 
---
 
### 🧰 **AI & Analytics Components**
 
| Module | Functionality |
|---------|----------------|
| **Conversation AI** | Uses Groq’s Llama-3.3-70b-versatile with system prompts optimized for elderly-friendly tone and brevity |
| **Sentiment Analysis** | Local keyword-based classifier; identifies emotion (positive/neutral/negative) |
| **Emergency Detection** | Local rule-based trigger detecting high/medium/low severity emergencies |
| **Safety Sheet** | Interactive UI flow for emergency confirmation and escalation |
| **Semantic Retrieval** | Vector similarity search in ChromaDB for contextual grounding |
| **Voice Output** | gTTS (Google Text-to-Speech) for optional voice replies |
 
---
 
### 🔔 **Notifications & Alerts**
 
| Feature | Implementation |
|----------|----------------|
| **Emergency Alerts** | Triggered automatically by emergency detection module |
| **Notification Channel** | Telegram bot integration (`TELEGRAM_BOT_TOKEN`) |
| **Alert Storage** | `CaregiverAlert` table maintains log history |
| **Reminders** | Scheduled via APScheduler |
| **Fail-Safe** | Duplicate-alert prevention using session state |
 
---
 
## 🧪 Validation & Concept Iteration (Checkpoint 2)
 
Before technical implementation, the team conducted an extensive **validation phase** focusing on **AI empathy, memory, and safety** using **persona-based prompting.**
 
### **Persona Design**
- **Maggie (79)** – lives alone, mild arthritis, enjoys chatting daily.  
- **Lilly (82)** – recovering from surgery, occasionally forgets medication.
 
Each persona included:
- Daily medical routine  
- Emotional preferences  
- Social behavior patterns  
- Safety protocols (e.g., what to do in dizziness episodes)
 
---
 
### **Prompting Protocol**
 
Prompts were classified into:
1. **Typical cases** – everyday conversations  
2. **Edge cases** – unexpected or emotional scenarios  
3. **Failure cases** – emergencies or model misunderstanding  
 
This revealed major empathy and safety gaps in existing tools (Gemini, ChatGPT, Copilot, etc.), shaping Carely’s **memory-driven empathetic architecture.**
 
---
 
### **Gap Analysis Findings**
 
| Aspect | Observed Gap | Carely Solution |
|--------|---------------|----------------|
| Memory | Context lost after few turns | Persistent multi-layer memory |
| Empathy | Generic replies | Persona-based fine prompting |
| Emergency | Weak detection | Rule-based real-time detection |
| Caregiver Visibility | Absent | Dual-portal caregiver view |
| Cost | Paid APIs | Free local stack (Groq + ChromaDB) |
 
---
 
## ⚙️ Implementation Summary (Checkpoint 3)
 
### **Tech Stack**
 
| Layer | Technology |
|-------|-------------|
| Frontend | Streamlit, Plotly, streamlit-mic-recorder |
| Backend | FastAPI, APScheduler |
| Database | SQLite + SQLModel |
| Vector Store | ChromaDB |
| AI Model | Groq API — Llama-3.3-70b-versatile |
| Notifications | Telegram Bot API |
| Voice Output | gTTS |
| Utilities | Requests, NumPy, Scikit-learn |
 
---
 
### **System Flow**
 
1. User interacts through Streamlit chat UI (text/voice).  
2. `CompanionAgent` sends message to Groq LLM.  
3. `MemoryManager` fetches context from all memory layers.  
4. Response generated → displayed → stored.  
5. Sentiment/emergency analysis runs locally.  
6. If alert triggered → caregiver notified via Telegram.  
7. Daily summaries auto-generated for episodic continuity.
 
---

## ✅ Checkpoint 4 Summary (Evaluation & Findings)

- Conducted a structured user evaluation with **6 pilot users** and **2 caregivers**, testing mood check-ins, memory recall, medication logging, emotional-support chats, quick actions, and emergency alerts.

- **Usability Metrics:** Achieved a strong **UMUX-Lite score of 82/100**, with average ratings around **4.0/5** for helpfulness, trust, usefulness, and safety during emergency prompts.

- **What Worked Well:**  
  - Users consistently appreciated Carely’s **empathetic, non-robotic tone**.  
  - Logging health data through chat felt **effortless** compared to forms.  
  - Memory of recent details made the assistant feel more human and reduced repetitive interactions.  
  - Natural language understanding often exceeded expectations, handling everyday conversations smoothly.

- **Pain Points Identified:**  
  - **Inconsistent long-term recall** in extended conversations.  
  - **Visual and UI clarity issues** such as message alignment, small fonts, and insufficient contrast.  
  - Emergency alert flow slower and more rigid than other tasks.  
  - Occasional hallucinations during confusing inputs.

- **Key Improvements After Study:**  
  - Updated UI for clarity (alignment fixes, larger fonts, cleaner contrast).  
  - Refined quick-action layout to avoid clutter.  
  - Improved memory stability logic and added stricter safety checks (PII redaction and no storage of sensitive information).

- **Validated User Needs:**  
  - Seniors want **more personalization**, including tailored prompts and preferences.  
  - Need for **bigger fonts and cleaner visual layout** to reduce confusion.  
  - Desire for **stronger long-term memory** to maintain trust over repeated use.  
  - High importance placed on **timely proactive reminders** for medication and daily routines.  
  - **Voice-first interaction** (STT/TTS) significantly boosts accessibility for low-tech users. 
- **Risks & Limitations:**  
  - Small, demographically narrow pilot group; results may not generalize.  
  - Model unpredictability (hallucinations, inconsistent temporal reasoning).  
  - Ethical balance between **helpfulness vs. user over-dependence**.

- **Future Enhancements:**  
  - Chat-based schedule editing.  
  - Multilingual support.  
  - Better temporal memory indexing.  
  - HIPAA-ready data handling.  
  - Integration with senior homes and wearable devices.


## 🤖 AI Disclosure

This project leveraged multiple AI-powered tools to enhance development efficiency, user experience, and code quality. Below is a transparent list of AI systems utilized during the development of Carely:

- **Cursor AI** (2024). AI-assisted code editor used for rapid prototyping, debugging, and generating implementation suggestions.  
  🔗 https://www.cursor.com

- **Replit AI** (2024). AI agent support for UI improvements, bug fixes, and assistance in streamlining the Streamlit front-end development.  
  🔗 https://replit.com

- **Microsoft Copilot Studio** (2024). Used for prompt optimization and design of conversational behavior in chatbot flows and safety guardrails.  
  🔗 https://www.microsoft.com/en-us/microsoft-copilot-studio

- **Antigravity** (2024). Assisted with content enhancement, code refactoring recommendations, and workflow automation throughout the project lifecycle.  
  🔗 https://antigravity.ai/

---

**Note:** All AI-generated outputs were reviewed, revised, and validated by the project team to ensure correctness, safety, and alignment with responsible development practices.


