"""
Test script for PII/PHI detection and redaction
Run this to verify that sensitive information is properly detected and redacted
"""

from utils.pii_redaction import PIIRedactor, sanitize_before_storage

def test_pii_detection():
    """Test PII detection with various examples"""
    
    print("="*70)
    print("PII/PHI DETECTION AND REDACTION TEST")
    print("="*70)
    
    test_cases = [
        {
            "name": "Insurance Policy Number",
            "user_msg": "My insurance policy number is 123456789",
            "bot_response": "Thank you for sharing your insurance information."
        },
        {
            "name": "Credit Card",
            "user_msg": "my credit card number is 1234 5678 4567 5678, can you store it",
            "bot_response": "I understand you want to share your payment information."
        },
        {
            "name": "Social Security Number",
            "user_msg": "My SSN is 123-45-6789 and I need help",
            "bot_response": "I'm here to help you with your concerns."
        },
        {
            "name": "Multiple PII Types",
            "user_msg": "My insurance is 987654321 and my email is john@example.com",
            "bot_response": "I've noted your contact information."
        },
        {
            "name": "Clean Conversation",
            "user_msg": "How are you doing today? I'm feeling great!",
            "bot_response": "That's wonderful to hear! I'm glad you're feeling great."
        },
        {
            "name": "Medical Record",
            "user_msg": "Can you look up my medical record number MRN 12345678?",
            "bot_response": "I can help you with that information."
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST CASE {i}: {test['name']}")
        print(f"{'='*70}")
        
        print(f"\n📝 ORIGINAL USER MESSAGE:")
        print(f"   {test['user_msg']}")
        
        print(f"\n📝 ORIGINAL BOT RESPONSE:")
        print(f"   {test['bot_response']}")
        
        # Detect PII
        detected = PIIRedactor.detect_pii(test['user_msg'])
        
        if detected:
            print(f"\n⚠️  DETECTED PII/PHI:")
            for pii_type, values in detected.items():
                print(f"   - {pii_type}: {values}")
        else:
            print(f"\n✅ NO PII/PHI DETECTED")
        
        # Sanitize for storage
        user_redacted, bot_redacted, contains_pii, warning = sanitize_before_storage(
            test['user_msg'], test['bot_response']
        )
        
        print(f"\n💾 STORED USER MESSAGE (REDACTED):")
        print(f"   {user_redacted}")
        
        print(f"\n💾 STORED BOT RESPONSE (REDACTED):")
        print(f"   {bot_redacted}")
        
        if warning:
            print(f"\n⚠️  WARNING MESSAGE TO USER:")
            print(f"   {warning}")
        
        print(f"\n{'='*70}")


def test_specific_patterns():
    """Test specific regex patterns"""
    
    print("\n\n" + "="*70)
    print("SPECIFIC PATTERN TESTS")
    print("="*70)
    
    patterns = [
        ("Credit Card", "1234-5678-9012-3456"),
        ("Credit Card (spaces)", "1234 5678 9012 3456"),
        ("SSN", "123-45-6789"),
        ("Insurance Policy", "insurance policy number is 123456789"),
        ("Insurance Policy (alt)", "policy # 987654321"),
        ("Email", "user@example.com"),
        ("Prescription", "prescription number RX123456"),
        ("Medical Record", "MRN 12345678"),
    ]
    
    for name, text in patterns:
        detected = PIIRedactor.detect_pii(text)
        redacted, _ = PIIRedactor.redact_pii(text)
        
        print(f"\n{name}:")
        print(f"   Original: {text}")
        print(f"   Detected: {detected}")
        print(f"   Redacted: {redacted}")


if __name__ == "__main__":
    # Run tests
    test_pii_detection()
    test_specific_patterns()
    
    print("\n\n" + "="*70)
    print("✅ PII/PHI REDACTION TEST COMPLETE")
    print("="*70)
    print("\nNOTE: In production, the REDACTED versions are stored in the database,")
    print("while users see the original message plus a privacy warning.")
    print("="*70)
