# Carely - Senior-Friendly AI Companion App
## Design Specification Document

<img src="Expanded_designdiagram.png" alt="Carely Flow Diagram" width="800">
---

## 1. Executive Summary

**Product Name:** Carely  
**Target Audience:** Senior citizens  
**Purpose:** An AI-powered companion app designed to help seniors manage medications, track health, communicate with an empathetic AI assistant, and maintain overall wellness through an accessible, senior-friendly interface.

## 2. Core Principles
- **Accessibility First:** Large buttons, clear typography (18px base), high contrast
- **Simplicity:** Streamlined workflows, minimal cognitive load
- **Empathy:** Warm, conversational tone with safety-first features
- **Trust:** Transparent interactions, clear labeling, consistent patterns

---

## 3. User Journeys

### 3.1 First-Time User Journey

**Scenario:** Margaret, 72, downloads Carely to help manage her medications. 

```
Entry → Sign Up → 9-Step Onboarding → Main App (Overview)
```

**Steps:**
1. **Welcome Screen (Login)**
   - Large "Sign Up" button prominently displayed
   - Demo credentials shown for testing

2. **Sign Up Form**
   - Simple 3-field form (Name, Email, Password)
   - Clear error messages
   - Large "Create Account" button

3. **Onboarding Wizard (9 Steps)**
   - Progress indicator at top
   - One question per screen
   - Large, clear navigation buttons
   
   **Step Breakdown:**
   - Step 1: Preferred name
   - Step 2: Age
   - Step 3: Health conditions (multi-select)
   - Step 4: Current medications
   - Step 5: Mobility level
   - Step 6: Emergency contact
   - Step 7: Daily routine preferences
   - Step 8: Notification preferences
   - Step 9: Completion summary

4. **First App Launch**
   - Lands on Overview tab
   - Sees personalized greeting
   - Left nav bar with different tabs for different actions

### 3.2 Daily User Journey

**Scenario:** Daily interaction with Carely

```
Login → Overview Dashboard → Quick Actions → Specific Tasks → Log Out
```

**Morning Flow:**
1. Open app (auto-login if enabled)
2. See morning medication reminder banner
3. Mark medication as taken or snooze
4. Check today's schedule
5. Log morning mood if desired

**Throughout Day:**
1. Receive medication reminders
2. Chat with Carely for questions, ask for riddles,puzzles, recommend music, stretch guides etc
3. View health insights
4. Add appointments as needed

### 3.3 Medication Management Journey

**Scenario:** Adding and managing medications

```
Overview/Medications Tab → Add Medication → Configure Schedule → Track Adherence
```

**Steps:**
1. Navigate to Medications tab or click "Add Medication" quick action
2. Fill out medication form:
   - Medication name
   - Dosage
   - Frequency (daily, multiple times, as needed)
   - Time(s) of day
   - Refill reminder (optional)
3. Save medication
4. Receive reminders at scheduled times
5. Mark as taken/snooze from banner or medications tab
6. View adherence statistics on Overview

### 3.4 AI Chat Interaction Journey

**Scenario:** Asking Carely for help

```
Chat Tab → Ask Question/Quick Action → AI Response → Follow-up or Exit
```

**Examples:**

**Example 1: Music Request**
1. Click "Chat" in sidebar
2. Click "Play music" quick action
3. Receive response with 3 embedded YouTube videos based on user likings
4. Watch/enjoy music
5. Continue conversation if desired

**Example 2: Health Question**
1. Type question: "I have a headache, what should I do?"
2. Carely provides empathetic response
3. If safety trigger detected → Safety dialog appears
4. Offers emergency services or trusted contact options

**Example 3: Medication Question**
1. Click "Log medication" quick action
2. AI confirms which medication
3. Navigate to medications tab or mark as taken

### 3.5 Safety Alert Journey

**Scenario:** User expresses concerning symptoms

```
Chat Message → Safety Trigger Detection → Safety Assessment Dialog → Resource Offering
```

**Steps:**
1. User types concerning message (e.g., "I'm feeling dizzy and my chest hurts")
2. AI detects safety trigger
3. Safety sheet appears with three steps:
   - **Assess:** "This could be serious. How severe is it?"
   - **Resources:** Options for emergency services, trusted contact
   - **Confirmation:** "Help is on the way" or "Feeling better"
4. User selects appropriate action
5. System provides contact information or confirmation

---

## 4. Task Flows

### 4.1 Logging Daily Mood

```
[Overview Tab] 
    ↓
[Click "Log Mood" button]
    ↓
[Mood Log Dialog Opens]
    ↓
[Select Mood: Good/Okay/Low]
    ↓
[Add Optional Notes]
    ↓
[Click "Log Mood" button]
    ↓
[Success Toast] → [Dialog Closes]
    ↓
[Mood appears in weekly trend]
```

**UI Elements:**
- Three large mood buttons with icons (Smile, Meh, Frown)
- Color-coded: Green (Good), Orange (Okay), Gray (Low)
- Optional textarea for notes
- Clear Cancel/Submit buttons

### 4.2 Adding an Appointment

```
[Top App Bar or Overview Quick Actions]
    ↓
[Click "New Appointment"]
    ↓
[Appointment Dialog Opens]
    ↓
[Fill Form]
    ├── Appointment Title
    ├── Date (Calendar picker)
    ├── Time (Time picker)
    ├── Location (Optional)
    └── Notes (Optional)
    ↓
[Click "Save Appointment"]
    ↓
[Success Toast] → [Dialog Closes]
    ↓
[Appointment appears in Today's Schedule]
```

### 4.3 Taking Medication

**Scenario A: From Overview Banner**
```
[Medication Due Banner appears]
    ↓
[Click "I took it" button]
    ↓
[Success Toast with Undo option]
    ↓
[Banner dismisses]
    ↓
[Adherence stats update]
```

**Scenario B: From Medications Tab**
```
[Navigate to Medications Tab]
    ↓
[Find due medication (highlighted)]
    ↓
[Click "Mark as Taken"]
    ↓
[Confirmation Toast]
    ↓
[Status updates to "Taken"]
```

### 4.4 Chatting with Carely

**Quick Action Flow:**
```
[Chat Tab]
    ↓
[Click Quick Suggestion Button]
    ├── "Play music" → Embedded video responses
    ├── "Guide stretch" → Guided routine
    ├── "Log medication" → Navigate to medications
    └── "Call Family" → Contact suggestions
    ↓
[AI Response Generated]
    ↓
[Continue Conversation or Exit]
```

**Free-Form Chat Flow:**
```
[Chat Tab]
    ↓
[Type message in input]
    ↓
[Click Send or Press Enter]
    ↓
[Message appears in chat]
    ↓
[Typing indicator shows]
    ↓
[AI Response appears]
    ├── Normal response → Conversation continues
    └── Safety trigger → Safety dialog appears
```

### 4.5 Viewing Health Insights

```
[Navigate to Health Insights Tab]
    ↓
[View Dashboard Cards]
    ├── Medication Adherence Trend (7-day chart)
    ├── Mood Patterns (Weekly visualization)
    └── Appointment History
    ↓
[Click specific card for details]
    ↓
[Expanded view with more data]
    ↓
[Return to dashboard]
```


### 4.6 Managing Alerts

```
[Navigate to Alerts Tab]
    ↓
[View Active Reminders List]
    ├── Medication reminders
    ├── Appointment reminders
    ├── Refill reminders
    └── Custom reminders
    ↓
[Take Action]
    ├── Toggle reminder on/off
    ├── Edit reminder settings
    ├── Delete reminder
    └── Snooze reminder
```

---

## 5. Key Screens & Interactions

### 5.1 Authentication Screens

#### Login Screen
**Layout:**
- Centered card (max-width: 400px)
- Carely branding at top
- Welcome message
- Email and password fields
- Large "Login" button (primary)
- "Forgot password?" link
- "Sign Up" button (outline)
- Demo credentials hint

**Interactions:**
- Form validation on submit
- Loading state during authentication
- Error messages below form
- Success → Navigate to app or onboarding

#### Sign Up Screen
**Layout:**
- Similar structure to login
- Additional "Full Name" field
- Password strength indicator
- Terms & conditions checkbox
- "Create Account" button
- "Back to Login" link

**Interactions:**
- Real-time validation
- Clear error messages
- Success → Navigate to onboarding

### 5.2 Onboarding Wizard

**Layout:**
- Full-screen wizard
- Progress bar at top (9 steps)
- Large step title
- Question/input in center
- Navigation buttons at bottom (Back/Next/Skip)

**Step-Specific Interactions:**

**Step 1: Preferred Name**
- Single text input
- Friendly greeting

**Step 2: Age**
- Number input or select dropdown
- Age-appropriate messaging

**Step 3: Health Conditions**
- Multi-select checkboxes
- Common conditions listed
- "Other" option with text input

**Step 4: Current Medications**
- Dynamic list (Add/Remove)
- Medication name + dosage fields
- "I don't take any" option

**Step 5: Mobility Level**
- Radio buttons or slider
- Options: Fully mobile, Some assistance, Limited mobility

**Step 6: Emergency Contact**
- Name, relationship, phone number
- Validation for phone format

**Step 7: Daily Routine**
- Time preferences (wake up, meals, bedtime)
- Helps schedule medication reminders

**Step 8: Notifications**
- Toggle switches for different notification types
- Medication reminders, appointments, health tips

**Step 9: Summary**
- Review entered information
- "Complete Setup" button
- Celebration message on completion

### 5.3 Main Application Layout

**Structure:**
```
┌─────────────────────────────────────────────┐
│              Top App Bar                     │
│  [Page Title]        [Quick Action Buttons] │
├──────────┬──────────────────────────────────┤
│          │                                   │
│ Sidebar  │        Main Content Area         │
│          │                                   │
│  [Nav]   │     [Tab-Specific Content]       │
│  [User]  │                                   │
│          │                                   │
└──────────┴──────────────────────────────────┘
```

**Sidebar:**
- Fixed left column (260px wide)
- User profile section at top
- 5 navigation items with icons:
  - Overview (Home icon)
  - Chat (MessageCircle icon)
  - Medications (Pill icon)
  - Health Insights (Activity icon)
  - Alerts (Bell icon)
- Active state: Primary color background, white text
- Hover state: Muted background

**Top App Bar:**
- Fixed header (64px height)
- Current page title and date
- Three quick action buttons:
  - Add Med (Plus icon)
  - Log Mood (Heart icon)
  - New Appointment (Calendar icon)

### 5.4 Overview Tab (Dashboard)

**Sections (Top to Bottom):**

1. **Welcome Banner**
   - Personalized greeting (time-aware)
   - User's preferred name
   - Primary/accent color background

2. **Medication Due Banner** (conditional)
   - Only shows when medication is due
   - Warning color scheme
   - Medication name and due time
   - "I took it" and "Snooze" buttons
   - Dismissible

3. **Two-Column Grid (Desktop)**

   **Left Column:**
   - **Medication Adherence Card**
     - Weekly percentage (large number)
     - Progress bar
     - Current streak (days)
     - Total medications count
     - "View Details" button → Medications tab

   **Right Column:**
   - **Mood Log Card**
     - 7-day mood visualization (circles)
     - Color-coded: Green (good), Orange (okay), Gray (low)
     - Trend indicator
     - "Log Mood" button → Opens dialog

4. **Today's Schedule Card**
   - List of medications and appointments
   - Each item shows:
     - Icon (Pill or Calendar)
     - Name/title
     - Time
     - Status badge (Taken, Due, Upcoming)
   - Due items have action buttons
   - Time-sorted

5. **Recent Conversations Card**
   - Last 3 chat summaries
   - Timestamp for each
   - "Open Chat" button → Chat tab

6. **Quick Actions Card**
   - Grid of 5 large buttons:
     - Log Mood (Heart icon)
     - Add Medication (Pill icon)
     - Add Appointment (Calendar icon)
     - Start Stretch (Dumbbell icon)
     - Play Music (Music icon)
   - 80px tall buttons with icon + label

**Responsive Behavior:**
- Desktop: Two-column grid
- Tablet/Mobile: Single column stack

### 5.5 Chat Tab

**Layout:**
```
┌─────────────────────────────────────────┐
│         Chat Header                      │
│  "How can I help you today?"            │
├─────────────────────────────────────────┤
│                                          │
│         Message Thread                   │
│  [AI Avatar] AI Message                  │
│             User Message [Avatar]        │
│  [AI Avatar] AI Message                  │
│             ... with videos if music     │
│                                          │
├─────────────────────────────────────────┤
│     Quick Suggestion Chips               │
│  [Play music] [Guide stretch] [Log med] │
├─────────────────────────────────────────┤
│         Message Input                    │
│  [Text Input]               [Send Icon] │
└─────────────────────────────────────────┘
```

**Key Features:**

1. **Message Bubbles**
   - AI messages: Left-aligned, muted background, Carely avatar
   - User messages: Right-aligned, primary color, no avatar
   - Timestamps shown
   - Urgent messages: Warning color border

2. **Video Embeds** (Music Feature)
   - Embedded YouTube iframe players
   - 16:9 aspect ratio
   - Title below each video
   - Appears in AI response bubble

3. **Quick Suggestion Chips**
   - 4 action buttons above input
   - Triggers contextual AI responses
   - "Play music" → Shows videos
   - "Guide stretch" → Routine instructions
   - "Log medication" → Navigation prompt
   - "Call Family" → Contact suggestions

4. **Safety Features**
   - Trigger words detection (medical emergencies, emotional distress)
   - Urgent message styling
   - Safety assessment dialog with 3 steps:
     - Assess severity
     - Offer resources (911, doctor, trusted contact)
     - Confirmation

5. **Typing Indicator**
   - Animated dots when AI is responding
   - Appears at bottom of message thread

6. **Voice Input** (Future consideration)
   - Microphone icon in input area

### 5.6 Medications Tab

**Layout:**

1. **Statistics Banner**
   - Weekly adherence percentage
   - Current streak
   - Quick stats

2. **Add Medication Button**
   - Prominent at top
   - Primary color, large size

3. **Medications List**
   - Grouped by frequency:
     - Daily medications
     - Multiple times daily
     - As needed
   
   **Each Medication Card:**
   - Medication name (large, bold)
   - Dosage
   - Frequency and times
   - Next dose indicator
   - Status: Taken (green check), Due (orange), Upcoming
   - Action buttons:
     - Mark as Taken
     - Snooze
     - Edit
     - Delete
   - Refill reminder if applicable

4. **Add/Edit Medication Form**
   - Can be dialog or inline form
   - Fields:
     - Medication name
     - Dosage
     - Form (pill, liquid, injection, etc.)
     - Frequency selector
     - Time picker(s)
     - Start date
     - Refill reminder (checkbox + days)
     - Notes (optional)
   - Save/Cancel buttons

5. **Adherence Calendar** (Optional view)
   - Monthly calendar
   - Color-coded days based on adherence
   - Click date for details

**Interactions:**
- Swipe to mark as taken (mobile)
- Long press for options (mobile)
- Hover states on desktop
- Confirmation dialogs for delete

### 5.7 Health Insights Tab

**Layout:**

1. **Overview Cards Grid**

   **Card 1: Medication Adherence Trend**
   - 7-day bar chart (Recharts)
   - Percentage per day
   - Average line
   - Color: Primary blue

   **Card 2: Mood Patterns**
   - 7-day line chart
   - Good/Okay/Low values
   - Color-coded points
   - Trend indicator

   **Card 3: Hydration Tracking**
   - Daily water intake
   - Goal vs. actual
   - Progress bar
   - "Log Water" quick action

   **Card 4: Appointment History**
   - List of past appointments
   - Click to view notes
   - Upcoming count

2. **Filters/Date Range Selector**
   - Week, Month, Quarter views
   - Date picker for custom range

3. **Export/Share Options**
   - Print summary
   - Email to doctor
   - PDF export

**Data Visualization:**
- Recharts library for charts
- Accessible color palette
- Large, readable axis labels
- Tooltips on hover
- Legend when needed

**Notable Exclusions:**
- No step counter
- No exercise tracking
- No weight/BMI tracking
- Focus on medication, mood, hydration, appointments only

### 5.8 Alerts & Reminders Tab

**Layout:**

1. **Active Reminders Section**
   - Toggle to view active vs. all
   
   **Each Reminder Card:**
   - Type icon (Pill, Calendar, Droplet, Bell)
   - Reminder title
   - Schedule/frequency
   - Next reminder time
   - Toggle switch (on/off)
   - Edit and Delete buttons

2. **Reminder Types:**
   - **Medication Reminders**
     - Auto-generated from medications
     - Cannot delete (linked to medication)
     - Can snooze or disable
   
   - **Appointment Reminders**
     - Auto-generated from appointments
     - Can customize timing (15 min, 1 hour, 1 day before)
   
   - **Refill Reminders**
     - Linked to medications
     - Customizable days before refill
   
   - **Custom Reminders**
     - User-created
     - Flexible scheduling
     - Can set recurring or one-time

3. **Add Custom Reminder Form**
   - Title
   - Type selector
   - Date and time
   - Repeat options (daily, weekly, monthly, custom)
   - Notification preferences
   - Notes

4. **Notification History**
   - Log of past notifications
   - Status: Acknowledged, Snoozed, Dismissed
   - Searchable

**Interactions:**
- Quick toggle on/off without confirmation
- Edit opens dialog
- Delete requires confirmation
- Snooze options: 15 min, 30 min, 1 hour, 4 hours

### 5.9 Dialogs & Modals

#### Mood Log Dialog
- Modal overlay
- Centered dialog (max-width: 450px)
- Title: "How are you feeling today?"
- 3 large mood buttons (Good/Okay/Low)
- Optional notes textarea
- Cancel and "Log Mood" buttons

#### Appointment Dialog
- Similar layout to Mood Log
- Title: "Add New Appointment"
- Form fields:
  - Appointment title (required)
  - Date picker (calendar component)
  - Time picker
  - Location (optional)
  - Notes (optional textarea)
- Save and Cancel buttons

#### Safety Assessment Sheet
- Bottom sheet (mobile) or modal (desktop)
- 3-step wizard:
  
  **Step 1: Assess**
  - Warning icon
  - Message: "This could be serious. How severe is it?"
  - Options: Very urgent, Somewhat urgent, Manageable
  
  **Step 2: Resources**
  - Based on severity:
    - Very urgent: "Call 911" button
    - Somewhat: "Call Doctor" with number
    - Manageable: "Contact Trusted Person" with list
  - Alternative actions below
  
  **Step 3: Confirmation**
  - "Help is on the way" or "Are you feeling better?"
  - Option to return to chat

---

---


### 6. Planned Features

**Voice Interaction:**
- Voice commands for hands-free use
- Voice input in chat
- Text-to-speech for AI responses


---

## 7. Technical Specifications

### 7.1 Tech Stack

**Frontend:**
-Streamlit
- Tailwind CSS v4.0
- Plotly (Express + Graph Objects)


**Key Libraries:**
- app.scheduling.reminder_scheduler
- date-fns or similar (date handling)
- YouTube embed library (for video responses)

## Conclusion

**Document Version:** 1.0  
**Last Updated:** October 9, 2025  
**Maintained By:** Carely Design Team NESJ 
