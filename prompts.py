# prompts.py - prompt templates for summary and action item extraction
SUMMARY_PROMPT = '''You are a helpful assistant. Produce a concise meeting summary (3-6 bullet points) from the transcript below. Keep it short and factual.

Transcript:
"""
{transcript}
"""

Please output only the summary in bullet points.
'''

ACTION_ITEM_PROMPT = '''You are a helpful assistant. From the transcript below, extract all action items.
For each action item return a JSON array where each element is an object with keys:
- task: short task description (string)
- owner: name of person responsible (string or null)
- deadline: deadline or due date if present (string or null)
- note: any extra context (string, optional)

Transcript:
"""
{transcript}
"""

Return only valid JSON (an array). Example:
[
  {{ "task": "Prepare slides", "owner": "John", "deadline": "Friday", "note": "" }},
  ...
]
'''
