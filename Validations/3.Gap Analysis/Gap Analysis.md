#This table summarizes key evaluation parameters used to assess various AI assistant tools for senior care and daily support. It highlights common gaps observed across tools such as safety handling, instruction adherence, and personalization along with the specific tools affected and the relative impact of each issue.


| Tool                  | Key Features / Offerings                                                | Observed Limitations / Gaps                                     |
|:----------------------|:------------------------------------------------------------------------|:----------------------------------------------------------------|
| SeniorTalk            | • AI chatbot designed for seniors with speech recognition               | • Paid subscription—no free plan                                |
|                       | • Provides conversation, companionship, and scam/fraud awareness        | • No emergency detection or escalation (no 911/caregiver alert) |
|                       | • Multilingual support and customizable companion personas              | • Limited long-term memory or contextual retention              |
|                       | • Focus on mental stimulation and social engagement                     | • No built‑in reminders                                         |
|                       |                                                                         | • No daily routine tracking                                     |
| ElliQ                 | • AI-powered social robot for seniors                                   | • No built-in emergency or 911 escalation                       |
|                       | • Proactive conversations, reminders, and wellness nudges               | • Limited conversational depth (short memory)                   |
|                       | • Encourages engagement, reflection, and physical activity              | • No integration with external health or smart-home systems     |
|                       | • Voice + screen interface with expressive design                       | • High cost and hardware dependency                             |
| Sensi.AI              | • 24/7 “Care Copilot” monitoring using audio sensing                    | • Not consumer-facing (B2B only)                                |
|                       | • Detects anomalies, distress, or emotional changes                     | • No direct user interaction or companionship                   |
|                       | • Generates reports for caregivers and agencies                         | • Audio-only input—misses visual cues                           |
|                       |                                                                         | • Privacy and consent concerns                                  |
|                       |                                                                         | • Opaque interpretation of sound data                           |
| GrandPad              | • Senior-friendly tablet for video calls, photos, games, and messaging  | • No real health tracking or emergency protocol                 |
|                       | • Simplified UI and family-controlled contact list                      | • Costly device + monthly plan                                  |
|                       | • Optional “Grandie” companion chat feature                             | • Weak memory and personalization                               |
|                       |                                                                         | • Limited to proprietary ecosystem                              |
| Amazon Alexa / Alexa+ | • Voice assistant with reminders, entertainment, and smart-home control | • Requires setup and familiarity                                |
|                       | • Add-ons like Alexa Together enable elder monitoring and alerts        | • Privacy and data-sharing risks                                |
|                       | • Integrates with many third-party devices                              | • Some elder-care skills are paid or third-party                |


#This table summarizes key gaps observed in various AI chatbot tools, covering areas like safety, reasoning, and memory. It also notes the tools affected and the impact severity of each issue.


| Evaluation Parameter                          | Common Gap Observed Across Tools                                                                                                                | Tools Where Gap Observed                                                         | Impact   |
|:----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:---------|
| 1. Safety & Emergency Handling                | No escalation or confirmation protocol; tools recognized red-flag terms but failed to act (no 911 follow-up, caregiver alert, or confirmation). | Copilot, NotebookLM, Kimi, Perplexity, Grok, Gemini, ChatGPT, Meta               | High     |
| 2. Instruction Adherence (“exactly one step”) | Violated single-instruction rule; gave multiple options or open-ended suggestions.                                                              | Copilot, Perplexity, Grok, Gemini, ChatGPT, Meta                                 | Medium   |
| 3. Temporal Reasoning / Scheduling            | Inconsistent handling of time/date validation; limited ability to manage recurring or conditional schedules.                                    | Kimi, Copilot Gemini ( able to schedule reminders)                               | Medium   |
| 4. Medication Tracking & Reasoning            | Could not maintain structured logs; hallucinated or lost medication data; no duplication checks.                                                | Copilot, Kimi, Gemini, Meta                                                      | High     |
| 5. Session Memory & Personalization           | Session-level memory only; no retention of health info, preferences, or routines. Context lost after refresh.                                   | NotebookLM, Kimi, Copilot, Gemini, ChatGPT, Meta, Grok (does retain health info) | High     |
| 6. Multi-Intent Handling                      | Difficulty parsing compound or mixed-context queries; lost one intent midway.                                                                   | Copilot, Kimi                                                                    | Medium   |
| 7. Caregiver Communication & Escalation       | No structured caregiver alert, summary, or escalation path; only textual mention.                                                               | Copilot, NotebookLM, Kimi, Perplexity, Grok, Gemini, ChatGPT, Meta               | High     |
| 8. Accessibility & Session Persistence        | Context lost on refresh; no cross-session recall or persistence. Voice/visual modes limited.                                                    | NotebookLM, Kimi, Perplexity, Grok, Gemini, Meta                                 | High     |
| 9. Reliability & Stability                    | Unstable sessions; occasional resets or output truncation. No assurance of long-term state.                                                     | NotebookLM, Gemini, Meta                                                         | High     |
| 10. Tone & Empathy                            | Varying warmth; some overly factual or robotic; empathy inconsistent in longer sessions.                                                        | Gemini, Meta, Kimi                                                               | Medium   |
| 11. Transparency of Capabilities / Limits     | Most didn’t clearly disclose what they can/can’t do (e.g., scheduling, calling 911).                                                            | Copilot, NotebookLM, Perplexity, Gemini, ChatGPT, Meta, Kimi, Grok               | Medium   |
| 12. Domain Adaptability (Health / Elder Care) | Generic reasoning; failed to detect domain-specific triggers; no health safety logic or personalization.                                        | Meta, Gemini, Perplexity                                                         | High     |
| 13. Feature Limitations                       | Limited context window, premium barriers, or API quotas restricted deeper use.                                                                  | Copilot, Perplexity, Gemini, ChatGPT                                             | Medium   |
| 14. Event Focused Capabilities                | Can schedule reminders, send youtube links                                                                                                      | Everything except Gemini                                                         | Medium   |
| 15. Memory Cues                               | Fails to give accurate hints                                                                                                                    | All except Grok                                                                  | Medium   |