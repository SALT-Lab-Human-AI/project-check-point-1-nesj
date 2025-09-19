# Senior Care Companion – AI-based Memory & Wellness Support (Carely)

## 📝 Problem Statement
Many seniors face loneliness, forgetfulness, and difficulty managing daily routines. Traditional care models focus on physical well-being but often overlook emotional support, cognitive stimulation, and proactive assistance. With limited caregiver availability, there is a strong need for an accessible, AI-driven companion that ensures seniors feel supported, engaged, and safe every day.

---

## 🎯 Target Users & Core Tasks

### Users
- **Seniors living alone or with minimal caregiver presence**: Desire a simple, conversational interface for companionship and daily assistance.  
- **Family caregivers**: Want peace of mind and proactive alerts about their loved one's well-being.  
- **Care facilities**: Seek digital tools to augment staff capacity, automate check-ins, and gather non-intrusive wellness data.  

### Core Tasks
- Daily check-ins (“How are you feeling today?”)  
- Sentiment & intent detection (detect “sad”, “confused”, “urgent”)  
- Routine reminders (medications, appointments, meals)  
- Personalized engagement (recommending devotional songs, stories, light exercises)  
- Escalations (alert caregiver if urgent condition detected)  
- Memory cues (remind names of family members or important dates)  

---

## 🔍 Competitive Landscape

### Existing Solutions
- **Voice assistants (Alexa, Google Home)** – broad but not senior-focused, lack personalization.  
- **Care apps** – task-oriented, often designed for caregivers, interfaces complex for seniors.  
- **Wearables** – track physical data but lack conversational/emotional support.  

### Shortcomings
- **Poor Personalization**: Fail to adapt to individual senior needs, language, or history.  
- **Limited Emotional Intelligence**: Cannot detect subtle changes in mood or tone.  
- **Lack of Proactive Nudging**: Passive, waiting for commands instead of engaging.  
- **No Holistic Integration**: Siloed solutions, not combining reminders, emotional support, and caregiver insights.  

---

## 💡 Initial Concept & Value Proposition

### Concept
A lightweight, conversational AI that seniors can talk to daily, tracking emotional states, routines, and proactively supporting wellness.  

### Value Proposition
- Provides companionship **plus** practical help (not just reminders).  
- **Bridges the Gap**: Connects seniors to caregivers with actionable, non-intrusive insights.  
- **Early Intervention**: Detects patterns (e.g., declining mood, missed meds) for proactive nudging.  
- **Affordable, simple, and tailored for seniors**.  

---

## 📆 Project Checkpoints

### ✅ Checkpoint 1 (Week 1): Foundation & Scoping
**Goal**: Establish project plan & dev environment.  
**Milestones**:
- Finalize scope, value proposition, and `README.md`.  
- Literature review + reflections.  
- Write `PROPOSAL.md`.  
- Set up dev environment (file structure, Docker for Ollama, dependencies).  

**Team Roles**:
- **Backend & DB**: FastAPI + SQLite setup.  
- **AI & Agent**: Ollama + LangChain agent framework.  
- **Frontend & UI**: React placeholder.  
- **Research & Docs**: Research + proposal writing.  

---

### ✅ Checkpoint 2 (Week 2): Core Functionality & Validation
**Goal**: Build basic end-to-end voice loop + validate assumptions.  
**Milestones**:
- Implement local voice loop (STT: faster-whisper, TTS: Piper, LLM: Ollama).  
- First agent tool: `record_event_response` → DB.  
- Minimal frontend (voice loop trigger + caregiver input).  
- Validation study on 3+ tools → gap analysis report.  

**Team Roles**:
- **Backend & DB**: Finalize API endpoints, DB updates.  
- **AI & Agent**: Integrate STT/TTS into loop.  
- **Frontend**: Core prototype, user journey.  
- **Validation & Analysis**: Study + report.  

---

### ✅ Checkpoint 3 (Week 3): Smart Features & Caregiver Integration
**Goal**: Implement smart features + caregiver dashboard.  
**Milestones**:
- Proactive reminder scheduler + missed dose alerts.  
- Sentiment detection integrated with prompts.  
- `notify_caregiver` tool via Telegram Bot API.  
- Caregiver dashboard UI (adherence + sentiment).  

**Team Roles**:
- **Backend**: Scheduler + Telegram API.  
- **AI & Agent**: Refine prompts for emotional nuance.  
- **Frontend**: Dashboard + data visualizations.  
- **Integration & Testing**: End-to-end testing.  

---

### ✅ Checkpoint 4 (Week 4): Final Product & Polish
**Goal**: Deliver polished, documented final product.  
**Milestones**:
- Refine features with feedback.  
- Add personalized engagement (memory cues, storytelling).  
- Implement escalation protocol.  
- Finalize UI/UX for senior + caregiver portals.  
- Write full technical docs + presentation.  

**Team Roles**:
- **Backend**: Optimize APIs + finalize DB schema.  
- **AI & Agent**: Add final tools + refine conversations.  
- **Frontend**: Polish UI.  
- **Docs & Presentation**: Consolidate deliverables + showcase.  

---

✨ This project (Carely) aims to redefine senior care by blending emotional intelligence with proactive digital support, ensuring seniors feel connected, safe, and cared for.
