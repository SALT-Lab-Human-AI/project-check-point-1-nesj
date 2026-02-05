# Observability Documentation

## Logging Architecture

### Log Categories

1. **Application Logs**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   
   # Log levels and use cases
   logger.debug("Fine-grained debug info")
   logger.info("General operational events")
   logger.warning("Minor issues that need attention")
   logger.error("Serious problems that need investigation")
   logger.critical("System-breaking issues")
   ```

2. **Component-Specific Logging**
   
   a. Memory System
   ```python
   # Vector store operations
   logger.info("Using ChromaDB default embedding")
   logger.error("Error adding conversation to vector store: {e}")
   
   # Memory cleanup
   logger.info(f"Removed {count} duplicate entries")
   logger.info(f"Cleaned up {count} old conversations")
   ```
   
   b. Database Operations
   ```python
   # Transaction logging
   logger.info(f"Created new {model_name} record: {id}")
   logger.error(f"Database transaction failed: {error}")
   ```
   
   c. API Requests
   ```python
   # Request tracking
   logger.info(f"Incoming {method} request to {endpoint}")
   logger.info(f"Request completed in {duration}ms")
   ```

### Log Storage

```
carely/
├── logs/
│   ├── app.log           # Main application log
│   ├── error.log        # Error-level and above
│   ├── api.log          # API request logs
│   └── security.log     # PII detection, auth events
└── archived_logs/       # Rotated logs
```

### Log Format
```python
LOG_FORMAT = (
    '%(asctime)s - %(name)s - %(levelname)s - '
    '%(filename)s:%(lineno)d - '
    '%(message)s'
)
```

## Bug Reproduction

### Test Data Setup

1. **Sample Database Seed**
   ```python
   # test_data/seed.py
   def create_test_data():
       test_user = UserCRUD.create_user(
           name="Test Patient",
           email="test@example.com"
       )
       
       test_medication = MedicationCRUD.create_medication(
           user_id=test_user.id,
           name="Test Med",
           dosage="100mg",
           frequency="daily",
           schedule_times=["09:00"]
       )
       
       return {
           "user": test_user,
           "medication": test_medication
       }
   ```

2. **Conversation History Generator**
   ```python
   # test_data/conversations.py
   def generate_test_conversations(user_id: int):
       templates = [
           "How are you feeling today?",
           "Did you take your medication?",
           "What time is my next dose?"
       ]
       
       for template in templates:
           ConversationCRUD.save_conversation(
               user_id=user_id,
               message=template,
               response="Test response",
               conversation_type="test"
           )
   ```

### Reproducing Issues

1. **Environment Setup**
   ```bash
   # 1. Reset test database
   rm carely_test.db
   python -m test_data.setup
   
   # 2. Enable detailed logging
   export LOG_LEVEL=DEBUG
   
   # 3. Run specific test scenario
   python -m pytest tests/test_specific_scenario.py
   ```

2. **Log Filtering**
   ```python
   # Filter logs for specific user/session
   def filter_logs(user_id: int, start_time: datetime):
       with open('logs/app.log', 'r') as f:
           for line in f:
               if (f'user_id={user_id}' in line and 
                   parse_log_time(line) >= start_time):
                   print(line)
   ```

## Test Debugging

### Failed Test Analysis

1. **Test Output Location**
   ```
   tests/
   ├── reports/
   │   ├── test_results.xml    # JUnit format
   │   └── coverage.xml        # Coverage report
   └── artifacts/
       └── failed_test_logs/   # Logs from failed tests
   ```

2. **Common Debug Steps**
   ```python
   # 1. Enable test logging
   pytest --log-cli-level=DEBUG
   
   # 2. Run specific test with debugger
   pytest tests/test_file.py::test_name -v --pdb
   
   # 3. Generate failure report
   pytest --html=report.html
   ```

### Debug Helpers

1. **PII Test Helper**
   ```python
   # test_pii_redaction.py
   def test_pii_detection():
       test_cases = [
           {
               "name": "Insurance Policy Number",
               "input": "policy #123456789",
               "expected_type": "insurance_policy"
           },
           # ... more test cases
       ]
       
       for case in test_cases:
           detected = PIIRedactor.detect_pii(case["input"])
           print(f"Test: {case['name']}")
           print(f"Detected: {detected}")
   ```

2. **Memory System Debug**
   ```python
   def debug_memory_chain(user_id: int):
       """Trace memory system operations"""
       memory = MemoryManager()
       
       # 1. Check conversation storage
       convs = memory.get_recent_conversations(user_id)
       print(f"Found {len(convs)} conversations")
       
       # 2. Verify vector embeddings
       vectors = memory.get_vector_store().get(user_id)
       print(f"Found {len(vectors)} embeddings")
       
       # 3. Test retrieval
       results = memory.search_memory(
           user_id, 
           "test query",
           limit=5
       )
       print(f"Search results: {results}")
   ```

3. **Transaction Debugger**
   ```python
   from contextlib import contextmanager
   
   @contextmanager
   def debug_transaction():
       """Debug database transactions"""
       try:
           print("Starting transaction...")
           yield
           print("Transaction committed")
       except Exception as e:
           print(f"Transaction failed: {e}")
           raise
   
   # Usage
   with debug_transaction():
       UserCRUD.create_user(...)
   ```

### Common Issues & Solutions

1. **Memory Leaks**
   - Symptom: Growing memory usage
   - Debug: Monitor Chroma collection sizes
   - Fix: Run periodic cleanup
   ```python
   memory.cleanup_old_conversations(days=30)
   ```

2. **Race Conditions**
   - Symptom: Intermittent database errors
   - Debug: Enable SQLModel echo
   - Fix: Use proper transaction isolation
   ```python
   with get_session() as session:
       session.begin()
       try:
           # Operations
           session.commit()
       except:
           session.rollback()
   ```

3. **PII Leaks**
   - Symptom: Unredacted data in logs
   - Debug: Run test_pii_detection()
   - Fix: Update regex patterns
   ```python
   # Add new pattern
   PATTERNS = {
       'new_type': r'pattern_here',
       ...
   }
   ```