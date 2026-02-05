# Artifact Package: Carely AI Companion
## Deployment Link, Reproduction Instructions, and Prompt Scripts

---

## 1. **Deployed Link**
The live deployed version of Carely is available at:

👉 **https://carely-final.streamlit.app/**

Runs directly in the browser. No installation required.

---

## 2. **Access Instructions**

### **Using the deployed app**
1. Open: **https://carely-final.streamlit.app/**
2. Log in or create a profile.
   You can use the below logins:
   - maggie@demo.com; maggie123
   - dorothy.johnson@email.com; carely-demo
3. Interact using:
   - Text input  
   - Voice input (🎤)  
   - Quick Actions (on the Carely Chatbot window below the chatbar) 
   - Medication logging  
   - Wellness routines   
4. Press **🔊** to hear the carely bot responses.

### **Caregiver Alert Access**
Triggered automatically when:
- User expresses distress (e.g., *“I have chest pain”*)  
- Safety module classifies based on the severity

Caregiver receives:
- Alert reason  
- Timestamp  
- User details  

---

## 3. **Prompts Used to Reproduce Results**

### **3.1 Wellness Guidance Prompts**
**Prompt:**  
> “Give me quick exercises to follow.”

**Follow-up:**  
> “Yes guide me through those steps.”

---

### **3.2 Contextual Memory + Activity Reflection**
**Prompt:**  
> “I just went to walk with my dog and it's a bright sunny day outside.”

**Follow-up:**  
> “We are planning a potluck tonight, what should I cook?”

---

### **3.3 Proactive Medication Check-ins**
Proactive Greeting:
> “Good evening Dorothy, I noticed you have a few medications to take care of tonight…”

---

## 4. **Testing Prompts for Each Use Case**

### **4.1 Safety & Alerts**
```
I have chest pain.
```
Expected: Emergency alert → Telegram.

```
When was my caregiver last contacted?
```

---

### **4.2 Medication Management**
```
Tell me my entire day routine.
```
```
When should I take my Metformin?
```

---

### **4.3 Memory & Personalization**
```
What did I tell you about my grandson’s birthday gift?
```
```
What food am I preparing for the neighborhood festival stall?
```

---

### **4.4 Wellness & Emotional Support**
```
Guide me through a breathing exercise.
```
```
I’m feeling a bit low today.
```

---

### **4.5 Deterministic Queries**
```
What’s the time now?
```
```
My insurance number is 98765.
```

---

### **4.6 Accessibility (Voice & Audio)**
Voice input:
```
Hello Carely.
```

Audio playback: press **🔊**.


---

## 5. **Included Files / Modules**
- `dashboard.py` – Streamlit UI  
- `companion_agent.py` – LLM + Safety + Memory logic  
- `memory_manager.py` – STM/LTM/Episodic fusion  
- `scheduler.py` – reminders + daily summaries  
- `conversation_store.py` – SQLite interface  
- `tts_helper.py` – text-to-speech  
- `use-cases.md` – evaluation use cases  

---

## 6. **Reproducibility Notes**
- Deterministic logic handles: time, safety, meds, DB.
- STM stored in SQLite conversation table.
- LTM uses ChromaDB vectors.
- Telegram alerts require valid tokens.
