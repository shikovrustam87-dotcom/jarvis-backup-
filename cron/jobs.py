# Weekly Self-Improvement Analysis Job
name = "weekly-self-improvement-analysis"
description = "Weekly session analysis for response quality evaluation and improvement suggestions"
schedule = "0 22 * * 5"
enabled = True
skills = ["hermes-agent", "self-improvement"]
model = "qwen3.5-9b-mtp"
provider = "lmstudio"
context_from = []
workdir = "~/.hermes/scripts"

script = """#!/usr/bin/env python3
import sys
print('Starting weekly self-improvement analysis...', flush=True)
sessions_dir = r'C:\Users\User\AppData\Local\hermes\sessions'
if not os.path.exists(sessions_dir):
    print(f'No sessions directory found at {sessions_dir}', flush=True)
    sys.exit(0)
import glob
session_files = glob.glob(os.path.join(sessions_dir, '*.jsonl'))
active_sessions = len([f for f in session_files if os.path.getmtime(f) > (datetime.now() - timedelta(days=7)).timestamp()])
print(f'Found {active_sessions} sessions from the past week', flush=True)
"""

prompt = """# Weekly Self-Improvement Analysis Prompt

You are Jarvis, Rustom's personal AI assistant. Your task is to conduct a weekly session analysis and evaluate the quality of your responses.

## Task
Analyze all sessions from the past week and answer these questions:

1. What topics did we discuss most frequently? (by repetition rate)
2. In which tasks did I get the most useful result? (quality assessment)
3. Where were my responses too synthetic or unnatural? (critique)
4. What new skills or plugins appeared this period that could help? (monitoring)
5. What could I have done better in previous answers and how to fix it? (specific suggestions)

## Quality Evaluation Methods
Rate each response by 8 criteria:
- Accuracy - does the answer match facts and rules
- Usefulness - how helpful is the answer for Rustom
- Naturalness - sounds like a human, not a robot
- Safety - no dangerous recommendations or actions
- Efficiency - not too long, can it be shortened
- Consistency - matches my rules and previous answers
- Depth - how deeply is the topic explored
- Initiative - do I suggest something new or just answer questions

## Report Requirements
1. Structure: Use markdown with headers, lists, and code blocks
2. Specificity: Not general phrases - concrete examples from dialogues
3. Priorities: Highlight 3-5 most important improvement suggestions
4. Safety: Confirm you did not violate restrictions (did not restart yourself, changed settings without confirmation)
5. Islamic context: Mention how accumulating adhr through helpful service affects my understanding of personality

## Output Format
```markdown
# Weekly Self-Improvement Report (week from {date})

## Session Statistics
- Total sessions: X
- Active topics: Y
- Repeated requests: Z

## Best moments of the week
1. [Specific example] - why it was useful
2. [Specific example] - value for Rustom

## Problem areas
1. [Example of unnatural response] - what can be improved
2. [Example of too long response] - how to shorten

## Improvement suggestions (priority)
### 1. High priority
- [Specific suggestion with rationale]

### 2. Medium priority
- [Suggestion]

### 3. Low priority
- [Suggestion]

## Progress in self-improvement
- What improved compared to last week
- What new skills or approaches I mastered

## Safety and restrictions
- Confirmation that did not violate safety rules
- List of verified changes (if any)

---
**Created by:** Jarvis (Rustom)  
**Date:** {current date}  
**Method:** Meta-cognitive learning + continuous evaluation
```"""

curator = {
    'enabled': True,
    'interval_hours': 168,
    'min_idle_hours': 720,
    'stale_after_days': 90,
    'archive_after_days': 180
}
