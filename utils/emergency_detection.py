from utils.timezone_utils import now_central
import os
from groq import Groq
from typing import Dict, Any
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmergencyDetector:
    EMERGENCY_KEYWORDS = [
        "chest pain", "breathing trouble", "shortness of breath", 
        "can't breathe", "cannot breathe", "difficulty breathing",
        "severe headache", "fainting", "unconscious", "heart attack",
        "stroke", "bleeding a lot", "suicidal", "pressure"
    ]
    
    WORSENING_KEYWORDS = ["worsening", "getting worse"]
    
    _last_alert_times = {}
    DEBOUNCE_MINUTES = 5
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
    
    def _check_keywords(self, text: str) -> Dict[str, Any]:
        """Check for emergency keywords using word boundary matching"""
        text_lower = text.lower()
        matched_phrases = []
        
        for keyword in self.EMERGENCY_KEYWORDS:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                matched_phrases.append(keyword)
        
        is_emergency = len(matched_phrases) > 0
        severity = "very_urgent" if is_emergency else "manageable"
        
        return {
            "is_emergency": is_emergency,
            "severity": severity,
            "matched_phrases": matched_phrases,
            "is_worsening": any(word in text_lower for word in self.WORSENING_KEYWORDS)
        }
    
    def _should_send_alert(self, user_id: int, is_worsening: bool) -> bool:
        """Check debounce: don't send >1 alert within 5 minutes unless worsening"""
        if is_worsening:
            return True
        
        last_alert = self._last_alert_times.get(user_id)
        if last_alert is None:
            return True
        
        time_since_last = now_central() - last_alert
        return time_since_last > timedelta(minutes=self.DEBOUNCE_MINUTES)
    
    def detect_emergency(self, text: str, user_id: int = None) -> Dict[str, Any]:
        """
        Detect if a message contains emergency health concerns using keyword matching
        Returns: {
            "is_emergency": bool,
            "severity": str ("very_urgent" or "manageable"),
            "concerns": list of detected health concerns,
            "matched_phrases": list of matched emergency keywords,
            "should_alert": bool (considering debounce logic)
        }
        """
        keyword_result = self._check_keywords(text)
        
        is_emergency = keyword_result["is_emergency"]
        matched_phrases = keyword_result["matched_phrases"]
        is_worsening = keyword_result["is_worsening"]
        severity = keyword_result["severity"]
        
        should_alert = False
        if is_emergency and user_id is not None:
            should_alert = self._should_send_alert(user_id, is_worsening)
            if should_alert:
                self._last_alert_times[user_id] = now_central()
        
        return {
            "is_emergency": is_emergency,
            "severity": severity,
            "concerns": matched_phrases,
            "matched_phrases": matched_phrases,
            "should_alert": should_alert,
            "is_worsening": is_worsening
        }
    
    def mark_alert_sent(self, user_id: int):
        """Mark that an alert was sent for this user (for debounce tracking)"""
        self._last_alert_times[user_id] = now_central()

def detect_emergency(text: str, user_id: int = None) -> Dict[str, Any]:
    """Helper function to detect emergency in text"""
    detector = EmergencyDetector()
    return detector.detect_emergency(text, user_id)
