# Carely AI System Architecture

## Overview

The diagram above represents the **end-to-end architecture** of **Carely AI**, a conversational companion designed for senior care.  
It highlights all major system layers — from the Streamlit frontend to the FastAPI backend, memory stack, database, LLM agent, scheduler, and external notification services.

---

## 1️⃣ Frontend – Streamlit UI
**Files:** `main.py`, `frontend/dashboard.py`

- Provides the chat and overview interface for users.
- Displays **Event schedules**, **medication adherence**, and **proactive reminders**.
- Sends user inputs and context as HTTP JSON requests to the FastAPI backend.

---

## 2️⃣ Backend API – FastAPI
**File:** `app/api/routes.py`

- Central request handler between the UI, LLM agent, memory modules, and database.
- Routes messages to the appropriate logic (chat handling, events, reminders).
- Integrates utilities for safety, redaction, and timezone consistency.

**Connected modules:**
- `pii_redaction.py` → removes personal identifiers.
- `emergency_detection.py` → detects urgent health conditions.
- `timezone_utils.py` → maintains CST/CDT consistency.
- `companion_agent.py` → main conversational logic layer.

---

## 3️⃣ Agent Layer – Groq Orchestration
**File:** `app/agents/companion_agent.py`

- Acts as the “brain” of Carely.
- Builds structured prompts and communicates with the **Groq LLM API**.
- Interfaces with the **Memory Manager** to recall and store user context.
- Can log outputs or events to the database for long-term retention.

---

## 4️⃣ Memory Orchestration
**Folder:** `app/memory/`

| Component | Description |
|------------|-------------|
| `memory_manager.py` | Coordinates between all memory layers and decides what to read/write. |
| `short_term_memory.py` | Tracks the current chat window for contextual continuity. |
| `episodic_memory.py` | Summarizes daily interactions (“What did we talk about yesterday?”). |
| `long_term_memory.py` | Handles semantic embeddings via **ChromaDB**. |
| `structured_memory.py` | Stores structured facts and key user data in SQLModel/SQLite. |

**External connections:**
- Reads/writes structured memory via `app/database/crud.py`.
- Stores semantic embeddings in **`data/vectors/`** (ChromaDB).

---

## 5️⃣ Persistence – SQLModel / SQLite
**Files:** `app/database/models.py`, `app/database/crud.py`, `data/carely.db`

- Stores persistent user data: profiles, medication logs, events, caregivers, summaries.
- Exposes CRUD operations for use by both API routes and the memory manager.
- Provides a unified persistence layer for structured memory and reminders.

---

## 6️⃣ Scheduler – APScheduler
**File:** `app/scheduling/reminder_scheduler.py`

- Periodically checks for **medication times** and **high-importance events**.
- Uses `timezone_utils.py` for local time alignment.
- Triggers caregiver alerts through `telegram_notifier.py`.
- Writes reminder logs to the database for tracking.

---

## 7️⃣ Utilities & Safety
**Folder:** `app/utils/`

| File | Role |
|------|------|
| `pii_redaction.py` | Detects and removes personally identifiable information. |
| `emergency_detection.py` | Flags critical phrases and triggers caregiver alerts. |
| `timezone_utils.py` | Converts UTC to CST/CDT and defines “today/this week” windows. |
| `telegram_notifier.py` | Sends outbound notifications through Telegram Bot API. |

---

## 8️⃣ External Services

| Service | Purpose |
|----------|----------|
| **Groq LLM API** | Generates responses and summaries through the Llama 3.3-70B model. |
| **Telegram Bot API** | Sends proactive reminders and emergency alerts to caregivers. |
| **ChromaDB (data/vectors/)** | Stores long-term semantic memory embeddings. |

---

## 🔁 Data Flow Summary

1. **User → Streamlit UI** → enters chat or logs medication.
2. **UI → FastAPI (routes.py)** → request sent via JSON.
3. **FastAPI → Companion Agent** → builds prompt, invokes LLM, manages memory.
4. **Agent → Memory Manager** → retrieves context (ST, episodic, LT, structured).
5. **Memory Manager → Database / ChromaDB** → reads/writes data as needed.
6. **Scheduler** runs in background, checks reminders → notifies caregivers via Telegram.
7. **Utilities** handle PII redaction, timezone alignment, and emergency escalation throughout the flow.

---

## 🧩 Architecture Highlights

- **Multi-layer memory ecosystem** (short-term, episodic, long-term, structured)
- **Centralized orchestration** via `companion_agent.py`
- **Fully local persistence** with SQLite + ChromaDB (no external data leaks)
- **Proactive & safety-aware** reminders with redaction and alert mechanisms
- **Modular code layout** under `/app/` for clean scaling and testability

---

## 📁 File Location

