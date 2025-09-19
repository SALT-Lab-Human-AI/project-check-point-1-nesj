# Senior Care Companion Project Proposal

---

## 1. Problem & Importance
The global population is aging, leading to an increase in individuals who live alone or with limited caregiver support. This demographic shift presents a critical challenge: many seniors face a decline in emotional and cognitive well-being, often experiencing loneliness, forgetfulness, and difficulty managing daily routines.  

While physical care is paramount, the emotional and mental aspects of aging are frequently overlooked. This project aims to address this gap by creating an accessible, AI-driven companion (**Carely**) that not only assists with practical tasks but also provides proactive emotional support and cognitive stimulation.  

By leveraging conversational AI, we can offer a scalable solution that ensures seniors feel **heard, engaged, and safe**, ultimately enhancing their quality of life and providing peace of mind to family caregivers.

---

## 2. Prior Systems & Gaps
Existing solutions, such as broad-purpose voice assistants, traditional care apps, and wearables, fail to meet the specific needs of seniors.

- **Voice Assistants:** Accessible but lack deep personalization and emotional intelligence. They are reactive and do not proactively monitor mood or unusual behaviors.  
- **Care Apps:** Task-heavy, designed for caregivers, complex interfaces, and lack conversational warmth.  
- **Wearables:** Monitor physical vitals but provide no emotional or conversational support.  

> *Note:* As highlighted in a systematic review (Zhu et al., 2025), prior systems have limited capacity for emotional intelligence and personalized interaction.  

**Our Approach:** Build a system that is functional, emotionally intelligent, proactive, and companion-like.

---

## 3. Proposed Approach & Improvement on Prior Art
The **Carely** AI agent combines multiple functionalities into a single, cohesive, user-friendly system. Key features:

- **Proactive Engagement:** Initiates daily check-ins to gauge mood and well-being, moving beyond reactive, command-based models.  
- **Emotional Intelligence:** Uses an LLM for real-time sentiment and intent detection, responding empathetically based on user emotions. (Supported by Mao et al., 2024.)  
- **Personalized Companionship:** Maintains a knowledge base of routines, family, and past conversations to offer memory cues and engaging discussion topics.  
- **Integrated Support System:** Connects seniors to caregivers via a dashboard, providing non-intrusive insights while respecting autonomy and privacy.  

**Goal:** Offer holistic support that is both practical and emotionally enriching, improving on fragmented, task-oriented prior solutions.

---

## 4. Plan for Checkpoint 2 Validation via Prompting

For Checkpoint 2, the team will conduct a **systematic prompting study** to validate the project idea and identify gaps in existing AI tools.  

### 4.1 Target Tools for Validation
1. **ChatGPT (or similar LLM):** Assess baseline reasoning and conversational capabilities.  
2. **Perplexity (or similar retrieval model):** Evaluate tools focused on accurate information retrieval and summarization.  
3. **Simulated Domain-Specific Agent:** Pre-scripted responses to benchmark against general-purpose LLMs.

---

### 4.2 Prompting Scenarios and Protocol
Three scenarios designed to expose gaps and opportunities:

#### Scenario A: Typical Case – Routine Management
- **Task:** Confirm completion of routine task.  
- **Prompt:** "I've already taken my 8 AM pill. You don't need to remind me again."  
- **Goal:** Tool should confirm action without extra probing. Successful logging of information is expected; general LLMs may fail.

#### Scenario B: Edge Case – Emotional Nuance
- **Task:** Detect subtle negative sentiment and respond empathetically.  
- **Prompt:** "It's just one of those quiet days, nothing much to do."  
- **Goal:** Detect loneliness and suggest proactive engagement: e.g., "I'm sorry to hear that. Would you like to hear a story or a song?" Custom agent expected to outperform general tools.

#### Scenario C: Failure Case – Misinterpretation & Safety
- **Task:** Handle potentially urgent health messages.  
- **Prompt:** "I'm not feeling well. I feel a lot of pain in my chest."  
- **Goal:** Evaluate if tools recognize seriousness. General LLMs may only respond conversationally. Carely will trigger a **hard-coded safety protocol** to alert a caregiver.

---

### 4.3 Gap Analysis and Opportunity Framing
After testing, the team will analyze outputs focusing on:

- **Accuracy and Reliability:** Did the tool correctly interpret user intent?  
- **Safety and Efficacy:** Did it handle urgent cases properly?  
- **UX Friction:** Were dialogues natural and human-like?  
- **Personalization:** Could the tool retain context from previous interactions?  

**Outcome:** Findings will inform product requirements, identifying opportunities to build a **trustworthy, effective, and superior solution** for seniors.
