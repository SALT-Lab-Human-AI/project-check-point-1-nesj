# Carely AI - Core Use Cases & Test Paths

This document outlines the critical user journeys and minimal test cases for the Carely AI companion. These use cases are derived from core project goals and validated against real user-bot interactions.

## 1. Critical Safety & Alerts

This is the most critical path and must be 100% reliable.

### Use Case: Critical Safety Alert (User-Triggered)

* **Description:** The user expresses clear, urgent medical distress or asks for help.
* **Chat Example(s):** "I have chest pain".
* **Expected Bot Behavior:** The bot must immediately stop all other conversational topics (like gardening) and enter a safety-first state. It must provide reassurance and explicitly state that it is notifying the caregiver on Telegram.
* **Minimal Test (e2e):**
    * `Given` a user is in a normal conversation.
    * `When` the user sends a message containing a critical trigger phrase (e.g., "I have chest pain," "I can't breathe," "I fell").
    * `Then` the bot's *immediate* response must contain a phrase like "I'm notifying your caregiver now" and reassuring language and then sends a telegram notification to the caregiver.

### Use Case: Alert Log Recall (Audit Trail)

* **Description:** The user asks for confirmation that a safety-related action was taken.
* **Chat Example(s):** "when was my caregiver last contacted?".
* **Expected Bot Behavior:** The bot must be able to query its action log (or structured memory) and recall the context of the last critical alert.
* **Minimal Test (Unit):**
    * `Given` a caregiver alert was logged at `[TIMESTAMP]` with the reason "chest pain".
    * `When` the user asks "when did you contact my caregiver?".
    * `Then` the bot's response must include both the time ("just a little while ago") and the reason ("when you were experiencing chest pain").

## 2. Medication & Routine Management

This is the most frequent and functionally important path.

### Use Case: Scheduled Medication Reminder (Proactive)

* **Description:** The bot proactively reminds the user when it is time to take a scheduled medication.
* **Chat Example(s):** "It's time for your Metformin 500mg. Take with meals to reduce stomach upset. Tap 'Log Medication' once you've taken it.".
* **Expected Bot Behavior:** The bot sends an unprompted message at the scheduled time, specifying the exact medication, dosage, and instructions.
* **Minimal Test (e2e):**
    * `Given` a user has "Metformin 500mg" scheduled for "20:00".
    * `When` the system time becomes 8:00 PM CST.
    * `Then` the bot must proactively send a reminder message to the user containing "Metformin 500mg".

### Use Case: Full Schedule Recall (User-Queried)

* **Description:** The user asks to hear their complete medication routine.
* **Chat Example(s):** "tell me entire day routine".
* **Expected Bot Behavior:** The bot retrieves all active medications and their specific times/instructions from structured memory and lists them clearly.
* **Minimal Test (Unit):**
    * `Given` the user's profile has [Lisinopril @ 09:00] and [Metformin @ 08:00, 20:00].
    * `When` the user asks "what is my routine?".
    * `Then` the response must contain "Lisinopril... 09:00" AND "Metformin... 08:00 and 20:00".


## 3. Memory & Personalization

This path defines the "companion" aspect, building trust and context.

### Use Case: Recall Personal Story (Long-Term Memory)

* **Description:** The user asks the bot to recall a specific, personal anecdote they shared in a previous conversation.
* **Chat Example(s):** "What did I tell you about my grandson's birthday gift?", "Can you tell me about plants?".
* **Expected Bot Behavior:** The bot performs a semantic search of long-term memory to find and recount the specific story about what the user gifted her grandson on his birthday.
* **Minimal Test (e2e):**
    * `Given` in a previous session, the user told a about what she gifted her grandson " blue soft toy and rose plant seeds".
    * `When` the user asks "What did I tell you about my grandson's birthday gift?".
    * `Then` the bot's response must include the keywords "grandson," "rose," and "soft toy".

### Use Case: Recall Recent Activity (Episodic Memory)

* **Description:** The user asks to be reminded of a recent event or activity.
* **Chat Example(s):** "which stall did I think of putting for the neighborhood festival?", "I cooked a curry last time and told you that, what was that curry?".
* **Expected Bot Behavior:** The bot correctly recalls facts from recent conversations, such as "muffins and zucchini crispers for the neighborhood festival" or "you cooked thai curry recently".
* **Minimal Test (e2e):**
    * `Given` the user stated "i am making muffins and zucchini crispers" for the festival.
    * `When` the user later asks "what food am I preparing for the neighborhood festival stall?".
    * `Then` the bot's response must contain "muffins and zucchini crispers".


## 4. Proactive Engagement & Wellness

This path demonstrates the bot's "proactive" and "caring" nature.

### Use Case: Proactive Event Reminder (In-Conversation)

* **Description:** During a conversation, the bot proactively reminds the user of an event scheduled for today or tomorrow.
* **Chat Example(s):** "...don't forget you have a busy day tomorrow with your Chess Club Meeting and your 45th wedding anniversary celebration...".
* **Expected Bot Behavior:** The bot injects timely reminders into its replies, demonstrating awareness of the user's schedule.
* **Minimal Test (Unit):**
    * `Given` a user has "Linda's birthday" scheduled for "tomorrow."
    * `When` the user has a general conversation.
    * `Then` the bot's response should proactively include a reminder for "Linda's birthday".

### Use Case: Guided Wellness Activity

* **Description:** The user asks for help with a wellness activity, like a breathing exercise.
* **Chat Example(s):** "can you suggest me quick relaxing exercises?", "Yes, guide me through a specific technique".
* **Expected Bot Behavior:** The bot provides a simple, actionable exercise (like the "4-7-8" method) and offers to guide the user through it.
* **Minimal Test (e2e):**
    * `When` the user asks "guide me through a breathing exercise".
    * `Then` the bot's response must include a specific, named technique (e.g., "4-7-8") and its steps.

### Use Case: Emotional Support & Empathy

* **Description:** The user expresses sadness, loneliness, or a non-urgent negative feeling.
* **Chat Example(s):** "I am feeling a bit low today", "I miss my old house and neighbors".
* **Expected Bot Behavior:** The bot responds with validation and empathy, then asks an open-ended, supportive follow-up question.
* **Minimal Test (e2e):**
    * `When` the user says "I miss my old days".
    * `Then` the bot's response must validate the feeling ("completely normal") and ask a relevant follow-up ("what specifically are you missing?").

## 5. Deterministic & Safety Queries

This path covers simple, factual queries that must be 100% accurate and safe.

### Use Case: PII Redaction & Safety

* **Description:** The user inputs highly sensitive personal data (PII/PHI).
* **Chat Example(s):** "My insurance policy is 12345678910".
* **Expected Bot Behavior:** The bot must detect the sensitive information, explicitly state that it *cannot* store or recall this information for safety, and pivot the conversation.
* **Minimal Test (e2e):**
    * `When` the user inputs "My insurance number is 98765".
    * `Then` the bot's response must state it "cannot store or recall" such details.
    * `And When` the user later asks "what is my insurance number?".
    * `Then` the bot must again refuse and explain it does not store sensitive data.

### Use Case: Get Current Time (Deterministic)

* **Description:** The user asks for the current time.
* **Chat Example(s):** "what's the time now?".
* **Expected Bot Behavior:** The bot bypasses the LLM and returns the exact system time with the correct timezone (CST/CDT).
* **Minimal Test (Unit):**
    * `When` the user asks "what's the time now?".
    * `Then` the bot's response must be a non-generative string containing the current time and the "CDT" or "CST" timezone.
	
## 6. Accessibility Features

This path covers audio-based interactions for accessibility.

### Use Case: Voice to Text (Speech Input)

* **Description:** The user clicks the microphone button and speaks their message instead of typing.
* **Expected Bot Behavior:** The `streamlit_mic_recorder` component captures the audio, transcribes it to an English string, and populates the chat input. The message is then sent as if it were typed.
* **Minimal Test (e2e):**
    * `Given` the user's chat input box is empty.
    * `When` the user clicks the "🎤" button and says "Hello Carely".
    * `Then` the `voice_text` variable must be populated with "Hello Carely" and a new user message "🎤 Hello Carely" must appear in the chat history.

### Use Case: Text to Voice (Audio Output)

* **Description:** The user clicks the "🔊" (listen) button next to any of the bot's chat messages.
* **Expected Bot Behavior:** The bot's text response is sent to the `utils.tts_helper` (`generate_speech_audio` function). An `st.audio` player appears directly under the message and automatically plays the generated speech.
* **Minimal Test (e2e):**
    * `Given` a bot response "Your next Metformin is due at 08:00 PM CDT." is on the screen.
    * `When` the user clicks the "🔊" button next to that message.
    * `Then` the `st.session_state.playing_audio` variable must be set.
    * `And` an `st.audio` component must render and autoplay the spoken version of that exact text.

## 7. Quick Actions (Button-Triggered)

This path covers the non-verbal, button-based interactions from the main chat UI.

### Use Case: Log Medication Button

* **Description:** The user clicks the "Log Medication" button instead of typing.
* **Expected Bot Behavior:** The bot triggers the `log_medication` action. If a medication reminder was just sent, it logs that specific medication. If the context is unclear, it asks "Which medication did you take?".
* **Minimal Test (e2e):**
    * `Given` the bot just sent a reminder for "Metformin".
    * `When` the user clicks the "Log Medication" button.
    * `Then` the bot's response must be a confirmation, e.g., "Got it! I've logged your Metformin for today."

### Use Case: Play Music Button

* **Description:** The user clicks the "Play Music" button.
* **Expected Bot Behavior:** The bot immediately provides a message containing a link to a pre-selected, relaxing YouTube music video.
* **Minimal Test (e2e):**
    * `When` the user clicks the "Play Music" button.
    * `Then` the bot's response must contain a message like "Here's your favorite music" and a valid `youtube.com` URL that could be played without leaving the chat interface.

### Use Case: Fun Corner Button

* **Description:** The user clicks the "Fun Corner" button for light entertainment.
* **Expected Bot Behavior:** The bot responds with a pre-selected joke or puzzle from its internal list.
* **Minimal Test (e2e):**
    * `When` the user clicks the "Fun Corner" button.
    * `Then` the bot's response must be a joke or a puzzle/riddle.

### Use Case: Memory Cue Button

* **Description:** The user clicks the "Memory Cue" button to request a cognitive prompt.
* **Expected Bot Behavior:** The bot generates a gentle, personalized question based on the user's structured memory (e.g., medications, family events, or routines).
* **Minimal Test (e2e):**
    * `When` the user clicks the "Memory Cue" button.
    * `Then` the bot's response must be a question referencing their personal data, like "Do you remember what medication you take in the morning?" or "What's your favorite memory from this week?".

### Use Case: Memory Game Button

* **Description:** The user clicks the "Memory Game" button.
* **Expected Bot Behavior:** This is a UI-only action. The chat interface is hidden and the Streamlit "Memory Card Game" UI is displayed.
* **Minimal Test (e2e):**
    * `When` the user clicks the "Memory Game" button.

    * `Then` the `st.session_state.show_memory_game` must be set to `True` and the chat container must be replaced by the game board UI.

