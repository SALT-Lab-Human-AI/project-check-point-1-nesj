import os
import requests
from typing import Dict, Any, Optional

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
            severity: Severity level (low, medium, high)
            message: Original message from patient
            
        Returns:
            Response from Telegram API
        """
        severity_emoji = {
            "high": "🚨",
            "medium": "⚠️",
            "low": "ℹ️"
        }
        
        emoji = severity_emoji.get(severity, "ℹ️")
        concerns_text = "\n".join([f"• {c}" for c in concerns])
        
        alert_message = f"""
{emoji} <b>EMERGENCY ALERT - {severity.upper()} PRIORITY</b> {emoji}

<b>Patient:</b> {patient_name}

<b>Health Concerns Detected:</b>
{concerns_text}

<b>Original Message:</b>
"{message}"

<b>Time:</b> {self._get_current_time()}

⚡ Please check on the patient immediately!
"""
        
        return self.send_message(chat_id, alert_message, parse_mode="HTML")
    
    def _get_current_time(self) -> str:
        """Get current time in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%I:%M %p, %B %d, %Y")

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
