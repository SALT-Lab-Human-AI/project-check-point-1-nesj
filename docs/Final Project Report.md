# IS 492: Final Project Report
## Carely: AI-based Memory & Wellness Support for Seniors

### Abstract
Carely is an AI-based memory and wellness companion designed to support older adults in their daily lives. Many seniors face challenges such as forgetfulness, inconsistent medication adherence, and emotional isolation, which can negatively affect their independence and overall well-being. Carely integrates empathetic conversational AI, multi-layer memory, and reliable safety features to offer daily check-ins, personalized reminders, proactive mood support, and caregiver alerts. The system combines a large language model for natural, adaptive dialogue with structured scheduling, semantic memory retrieval, sentiment detection, and emergency monitoring. A lightweight backend architecture using SQLite and ChromaDB ensures privacy through local data storage and deterministic PII redaction, implemented with a Streamlit frontend and a FastAPI backend. Carely aims to bridge functional support and emotional companionship, helping seniors feel heard, guided, and safe while maintaining a simple and accessible user experience.

### Introduction
**Problem Statement and Motivation:**
Older adults increasingly face a complex set of cognitive, emotional, and practical challenges that affect their daily functioning. Age-related memory decline often disrupts routine activities such as remembering medications, tracking appointments, or events. Even when seniors remain physically independent, the cumulative impact of small lapses can elevate health risks and diminish confidence in self-management. These challenges are compounded for individuals managing multiple medications, chronic conditions, or irregular care patterns; circumstances that require reliable behavioral reinforcement and timely reminders.

Emotional well-being presents an equally significant concern. Many older adults live alone, experience reduced social contact, or rely on brief, infrequent interactions with caregivers and family members. The absence of daily conversational engagement can intensify feelings of loneliness, anxiety, or disorientation. While caregivers strive to provide support, the demand for continuous monitoring and emotional presence is rarely feasible, creating gaps that technology could meaningfully address.

Existing digital tools, however, fall short of meeting these multidimensional needs. Voice assistants provide convenience but often struggle with contextual memory, conversational coherence, or understanding the softer emotional nuances essential for senior communication. Reminder and scheduling apps require technical familiarity and typically lack adaptive dialogue, empathy, or safety awareness. Wearable devices excel at capturing physiological data yet offer minimal guidance beyond basic notifications and lack conversational reassurance. In practice, seniors encounter fragmented solutions each addressing a narrow function but failing to create a cohesive, supportive experience.

A fundamental gap persists: there is no widely accessible system that combines empathetic communication, routine reinforcement, contextual memory, and safety monitoring in a format that feels natural and non-intimidating to older adults. Seniors need tools that respond not only to what they say, but also to how they feel, what they struggle to remember, and the patterns that emerge across days of conversation. They need support that is proactive rather than reactive, capable of checking in, noticing concerning changes, recalling meaningful context, and escalating risk appropriately.

Carely was developed to address this gap by integrating conversational warmth with structured intelligence. The system is designed to operate not as a transactional assistant but as a consistent companion that adapts to a user’s routines, communicates with empathy, and offers guidance grounded in long-term context. Through multi-layer memory, Carely can recall past interactions, track daily summaries, interpret behavioral cues, and generate responses that feel genuinely personalized. Through built-in safety guardrails, it ensures predictable handling of emergencies, medication inquiries, and other high-risk interactions.

The overarching motivation is to increase independence, emotional resilience, and safety for older adults while reducing caregiver burden. Carely aims to meet seniors where they are linguistically, cognitively, and emotionally by providing a calm, trustworthy presence that is always available. At the same time, the system is deliberately designed to respect privacy through local data storage and transparent data handling practices, addressing a key barrier to technology adoption among older adults. 

By blending human-centered design with technical rigor, Carely seeks to reimagine what supportive AI can look like for an aging population: a system that reinforces daily structure, nurtures emotional connection, and intervenes with clarity when safety demands it.

### Literature Review
Research on AI-driven support for older adults spans several interconnected domains, including technology acceptance, conversational companionship, emotional intelligence, and cognitive reinforcement. Together, these bodies of work illuminate both the opportunities and design constraints associated with building systems like Carely that must operate reliably, empathetically, and safely in real-world eldercare contexts.

**Acceptance of AI Among Older Adults:**
Across numerous studies, older adults demonstrate a clear interest in assistive technologies when the systems feel intuitive, unobtrusive, and trustworthy. Wong et al. [1] highlight that adoption is strongly tied to perceived transparency and ease of control; seniors are more receptive to tools that explain how data is used and provide simple mechanisms for modifying preferences. Many older adults exhibit apprehension toward opaque automated systems, particularly those that adapt behavior without explicit user feedback. 

Zhu et al. [2] further note that unpredictability and perceived loss of autonomy are major barriers to long-term engagement. When seniors cannot anticipate how an AI system will behave or when it responds inconsistently their trust deteriorates rapidly. These findings are especially relevant to conversational AI, where variability in responses can be interpreted as unreliability.

Reliability appears repeatedly as a decisive factor. Pradhan et al. [3] show that older adults abandon systems after just a few errors, such as incorrect reminders, misinterpreted speech, or inconsistent follow-through. This creates a high bar for designing dependable systems; even minor lapses can undermine user confidence. For Carely, this evidence reinforces the need for deterministic logic in medication support, emergency detection, and contextual recall, ensuring that safety-critical functions do not depend solely on generative output. Collectively, this literature underscores the importance of transparency, predictability, and supportive interaction principles deeply integrated into Carely’s design.

**AI Companions and Loneliness Reduction:**
Loneliness among older adults is a well-documented public health concern. AI conversational companions have emerged as a potential intervention by offering consistent, emotionally supportive engagement. Yang et al. [4] demonstrate that empathetic conversational agents can meaningfully reduce perceived loneliness when interactions feel coherent and ongoing rather than fragmented or purely transactional. 

Mao et al. [5] emphasize that the most effective systems foster a sense of being heard. Users respond positively when dialogue acknowledges prior conversations, references past experiences, and adapts to personal preferences. These findings directly support the use of multi-layer memory within Carely, enabling the system to recall details from previous interactions and maintain continuity over days or weeks. 

Chen et al. [6] further caution that seniors are sensitive to repetitive or mechanical responses. Overused phrasing or lack of contextual understanding can break the illusion of companionship and lead to disengagement. This insight informs Carely’s controlled prompting strategy, sentiment-based tone modulation, and incorporation of long-term semantic recall to reduce repetitive patterns in conversation flow.

**Empathetic Dialogue and Emotion Modeling:**
Empathy is a critical element of supportive conversational AI, especially in eldercare contexts where emotional states may fluctuate throughout the day. Li et al. [7] demonstrate that multi-resolution emotional modeling capturing both fine-grained sentiment and broader affective signals significantly improves user perception of empathy. However, advanced neural emotion models often require large datasets, additional compute, and extensive model customization. 

Additionally, the literature highlights the importance of aligning emotional support with context. Empathy without situational grounding can feel generic or insincere. Carely’s memory architecture addresses this by providing context-rich inputs to the LLM, enabling responses that reflect prior conversations, user routines, and long-term behavioral patterns.

**Cognitive Well-Being and Structured Conversational Support:**
Conversational AI has shown potential for reinforcing cognitive engagement among older adults. Xu and Zhang [8] found that personalized, structured conversations can stimulate memory recall, promote reflection, and help users maintain attention. Systems that tailor interactions to user interests, routines, and past events have a greater likelihood of sustaining engagement over time. 

This research supports the inclusion of episodic memory, structured behavioral logs, and routine-based prompts in Carely’s design. By summarizing daily themes and identifying key topics across conversations, the system can deliver cognitive cues that feel personalized and meaningful. Additionally, features such as memory games, quick actions, and playful interactions (e.g., jokes or music choices) align with evidence that cognitive stimulation is most effective when embedded in enjoyable and familiar activities.

**Synthesis:**
Across all domains, the literature consistently points to four requirements for effective eldercare AI:
* Reliability and predictability in routine and safety-related tasks
* Continuity and personalization through memory and adaptive dialogue
* Emotional intelligence grounded in contextual understanding
* Simplicity and accessibility in user interaction

Carely’s architecture and feature set reflect these insights directly. By integrating structured memory with empathetic LLM dialogue, deterministic safety logic, and a high-accessibility interface, the system aligns tightly with established research while addressing persistent barriers to technology adoption among older adults.

### Method
**System Description:**
The development of Carely follows a modular, end-to-end architecture designed to support elderly users through natural dialogue, personalized context recall, mood tracking, proactive medication reminders and safety monitoring. The system is composed of four primary layers: the Streamlit-based frontend, FastAPI backend, LLM-driven agentic core, and a multi-tier memory subsystem (Figure 1). Each component is engineered to balance usability, technical robustness, and privacy, ensuring that interactions feel human-centered while remaining computationally efficient and predictable.

**Frontend Layer:**
The user interface is implemented in Streamlit, chosen for its rapid prototyping capabilities and compatibility with senior-friendly design principles. It provides text input, voice input through integrated speech-to-text, and the ability to play back AI responses using a clearly visible speaker button. These features address accessibility needs by reducing reliance on typing and improving clarity for users with hearing or visual limitations. 

The dashboard aggregates real-time insights using Plotly visualizations, presenting medication adherence, mood trends, and conversation history (Figure 2,3,5) in formats that are easy for seniors and caregivers to interpret.

The UI also includes:
* Quick Action buttons for common tasks such as logging medication, playing music, initiating a memory cue, or accessing a fun corner and built-in cognitive game. (Figure 4)
* Emergency safety sheets, which are displayed when the system detects concerning phrases or emotional distress.
* A memory game, designed to promote cognitive engagement through a card-matching challenge with adjustable difficulty and visually recognizable emojis.

The frontend maintains state through the Streamlit session mechanism, allowing seamless transitions between chat, reminders, health insights, and emergency flows without overwhelming the user. Senior-friendly color schemes, larger text, simplified spacing, and predictable navigation structures further enhance usability.

**Backend Layer:**
The backend is powered by FastAPI, enabling efficient routing and modular service organization. Its responsibilities include:
* Authentication and session management
* CRUD operations for user profiles, medications, events, conversations, and caregiver relationships
* Logging and monitoring of all AI-generated and user-generated messages
* Task scheduling using APScheduler for medication reminders, daily summaries, and periodic check-ins
* Delivery of notifications, particularly emergency alerts sent through Telegram to registered caregivers

Data persistence is handled locally using SQLite, which supports fast queries while eliminating external dependencies. This design choice aligns with older adults’ privacy expectations: sensitive health data and conversational logs remain entirely on-device or within local execution environments. Meanwhile, ChromaDB is used for semantic vector storage, enabling long-term recall of meaningful conversational patterns and user-specific details.

**LLM Agentic Core:**
The CompanionAgent serves as the cognitive engine of the system. It coordinates between deterministic rule-based components and generative reasoning modules to ensure that interactions remain safe, empathetic, and contextually grounded. Key functionalities include:

* Intent recognition, routing questions to appropriate handlers such as medication lookup, event retrieval, or conversational engagement.
* Sentiment classification, which identifies user mood and influences tone adjustments and proactive check-ins. (Figure 3,6)
* Emergency triage leverages a structured keyword–pattern detection system that identifies high-risk statements, assigns an appropriate severity level, and initiates the emergency workflow. When a critical threshold is reached, Carely automatically passes the alert to the backend’s notification service, which delivers a real-time Telegram message to the user’s designated caregiver. (Figure 11)
* PII redaction, applied deterministically before prompting the model, reducing the risk of sensitive information leakage. (Figure 7)
* Prompt construction, where relevant memory layers - short-term context, semantic recall, episodic summaries, and structured data are combined into a coherent input block.
* Response generation, executed through an LLM configured on the Groq platform for low-latency inference.

Wherever possible, Carely avoids over-reliance on generative reasoning for safety-sensitive tasks. For example, medication timing queries, emergency detections, and date/time questions are explicitly handled through deterministic logic to prevent hallucinations and ensure consistent system behavior. The agent also uses controlled verbosity, adjusting detail level based on user preferences and conversational context.

**Memory Subsystem:**
Carely’s memory architecture is central to its ability to deliver personalized, consistent dialogue. It is composed of four layers:

* **Short-Term Memory (STM):** Stored in the database, STM retrieves the last several conversational exchanges and formats them into a compact representation. This ensures the LLM receives immediate context without redundant or excessive tokens. (Figure 9)
* **Long-Term Semantic Memory (LTM):** Powered by ChromaDB, LTM stores conversational embeddings, profile facts, and episodic summaries. Retrieval incorporates recency weighting, deduplication, and hygiene mechanisms to remove outdated or low-value entries. The agent uses this layer to recall relevant past experiences, routines, or personal details. (Figure 8)
* **Episodic Memory:** This layer generates daily extractive summaries, capturing the number of conversations, key topics, average sentiment, and medication mentions. These summaries form higher-level temporal context, enabling the agent to recognize changes across days.
* **Structured Memory:** Structured memory provides guaranteed-accurate retrieval of factual data such as medication schedules, personal events, meal times, and logged behaviors. Unlike semantic memory, it is deterministic and supports interactions requiring precision.

The MemoryManager orchestrates these components, assembling a unified context block that blends factual and experiential data for the LLM. This design allows Carely to maintain personality consistency, remember user routines, and offer insights grounded in both short-term interaction and long-term patterns.

### Evaluation Design
The evaluation of Carely focused on understanding how well the system supported real users across everyday tasks, wellness interactions, and safety-critical scenarios. To ground the assessment in realistic use cases, eight participants were involved: six pilot users including classmates and seniors from Wesley Church who interacted directly with the system and two caregivers who reviewed the emergency-alert workflow. Their experiences helped reveal both the strengths of the platform and the inconsistencies that emerged under real conversational and behavioral conditions.

Participants were asked to complete a series of structured tasks intended to evaluate routine interaction flows, memory continuity, emotional support behaviors, and system resilience. Each user began with a daily check-in (“How are you feeling today?”), enabling observation of tone alignment and sentiment detection. They then progressed into memory-based conversations designed to test whether Carely accurately recalled earlier details and incorporated them into replies. Additional interaction paths included exploring proactive reminders, asking for emotional support, and using the quick-action features such as the Memory Game, Play Music, Log Medication, and Fun Corner prompts. Edge-case testing was also performed using intentionally confusing or nonsensical input to probe system stability and classify how the LLM and safety layers behaved under stress. The evaluation concluded with triggering an emergency alert so caregivers could assess the clarity, timing, and reliability of Telegram notifications.

To interpret user performance and system behavior, several metrics were employed:

**Key Evaluation Metrics**
* **Task Success:** Whether users could complete onboarding, log medication, perform check-ins, and confirm that the system recalled prior information.
    * **Finding:** Most tasks were completed successfully, though some users experienced confusion in multi-step flows.
* **Time on Task:** User-rated and observer-measured time required to complete core actions.
    * **Finding:** Most tasks were efficient, but the emergency-alert process took longer than other flows due to additional verification steps.
* **Error Rate:** Failures arising from incorrect LLM outputs, missing memory references, or misunderstandings.
    * **Finding:** Occasional hallucinations appeared in edge cases, and long-term recall showed inconsistency during prolonged conversations.
* **Satisfaction & Usefulness:** Perceived ease of use, trust, and overall interaction quality.
    * **Finding:** Users appreciated the conversational tone and supportive phrasing, but several noted that UI contrast and font sizes needed improvement.
* **UMUX-Lite:** A standardized usability measure used to benchmark experience quality.
    * **Finding:** Carely achieved an overall usability score of 82/100, indicating strong acceptance with room for refinement.
* **Qualitative Themes:** Observed behavior patterns and user comments.
    * **Finding:** Feedback highlighted overflowing quick actions, less-personal memory responses in some cases, and the desire for clearer visual hierarchy in the interface.

Overall, the evaluation demonstrated that Carely is effective for routine wellness tasks, provides meaningful emotional engagement, and performs reliably in safety workflows. At the same time, the findings identify opportunities to improve interface clarity, strengthen long-term memory stability, and reduce conversational variability, insights that inform the system’s future development.

### Results
The evaluation generated a combination of quantitative usability scores and qualitative feedback that together provide a clear picture of how Carely performed in real-world pilot use. The results reflect both the strengths of the system and the areas that require refinement to support sustained adoption among older adults and caregivers.

**Quantitative Findings:**
Across all metrics, Carely demonstrated strong baseline usability. Participants rated key interaction dimensions on a 5-point scale, with results indicating consistent performance above average and several categories approaching high satisfaction. Ease of navigation, helpfulness of AI responses, and system usability all scored between 3.8 and 4.0, suggesting that users were generally able to move through the interface, understand the available actions, and interpret the bot’s messages without major difficulty. Medication management clarity received the highest score at 4.3, reflecting the strength of Carely’s deterministic safety logic and simplified medication workflows.

Participants also rated the reliability of additional features, the likelihood of continued use, and perceived trustworthiness at 4.0, reinforcing that the system’s tone, structure, and functional coverage were aligned with user expectations. Notably, “Felt Safer During Emergency Prompts” also scored 4.0, indicating that although the emergency alert flow was slower than other interaction pathways, participants still felt reassured by the guided steps and the clear escalation process. The lowest individual scores primarily 3.8 in ease of use, user confidence, and emergency scenario accuracy point to minor friction in navigation and occasional hesitation when responding to less predictable AI behavior. 

Overall, the quantitative results show that Carely provides a solid user experience, with scores suggesting strong trust and steady ease of use, but also signaling the need to refine conversational consistency and streamline emergency handling.

**Qualitative Insights:**
Qualitative feedback offered additional depth by highlighting the aspects of Carely that felt intuitive and supportive, as well as the moments that introduced confusion or broken immersion.

* **Positive Themes:** Users repeatedly emphasized a reduction in cognitive load. Logging medications or updating wellness information via conversational input felt more natural than working through menus or structured forms. The system’s ability to blend personal and medical reminders created what several participants described as a “holistic companion feel,” making the assistant seem more relational than functional. The tone; supportive, simple, and non-robotic was one of the clearest reasons users said they would continue interacting with Carely.
  
* **Areas for Improvement:** Two frustrations emerged frequently. First, visual clarity: several users struggled to distinguish between user messages and assistant responses due to alignment and formatting, which reduced readability during longer conversations. Second, memory inconsistency: participants noticed that long-term recall sometimes failed during extended chats, leading to moments where the assistant felt less reliable.

* **Voice of the User:**
Direct quotes captured the emotional resonance of the system:
> “It didn’t feel like I was filling out a medical chart. It felt like texting a friend who cares about my health.”

> “The text-to-speech and speech-to-text made the interaction feel natural — so much easier than typing.”

These reflections reinforce that Carely’s conversational interface and accessibility features meaningfully improve the user experience. Together, the results indicate that Carely is well-received and functionally robust, with clear opportunities to refine UI clarity and long-term memory consistency to improve the system’s reliability and long-term engagement.

### Limitations & Risks
Despite the system’s robust design, several limitations remain. The agent’s reasoning is ultimately dependent on an external LLM, which introduces potential variability in outputs despite the presence of deterministic routing and memory constraints. Although structured memory helps ground factual queries, generative responses may still exhibit subtle inconsistencies or oversimplifications when user inputs are ambiguous or emotionally charged. The long-term memory index, while semantically powerful, can drift over time if embeddings capture noisy or redundant content, necessitating periodic hygiene operations.

From a usability standpoint, the system assumes steady user engagement for accurate sentiment modeling and episodic summaries; sparse interactions reduce the reliability of longitudinal insights. Voice-input features may suffer from transcription errors for users with speech impairments, accents, or background noise. The system’s reliance on local data storage and schedulers also expose it to device-level failures or offline conditions. Finally, emergency detection remains keyword-triggered and rule-based - while intentionally conservative, it may under-classify nuanced distress signals or over-trigger in emotionally expressive users.

### Ethical Considerations
Given its role in a health-adjacent, elderly-support context, the system must uphold strong ethical standards. All interactions involve sensitive personal data - health routines, moods, medication schedules, and caregiver relationships - requiring strict adherence to privacy and data-protection principles. The design intentionally confines data to local storage and structured schemas to minimize exposure, yet users must still be informed about data retention, access policies, and risks associated with unauthorized access.

The system seeks to provide emotional support, but it is not a medical authority. Clear boundaries are necessary to avoid overreliance on AI-generated guidance, particularly in cases involving mental health, medication decisions, or emergencies. Emergency routing is intentionally deterministic to prevent hallucinated instructions, but the system must consistently reinforce that it cannot replace professional help. Algorithmic biases may also emerge in sentiment prediction or conversational tone, especially when the LLM interprets culturally specific expressions or atypical speech patterns. Continuous monitoring and iterative refinement are required to ensure equitable treatment and prevent misclassification-driven harm.

### Conclusion
Carely proved effective in supporting seniors through a conversational, memory-aware interface that reduced cognitive load and strengthened routine adherence. Users consistently valued the system’s contextual recall and voice-first interaction, reporting that it felt more personal and trustworthy when it remembered previous conversations and wellness details. The evaluation shows that AI can enhance not replace human caregiving by offering timely prompts, emotional support, and reliable medication guidance. While the system performed well across core tasks, issues with long-term memory consistency and UI clarity highlight areas for refinement. Overall, Carely demonstrates meaningful potential as a supportive companion that blends empathy, structure, and safety for older adults.

### Future Work
Future improvements will focus on expanding user control and strengthening reliability. Key directions include enabling schedule and appointment updates through chat, adding multilingual support, and integrating temporal memory indexing for richer, time-aware responses. Achieving HIPAA-aligned data protection will be essential as the system scales to real healthcare settings. Deployments in senior-living facilities will provide long-term behavioral insights and real-world stress testing. Additional integrations with wearables such as activity, hydration, or nutrition tracking can further enhance Carely’s ability to provide proactive, personalized wellness support.

### References
[1] Wong, A. K. C., Lee, J. H. T., Zhao, Y., Lu, Q., Yang, S., & Hui, V. C. C. (2025). Exploring older adults’ perspectives and acceptance of AI-driven health technologies: Qualitative study. JMIR Aging, 8, e66778. https://doi.org/10.2196/66778

[2] Zhu, Y., Zeng, T., Li, X., Wu, X., & Li, R. (2025). Conversational Agents for Older Adults’ Health: A Systematic Literature Review. arXiv preprint arXiv:2503.23153. https://arxiv.org/abs/2503.23153.

[3] Pradhan, A., Lazar, A., & Findlater, L. (2020). Use of Intelligent Voice Assistants by Older Adults with Low Technology Use. ACM Transactions on Computer-Human Interaction, 27(4), Article 31. https://doi.org/10.1145/3373759

[4] Yang, Y., Wang, C., Xiang, X., & An, R. (2025). AI applications to reduce loneliness among older adults: A systematic review of effectiveness and technologies. Healthcare, 13(5), 446. https://doi.org/10.3390/healthcare13050446

[5] Mao, W., Luo, X., & Castelo, N. (2024). AI Companions Reduce Loneliness (Working Paper No. 24-078). Harvard Business School. https://www.hbs.edu/ris/Publication%20Files/24-078_a3d2e2c7-eca1-4767-8543-122e818bf2e5.pdf

[6] Chen, H., Li, X., Zhang, Y., & Wang, S. (2024). Qualitative analysis of conversational chatbots to alleviate loneliness in older adults. Healthcare, 12(1), 62. https://doi.org/10.3390/healthcare12010062

[7] Li, Q., Chen, H., Ren, Z., Ren, P., Tu, Z., & Chen, Z. (2020). EmpDG: Multi-resolution interactive empathetic dialogue generation. In Proceedings of the 28th International Conference on Computational Linguistics (COLING 2020) (pp. 4454–4466). International Committee on Computational Linguistics. https://doi.org/10.18653/v1/2020.coling-main.394

[8] Xu, Y., & Zhang, W. (2025). ChatWise: AI-powered engaging conversations for enhancing senior cognitive wellbeing. arXiv. https://arxiv.org/abs/2503.05740

### Appendix
## Figure 1
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/ce52d81318ec9dd408ee1e5ed2de5140016747ee/docs/architecture.png"/>
</p>

## Figure 2
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_2.png"/>
</p>

## Figure 3
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_3.png"/>
</p>

## Figure 4
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_4.png"/>
</p>

## Figure 5
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_5.png"/>
</p>

## Figure 6
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_1.png"/>
</p>

## Figure 7
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_7.png"/>
</p>

## Figure 8
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_8.png"/>
</p>

## Figure 9
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_9.png"/>
</p>

## Figure 10
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/ce52d81318ec9dd408ee1e5ed2de5140016747ee/docs/architecture.png"/>
</p>

## Figure 11
<p align="center">
  <img src="https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/blob/566cc953cc98c8f9f077cfc38ee158b7227c6572/docs/Appendix_6.png"/>
</p>
