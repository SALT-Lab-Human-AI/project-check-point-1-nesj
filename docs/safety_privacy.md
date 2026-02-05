# Safety & Privacy Documentation

## PII/PHI Protection

### Detection & Redaction Points
1. **Input Processing**
   - User messages scanned before storage
   - Bot responses checked for echoed PII
   - Real-time warning generation

2. **Protected Patterns**
   ```
   Financial Information:
   - Credit card numbers
   - Social Security Numbers (SSN)
   - Bank account numbers

   Medical Information:
   - Insurance policy numbers
   - Medical record numbers (MRN)
   - Prescription numbers

   Personal Identifiers:
   - Email addresses
   - Passport numbers
   - Driver's license numbers
   ```

3. **Redaction Strategy**
   - Context-aware redaction for medical information
   - Full replacement for financial data
   - Warning messages to users when PII is detected
   - Safe storage with placeholders (e.g., [SSN_REDACTED])

## Rate Limiting

### Implementation
```python
from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.tokens = defaultdict(list)  # IP/User -> list of timestamps
        
    async def check_rate_limit(self, request: Request):
        key = request.client.host  # or user_id for authenticated requests
        now = time.time()
        
        # Remove old timestamps
        self.tokens[key] = [ts for ts in self.tokens[key] 
                           if ts > now - 60]
        
        # Check limit
        if len(self.tokens[key]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again in a minute."
            )
        
        # Add new timestamp
        self.tokens[key].append(now)
        return True

# Usage in FastAPI
rate_limiter = RateLimiter()

@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    await rate_limiter.check_rate_limit(request)
    return await call_next(request)
```

## Emergency Handling

### Detection & Escalation
1. **Severity Levels**
   - Critical: Immediate caregiver notification
   - High: Urgent caregiver alert
   - Medium: Optional notification

2. **Escalation Pathway**
   ```
   User Emergency Message
   ↓
   Emergency Detection (utils/emergency_detection.py)
   ↓
   Severity Classification
   ↓
   Caregiver Alert System
     → Telegram alert
   ↓
   Database Alert Log
   ```

3. **Response Protocol**
   - Immediate user reassurance
   - Clear instructions for immediate actions
   - Confirmation of caregiver notification
   - Follow-up monitoring

## Data Residency

### Local Storage
1. **Primary Database**
   - SQLite database (`carely.db`)
   - Local file system storage
   - No cloud synchronization

2. **Vector Store**
   - Chroma embeddings in `data/` directory
   - Local persistence only
   - Memory context isolation per user

3. **Data Locations**
   ```
   carely/
   ├── carely.db       # Main SQLite database
   ├── data/           # Chroma vector store
   │   └── embeddings/ # Conversation embeddings
   └── logs/          # System logs
   ```

## Model Provider Integration

### Groq API Usage
1. **Data Transmission**
   - Chat messages (PII redacted)
   - System prompts
   - Context windows

2. **Metadata Handling**
   ```
   Sent to Groq:
   - Redacted conversation history
   - System instructions
   - User preferences (non-PII)

   Not Sent:
   - Raw PII/PHI data
   - User identifiers
   - Location data
   - Medical records
   ```

## Consent & Legal Disclaimers

### Medical Disclaimer
```
IMPORTANT: Carely is an AI companion and does not provide medical advice. 
The system:
- Cannot diagnose conditions
- Does not prescribe medications
- Should not replace healthcare providers
- Is for companionship and reminder purposes only
```

### Caregiver Visibility
1. **Alert Access**
   - Emergency notifications
   - Conversation summaries (PII redacted)

2. **Privacy Controls**
   - User-configurable sharing settings
   - Granular permission system
   - Audit logging of access

### Data Rights

1. **Data Export**
   ```
   Request Process:
   1. User contacts support
   2. Identity verification
   3. Data package generation
   4. Secure download link
   ```

2. **Account Deletion**
   ```sql
   -- Deletion Process
   BEGIN TRANSACTION;
     -- 1. Archive necessary logs
     -- 2. Delete user data
     DELETE FROM conversations WHERE user_id = ?;
     DELETE FROM medication_logs WHERE user_id = ?;
     DELETE FROM reminders WHERE user_id = ?;
     DELETE FROM personal_events WHERE user_id = ?;
     DELETE FROM caregiver_alerts WHERE user_id = ?;
     -- 3. Remove vector store embeddings
     DELETE FROM chroma_embeddings WHERE user_id = ?;
     -- 4. Delete user account
     DELETE FROM users WHERE id = ?;
   COMMIT;
   ```

3. **Retention Policy**
   - Active data: Duration of account
   - Logs: 90 days
   - Backup: 30 days
   - Emergency data: 7 days
