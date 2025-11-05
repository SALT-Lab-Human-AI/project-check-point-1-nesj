from utils.timezone_utils import now_central
import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def send_message(self, chat_id: str, message: str, parse_mode: str = "HTML") -> Dict[str, Any]:
        """
        Send a message to a Telegram chat
        
        Args:
            chat_id: Telegram chat ID
            message: Message text to send
            parse_mode: Message format (HTML or Markdown)
            
        Returns:
            Response from Telegram API
        """
        if not self.bot_token:
            return {"success": False, "error": "Telegram bot token not configured"}
            
        if not chat_id:
            return {"success": False, "error": "Chat ID not provided"}
            
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("ok"):
                return {"success": True, "message_id": result.get("result", {}).get("message_id")}
            else:
                return {"success": False, "error": result.get("description", "Unknown error")}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_emergency_alert(
        self, 
        chat_id: str, 
        patient_name: str, 
        concerns: list, 
        severity: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Send an emergency alert to a caregiver
        
        Args:
            chat_id: Caregiver's Telegram chat ID
            patient_name: Name of the patient
            concerns: List of health concerns detected
            severity: Severity level (very_urgent or manageable)
            message: Original message from patient
            
        Returns:
            Response from Telegram API
        """
        matched_phrase = ", ".join(concerns) if concerns else "Unknown symptoms"
        severity_display = "🔴 Very Urgent" if severity == "very_urgent" else "⚠️ Manageable"
        
        alert_message = f"""
<b>From: Carely (Emergency Alert)</b>
<b>User:</b> {patient_name}
💬 <b>Reported Symptoms:</b> {matched_phrase}
⚠️ <b>Severity:</b> {severity_display}

Please take immediate action.
Carely has started first-level comfort and monitoring responses for the user.
"""
        
        return self.send_message(chat_id, alert_message, parse_mode="HTML")
    
    def _get_current_time(self) -> str:
        """Get current time in readable format"""
        from datetime import datetime
        return now_central().strftime("%I:%M %p, %B %d, %Y")

def send_emergency_alert(
    chat_id: str,
    patient_name: str,
    concerns: list,
    severity: str,
    message: str
) -> Dict[str, Any]:
    """Helper function to send emergency alert"""
    notifier = TelegramNotifier()
    return notifier.send_emergency_alert(chat_id, patient_name, concerns, severity, message)

def send_telegram_message(chat_id: str, message: str) -> Dict[str, Any]:
    """Helper function to send a simple Telegram message"""
    notifier = TelegramNotifier()
    return notifier.send_message(chat_id, message)
