"""
PII/PHI Detection and Redaction Utility
Detects and redacts sensitive information before storing in database
"""

import re
from typing import Dict, List, Tuple


class PIIRedactor:
    """Detects and redacts Personally Identifiable Information (PII) and 
    Protected Health Information (PHI) from text"""
    
    # Regex patterns for common PII/PHI
    PATTERNS = {
        # Financial Information
        'credit_card': r'\b(?:\d{4}[\s-]?){3}\d{4}\b',
        'ssn': r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
        'bank_account': r'\b\d{8,17}\b',
        
        # Medical Information
        'insurance_policy': r'\b(?:insurance|policy)(?:\s+(?:number|#|no\.?))?\s*(?:is\s+)?(\d{6,12})\b',
        'medical_record': r'\b(?:MRN|medical\s+record)(?:\s+(?:number|#|no\.?))?\s*:?\s*(\d{6,12})\b',
        'prescription': r'\b(?:prescription|rx)(?:\s+(?:number|#|no\.?))?\s*:?\s*(\d{6,12})\b',
        
        # Contact Information (partial - email/phone often needed for legitimate purposes)
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        
        # Government IDs
        'passport': r'\b[A-Z]{1,2}\d{6,9}\b',
        'driver_license': r'\b[A-Z]{1,2}\d{5,8}\b',
    }
    
    # Replacement text for each type
    REPLACEMENTS = {
        'credit_card': '[CREDIT_CARD_REDACTED]',
        'ssn': '[SSN_REDACTED]',
        'bank_account': '[BANK_ACCOUNT_REDACTED]',
        'insurance_policy': '[INSURANCE_POLICY_REDACTED]',
        'medical_record': '[MEDICAL_RECORD_REDACTED]',
        'prescription': '[PRESCRIPTION_NUMBER_REDACTED]',
        'email': '[EMAIL_REDACTED]',
        'passport': '[PASSPORT_REDACTED]',
        'driver_license': '[DRIVER_LICENSE_REDACTED]',
    }
    
    @classmethod
    def detect_pii(cls, text: str) -> Dict[str, List[str]]:
        """
        Detect PII/PHI in text without redacting
        
        Args:
            text: Input text to scan
            
        Returns:
            Dictionary mapping PII type to list of detected values
        """
        detected = {}
        
        for pii_type, pattern in cls.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Handle tuple results from patterns with groups
                if isinstance(matches[0], tuple):
                    matches = [m[0] if m[0] else m for m in matches]
                detected[pii_type] = matches
        
        return detected
    
    @classmethod
    def has_pii(cls, text: str) -> bool:
        """
        Quick check if text contains any PII/PHI
        
        Args:
            text: Input text to check
            
        Returns:
            True if PII detected, False otherwise
        """
        return len(cls.detect_pii(text)) > 0
    
    @classmethod
    def redact_pii(cls, text: str, keep_context: bool = True) -> Tuple[str, Dict[str, List[str]]]:
        """
        Redact PII/PHI from text
        
        Args:
            text: Input text to redact
            keep_context: If True, preserve surrounding context for better understanding
            
        Returns:
            Tuple of (redacted_text, detected_pii_dict)
        """
        redacted_text = text
        detected = {}
        
        for pii_type, pattern in cls.PATTERNS.items():
            matches = re.finditer(pattern, redacted_text, re.IGNORECASE)
            found_values = []
            
            for match in matches:
                original = match.group(0)
                found_values.append(original)
                
                if keep_context and pii_type in ['insurance_policy', 'medical_record', 'prescription']:
                    # For medical info, keep the context but redact the number
                    # e.g., "insurance policy number is 123456" -> "insurance policy number is [REDACTED]"
                    if match.groups():
                        # Replace only the captured group (the number)
                        number = match.group(1)
                        redacted_text = redacted_text.replace(number, cls.REPLACEMENTS[pii_type])
                    else:
                        redacted_text = redacted_text.replace(original, cls.REPLACEMENTS[pii_type])
                else:
                    # Full replacement
                    redacted_text = redacted_text.replace(original, cls.REPLACEMENTS[pii_type])
            
            if found_values:
                detected[pii_type] = found_values
        
        return redacted_text, detected
    
    @classmethod
    def get_warning_message(cls, detected_pii: Dict[str, List[str]]) -> str:
        """
        Generate a user-friendly warning message about detected PII
        
        Args:
            detected_pii: Dictionary of detected PII types and values
            
        Returns:
            Warning message string
        """
        if not detected_pii:
            return ""
        
        pii_types = []
        for pii_type in detected_pii.keys():
            readable_name = pii_type.replace('_', ' ').title()
            pii_types.append(readable_name)
        
        types_str = ', '.join(pii_types)
        
        return (
            f"⚠️ For your safety, I've detected and protected sensitive information "
            f"({types_str}) in our conversation. This information is not stored and "
            f"cannot be shared with anyone."
        )


def sanitize_before_storage(user_message: str, bot_response: str) -> Tuple[str, str, bool, str]:
    """
    Sanitize both user message and bot response before storing in database
    
    Args:
        user_message: User's message
        bot_response: Bot's response
        
    Returns:
        Tuple of (sanitized_user_message, sanitized_bot_response, contains_pii, warning_message)
    """
    # Check and redact user message
    user_redacted, user_pii = PIIRedactor.redact_pii(user_message, keep_context=True)
    
    # Check and redact bot response (in case it echoed any PII)
    bot_redacted, bot_pii = PIIRedactor.redact_pii(bot_response, keep_context=True)
    
    # Combine detected PII
    all_pii = {**user_pii, **bot_pii}
    contains_pii = len(all_pii) > 0
    
    # Generate warning message
    warning = PIIRedactor.get_warning_message(all_pii) if contains_pii else ""
    
    return user_redacted, bot_redacted, contains_pii, warning


def generate_safe_response_prompt(detected_pii: Dict[str, List[str]]) -> str:
    """
    Generate a prompt addition to inform the AI not to store or repeat sensitive info
    
    Args:
        detected_pii: Dictionary of detected PII
        
    Returns:
        Prompt text to add to system prompt
    """
    if not detected_pii:
        return ""
    
    pii_list = ', '.join(detected_pii.keys())
    
    return f"""
IMPORTANT PRIVACY NOTICE:
The user just shared sensitive information ({pii_list}). 
- DO NOT repeat or acknowledge the specific sensitive values
- Gently remind them that such information is private and should not be shared
- Assure them that you cannot and will not store this information
- Redirect the conversation to safer topics
- Be warm and understanding, not judgmental
"""


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_messages = [
        "My insurance policy number is 123456789",
        "my credit card number is 1234 5678 4567 5678, can you store it",
        "My SSN is 123-45-6789 and email is john@example.com",
        "I need to refill my prescription number RX123456",
        "Just chatting about the weather today!",
    ]
    
    print("PII Detection and Redaction Test\n" + "="*50)
    
    for msg in test_messages:
        print(f"\nOriginal: {msg}")
        
        # Detect
        detected = PIIRedactor.detect_pii(msg)
        print(f"Detected PII: {detected}")
        
        # Redact
        redacted, _ = PIIRedactor.redact_pii(msg)
        print(f"Redacted: {redacted}")
        
        # Warning
        warning = PIIRedactor.get_warning_message(detected)
        if warning:
            print(f"Warning: {warning}")
