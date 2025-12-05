"""
Medication Safety Guardrails Module

This module provides safety filters to prevent the AI from recommending or naming
specific medications, dosages, or treatment advice. It includes:

1. Pre-processing: Detect when users ask for medication recommendations
2. Post-processing: Filter out any medication names/dosages from AI responses
3. Safe response templates for medication-related queries

SAFETY RULES:
- Never recommend specific medications (prescription or OTC)
- Never mention brand names or generic drug names  
- Never provide dosage information
- Always redirect to healthcare professionals
- Flag emergency symptoms for immediate care
"""

import re
from typing import Dict, Any, List, Tuple

# ============================================
# MEDICATION & DRUG PATTERN LISTS
# ============================================

# Common OTC and prescription drug names (partial list - expand as needed)
MEDICATION_NAMES = [
    # Pain relievers / Fever reducers
    "acetaminophen", "tylenol", "paracetamol", "ibuprofen", "advil", "motrin",
    "aspirin", "bayer", "naproxen", "aleve", "excedrin", "panadol",
    
    # Cold/Flu/Allergy
    "benadryl", "diphenhydramine", "zyrtec", "cetirizine", "claritin", "loratadine",
    "allegra", "fexofenadine", "sudafed", "pseudoephedrine", "dayquil", "nyquil",
    "robitussin", "mucinex", "dextromethorphan", "guaifenesin", "theraflu",
    
    # Stomach/Digestive
    "pepto bismol", "pepto-bismol", "tums", "antacid", "prilosec", "omeprazole",
    "nexium", "pepcid", "famotidine", "zantac", "ranitidine", "imodium", "loperamide",
    "miralax", "dulcolax", "laxative", "gas-x", "simethicone", "dramamine",
    
    # Sleep aids
    "melatonin", "unisom", "zzzquil", "ambien", "zolpidem", "lunesta",
    
    # Antibiotics (should never recommend)
    "amoxicillin", "penicillin", "azithromycin", "zithromax", "z-pack", "ciprofloxacin",
    "cipro", "doxycycline", "metronidazole", "flagyl", "cephalexin", "keflex",
    
    # Heart/Blood pressure
    "lisinopril", "metoprolol", "atenolol", "amlodipine", "losartan", "hydrochlorothiazide",
    
    # Diabetes
    "metformin", "insulin", "glipizide", "januvia",
    
    # Mental health
    "prozac", "fluoxetine", "zoloft", "sertraline", "lexapro", "xanax", "alprazolam",
    "valium", "diazepam", "ativan", "lorazepam", "wellbutrin", "bupropion",
    
    # Cholesterol
    "lipitor", "atorvastatin", "crestor", "rosuvastatin", "simvastatin", "zocor",
    
    # Other common
    "prednisone", "gabapentin", "tramadol", "hydrocodone", "oxycodone", "codeine",
    "viagra", "cialis", "synthroid", "levothyroxine", "warfarin", "coumadin",
]

# Dosage-related patterns
DOSAGE_PATTERNS = [
    r'\b\d+\s*mg\b',           # 400mg, 200 mg
    r'\b\d+\s*ml\b',           # 5ml, 10 ml
    r'\b\d+\s*mcg\b',          # 100mcg
    r'\b\d+\s*gram\b',         # 1 gram
    r'\b\d+\s*g\b',            # 500g
    r'\b\d+\s*cc\b',           # 5cc
    r'\btake\s+\d+\b',         # take 2
    r'\b\d+\s*tablet',         # 2 tablets
    r'\b\d+\s*pill',           # 1 pill
    r'\b\d+\s*capsule',        # 2 capsules
    r'\b\d+\s*dose',           # 1 dose
    r'\btwice\s+(a\s+)?day\b', # twice a day
    r'\bthree\s+times\s+(a\s+)?day\b',
    r'\bevery\s+\d+\s*hour',   # every 4 hours
    r'\b\d+\s*times\s+(a\s+|per\s+)?day\b',  # 3 times a day
    r'\bonce\s+daily\b',
    r'\btwice\s+daily\b',
    r'\bmorning\s+and\s+(evening|night)\b',
]

# Keywords indicating user is asking for medication advice
MEDICATION_ADVICE_KEYWORDS = [
    "what medicine", "what medication", "which medicine", "which medication",
    "what drug", "which drug", "what pill", "which pill",
    "what should i take", "what can i take", "what do i take",
    "should i take", "can i take", "is it ok to take", "is it okay to take",
    "recommend", "suggest", "prescribe", "prescription",
    "what helps", "what helps with", "what's good for",
    "how much", "how many", "dosage", "dose",
    "over the counter", "otc", "pharmacy",
    "treat", "treatment for", "cure for", "remedy",
    "painkiller", "pain killer", "pain relief", "pain reliever",
    "antibiotic", "antacid", "anti-inflammatory",
]

# Emergency symptoms requiring immediate medical attention
EMERGENCY_SYMPTOMS = [
    "chest pain", "heart attack", "can't breathe", "cannot breathe",
    "difficulty breathing", "shortness of breath", "stroke",
    "severe bleeding", "unconscious", "fainting", "seizure",
    "suicidal", "suicide", "want to die", "end my life",
    "severe allergic", "anaphylaxis", "swelling throat",
    "numbness", "paralysis", "sudden confusion",
    "severe headache", "worst headache", "sudden vision loss",
    "coughing blood", "vomiting blood",
]


# ============================================
# PRE-PROCESSING: Detect Medication Queries
# ============================================

def is_asking_for_medication_advice(user_message: str) -> Tuple[bool, List[str]]:
    """
    Detect if user is asking for medication recommendations or advice.
    
    Returns:
        Tuple of (is_asking, matched_keywords)
    """
    message_lower = user_message.lower()
    matched_keywords = []
    
    for keyword in MEDICATION_ADVICE_KEYWORDS:
        if keyword in message_lower:
            matched_keywords.append(keyword)
    
    is_asking = len(matched_keywords) > 0
    
    return is_asking, matched_keywords


def detect_emergency_symptoms(user_message: str) -> Tuple[bool, List[str]]:
    """
    Detect if user is describing emergency symptoms.
    
    Returns:
        Tuple of (is_emergency, matched_symptoms)
    """
    message_lower = user_message.lower()
    matched_symptoms = []
    
    for symptom in EMERGENCY_SYMPTOMS:
        if symptom in message_lower:
            matched_symptoms.append(symptom)
    
    is_emergency = len(matched_symptoms) > 0
    
    return is_emergency, matched_symptoms


# ============================================
# POST-PROCESSING: Filter AI Response
# ============================================

def contains_medication_names(text: str) -> Tuple[bool, List[str]]:
    """
    Check if text contains any medication/drug names.
    
    Returns:
        Tuple of (contains_meds, found_medications)
    """
    text_lower = text.lower()
    found_medications = []
    
    for med in MEDICATION_NAMES:
        pattern = r'\b' + re.escape(med) + r'\b'
        if re.search(pattern, text_lower):
            found_medications.append(med)
    
    return len(found_medications) > 0, found_medications


def contains_dosage_info(text: str) -> Tuple[bool, List[str]]:
    """
    Check if text contains dosage information.
    
    Returns:
        Tuple of (contains_dosage, found_patterns)
    """
    found_patterns = []
    
    for pattern in DOSAGE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_patterns.extend(matches)
    
    return len(found_patterns) > 0, found_patterns


def filter_medication_content(ai_response: str) -> Tuple[str, bool, Dict[str, Any]]:
    """
    Post-process AI response to remove any medication names or dosage info.
    
    Returns:
        Tuple of (filtered_response, was_filtered, details)
    """
    has_meds, found_meds = contains_medication_names(ai_response)
    has_dosage, found_dosage = contains_dosage_info(ai_response)
    
    was_filtered = has_meds or has_dosage
    
    details = {
        "found_medications": found_meds,
        "found_dosage_patterns": found_dosage,
        "was_filtered": was_filtered
    }
    
    if was_filtered:
        # Replace with safe response
        filtered_response = get_safe_medication_response()
        return filtered_response, True, details
    
    return ai_response, False, details


# ============================================
# SAFE RESPONSE TEMPLATES
# ============================================

def get_safe_medication_response(is_emergency: bool = False, symptoms: List[str] = None) -> str:
    """
    Generate a safe, empathetic response that declines medication advice.
    """
    if is_emergency and symptoms:
        symptom_str = ", ".join(symptoms[:2])
        return f"""I'm really concerned about what you're describing ({symptom_str}). This sounds like it needs immediate medical attention.

Please call 911 or your local emergency number right away, or have someone take you to the nearest emergency room.

I'm here with you. While you wait for help, try to stay calm and comfortable. I'm notifying your caregiver now.

Is there anything else I can do to help you feel more comfortable right now?"""

    return """I understand you're not feeling well, and I really wish I could help more. However, I'm not able to recommend specific medications or dosages - that's something only a doctor, nurse practitioner, or pharmacist can safely do.

Here's what I'd suggest:
- For non-urgent concerns, please reach out to your doctor's office or a pharmacist
- For after-hours care, consider calling a nurse hotline or visiting urgent care
- If you're experiencing severe symptoms, please don't hesitate to call 911

I care about your wellbeing and want to make sure you get the right help. Is there anything else I can do to support you right now? I'm happy to help you remember to call your doctor or just chat to keep you company."""


def get_medication_safety_system_prompt_addition() -> str:
    """
    Returns additional system prompt text to reinforce medication safety.
    """
    return """
CRITICAL MEDICATION SAFETY RULES (NEVER VIOLATE):
1. NEVER recommend or name specific medications (prescription OR over-the-counter)
2. NEVER mention drug brand names (Tylenol, Advil, etc.) or generic names (acetaminophen, ibuprofen, etc.)
3. NEVER provide dosage information (mg, ml, "take 2 pills", "twice a day", etc.)
4. NEVER suggest treatments, remedies, or "what helps" for symptoms
5. If a user asks what medicine to take, politely decline and redirect to a doctor, pharmacist, or urgent care
6. For emergency symptoms (chest pain, difficulty breathing, suicidal thoughts), tell user to call 911 immediately
7. You may discuss the user's ALREADY PRESCRIBED medications from their schedule (reminder purposes only)
8. You may NOT advise on whether to take more, less, or different medications than prescribed

When users ask for medication advice, respond with empathy, acknowledge their discomfort, 
clearly state you cannot provide medication recommendations, and encourage them to contact 
a healthcare professional (doctor, pharmacist, nurse hotline, or urgent care).
"""


# ============================================
# MAIN SAFETY CHECK FUNCTION
# ============================================

def apply_medication_safety_guardrails(
    user_message: str,
    ai_response: str = None
) -> Dict[str, Any]:
    """
    Main function to apply all medication safety guardrails.
    
    Call this:
    1. Before LLM call: Check if user is asking for medication advice
    2. After LLM call: Filter response for any medication content
    
    Args:
        user_message: The user's input message
        ai_response: The AI's response (optional, for post-processing)
    
    Returns:
        Dictionary with safety analysis and filtered response
    """
    result = {
        "is_medication_query": False,
        "is_emergency": False,
        "should_use_safe_response": False,
        "safe_response": None,
        "original_response_filtered": False,
        "filtered_response": ai_response,
        "details": {}
    }
    
    # Pre-processing: Check user message
    is_med_query, med_keywords = is_asking_for_medication_advice(user_message)
    is_emergency, emergency_symptoms = detect_emergency_symptoms(user_message)
    
    result["is_medication_query"] = is_med_query
    result["is_emergency"] = is_emergency
    result["details"]["matched_medication_keywords"] = med_keywords
    result["details"]["matched_emergency_symptoms"] = emergency_symptoms
    
    # If user is asking for medication advice, prepare safe response
    if is_med_query:
        result["should_use_safe_response"] = True
        result["safe_response"] = get_safe_medication_response(is_emergency, emergency_symptoms)
    
    # Post-processing: Filter AI response if provided
    if ai_response:
        filtered, was_filtered, filter_details = filter_medication_content(ai_response)
        result["filtered_response"] = filtered
        result["original_response_filtered"] = was_filtered
        result["details"].update(filter_details)
        
        # If response was filtered, it means AI gave medication advice despite instructions
        if was_filtered:
            result["should_use_safe_response"] = True
            result["safe_response"] = filtered
    
    print(f"MEDICATION SAFETY DEBUG: query={is_med_query}, emergency={is_emergency}, filtered={result.get('original_response_filtered', False)}")
    
    return result
