# Literature Review: Senior Care Companion Project

---

## Paper 1: EmpDG – Multi-resolution Interactive Empathetic Dialogue Generation

**Citation:**  
Li, Q., Chen, H., Ren, Z., Ren, P., Tu, Z., & Chen, Z. (2020). *EmpDG: Multi-resolution interactive empathetic dialogue generation.* In Proceedings of the 28th International Conference on Computational Linguistics (COLING 2020) (pp. 4454–4466). International Committee on Computational Linguistics. [https://doi.org/10.18653/v1/2020.coling-main.394](https://doi.org/10.18653/v1/2020.coling-main.394)

**Summary:**  
The EmpDG paper addresses the problem of dialogue systems producing emotionally flat responses that fail to convey empathy, which is especially important in supportive conversations. The authors propose a multi-resolution framework that models emotions at both the **dialogue level** (overall sentiment) and **token level** (emotion words) to better capture subtle emotional signals. They also introduce an **interactive adversarial learning setup** where a discriminator ensures generated responses are empathetic as well as coherent. Experiments on empathetic dialogue datasets show that EmpDG significantly outperforms baseline models in emotional alignment and content quality. This demonstrates that incorporating explicit emotional modeling leads to more human-like, caring responses in AI.

### 3 Insights Learned
1. **Emotion has layers** — both the overall tone and specific words contribute to empathy, and both must be modeled to feel natural.  
2. **Feedback loops improve empathy** — using adversarial training or even lightweight feedback (thumbs up/down) helps refine responses.  
3. **Balancing empathy + relevance is key** — responses should be supportive and stay on-topic, not just one or the other.

### 2 Limitations / Risks
1. The model is **resource-intensive** (adversarial training + fine-grained modeling), which may be impractical for lightweight, offline senior-care agents.  
2. It depends heavily on **emotion-labeled datasets**, which may not reflect the cultural, generational, or health-specific language of seniors.

### Concrete Idea for Your Project
Instead of training a heavy empathetic dialogue model, adopt EmpDG’s insight by creating a **lightweight emotion-response mapping system**:  
- Detect a senior’s mood (happy, sad, lonely, confused, in-pain) via **keyword + sentiment classifier**.  
- Map each emotion to empathetic voice responses + optional actions.  
  - Example for sadness: *“I hear you. Would you like me to play a devotional song on YouTube or message your daughter?”*

---

## Paper 2: Use of Intelligent Voice Assistants by Older Adults with Low Technology Use

**Citation:**  
Pradhan, A., Lazar, A., & Findlater, L. (2020). *Use of Intelligent Voice Assistants by Older Adults with Low Technology Use.* ACM Transactions on Computer-Human Interaction, 27(4), Article 31. [https://doi.org/10.1145/3373759](https://doi.org/10.1145/3373759)

**Summary:**  
This paper studies how older adults who use technology infrequently perceive and use voice assistants (smart speakers), especially in domestic settings. The authors conducted a **three-week field deployment** of Amazon Echo Dot in the homes of seven older adults to observe usage patterns and helpful features. They found that **health-related information** remained consistently useful, while features like reminders and timers saw much lower usage due to concerns about reliability. Participants appreciated the simplicity of voice interaction but adoption was hindered by trust and performance gaps.

### 3 Insights Learned
1. **Health information is valued** — older adults consistently sought health-related info using smart speakers.  
2. **Reliability determines trust** — memory/routine features are only accepted if consistent; trust is key.  
3. **Simplicity and low tech effort** — participants liked voice assistants for requiring minimal interaction; features with complexity or errors lost adoption over time.

### 2 Limitations / Risks
1. **Small sample size & short duration** — only 7 participants over 3 weeks; may not generalize to wider populations or long-term usage.  
2. **Reliability & voice recognition concerns** — misinterpretation of speech patterns can reduce trust and lead to abandonment.

### Concrete Idea for Your Project
Build with **“reliability by feedback”**:  
- After each reminder, the system asks: *“Was this reminder helpful / accurate?”*  
- If the response is negative, the system logs it, retries, or escalates to a caregiver.  
- This builds **trust**, allows tuning early in deployment, and ensures seniors rely on critical features.
