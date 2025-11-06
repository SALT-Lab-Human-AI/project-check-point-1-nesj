# Output Schemas Documentation

## Response Schema

```json
{
    "response": "string",          // The AI response text
    "sentiment_score": float,      // Range: -1.0 to 1.0
    "sentiment_label": "string",   // "positive", "negative", "neutral"
    "alert_sent": boolean,         // Whether caregiver was alerted
    "conversation_id": int,        // Database ID of conversation
    "is_emergency": boolean,       // Emergency situation flag
    "emergency_severity": "string", // "critical", "high", "medium", "none"
    "emergency_concerns": [        // List of detected concerns
        "string"
    ],
    "should_alert": boolean,       // Whether caregiver alert needed
    "quick_actions": [             // Available quick actions
        "string"
    ],
    "contains_pii": boolean       // PII detection flag
}
```

## Verbosity Levels

```json
{
    "SHORT": {
        "max_tokens": 220,
        "sentence_limit": 4,
        "use_case": "casual chat, simple questions"
    },
    "MEDIUM": {
        "max_tokens": 600,
        "sentence_limit": 8,
        "use_case": "explanations, summaries"
    },
    "LONG": {
        "max_tokens": 1200,
        "sentence_limit": null,
        "use_case": "detailed instructions, stories"
    }
}
```

## Quick Actions

```json
{
    "available_actions": [
        "log_medication",   // Medication logging
        "play_music",       // Music/relaxation
        "fun_corner",       // Entertainment
        "memory_cue"        // Memory exercise
    ]
}
```

## Emergency Detection

```json
{
    "severity_levels": {
        "critical": {
            "keywords": [
                "chest pain",
                "can't breathe",
                "heart attack",
                "stroke",
                "fell",
                "bleeding",
                "unconscious"
            ],
            "response": "immediate",
            "alert": true
        },
        "high": {
            "keywords": [
                "pain",
                "emergency",
                "help me",
                "fallen",
                "can't move"
            ],
            "response": "urgent",
            "alert": true
        },
        "medium": {
            "keywords": [
                "dizzy",
                "confused",
                "nausea",
                "headache",
                "weak"
            ],
            "response": "monitor",
            "alert": false
        }
    }
}
```

## Sentiment Analysis

```json
{
    "score_ranges": {
        "positive": "> 0.1",
        "neutral": "-0.1 to 0.1",
        "negative": "< -0.1"
    },
    "emotions": [
        "concern",
        "discomfort",
        "loneliness",
        "contentment"
    ],
    "alert_threshold": -0.7
}
```

## Memory Context

```json
{
    "context_types": {
        "conversation": {
            "recent_limit": 5,
            "format": "chronological"
        },
        "personal_events": {
            "window_days": 30,
            "format": "upcoming"
        }
    }
}
```

## Time Format

```json
{
    "timezone": "America/Chicago",
    "formats": {
        "time": "%I:%M %p %Z",
        "date": "%B %d, %Y",
        "day": "%A",
        "datetime": "%B %d at %I:%M %p %Z"
    }
}
```