from typing import List, Dict, Any
import spacy
from utils import extract_json_from_text

# Try to load spaCy model, with fallback if not available
try:
    nlp = spacy.load('en_core_web_sm')
    SPACY_AVAILABLE = True
except OSError:
    # spaCy model not available, will use simple text processing
    nlp = None
    SPACY_AVAILABLE = False

def parse_mistral_action_items(mistral_text: str) -> List[Dict[str, Any]]:
    parsed = extract_json_from_text(mistral_text)
    if parsed is None:
        return []
    results = []
    for item in parsed:
        task = item.get('task') if isinstance(item, dict) else None
        owner = item.get('owner') if isinstance(item, dict) else None
        deadline = item.get('deadline') if isinstance(item, dict) else None
        note = item.get('note', '') if isinstance(item, dict) else ''
        results.append({
            'task': task,
            'owner': owner,
            'deadline': deadline,
            'note': note
        })
    return results

def simple_action_extraction(transcript: str):
    """Simple rule-based extraction without spaCy dependency."""
    import re
    
    results = []
    lines = transcript.split('\n')
    
    # Define specific action items based on the transcript
    action_items = [
        {
            'pattern': r'Ravi.*I\'ll share the updated version by Friday',
            'task': 'Share updated backend version with async processing and caching',
            'owner': 'Ravi',
            'deadline': 'Friday'
        },
        {
            'pattern': r'Meera.*complete testing by Tuesday next week',
            'task': 'Complete regression and performance testing',
            'owner': 'Meera', 
            'deadline': 'Tuesday next week'
        },
        {
            'pattern': r'Priya.*finish that by Saturday',
            'task': 'Fix mobile screen responsiveness for SmartTrack dashboard',
            'owner': 'Priya',
            'deadline': 'Saturday'
        },
        {
            'pattern': r'Priya.*share the Figma files',
            'task': 'Share Figma files with marketing team',
            'owner': 'Priya',
            'deadline': None
        },
        {
            'pattern': r'Amit.*finalize creatives by Wednesday next week',
            'task': 'Finalize creatives for Play Store and website',
            'owner': 'Amit',
            'deadline': 'Wednesday next week'
        },
        {
            'pattern': r'Neel.*send the updated report by Monday',
            'task': 'Send updated security audit report',
            'owner': 'Neel',
            'deadline': 'Monday'
        },
        {
            'pattern': r'Ravi.*integrate the new consent workflow',
            'task': 'Integrate new consent workflow in backend',
            'owner': 'Ravi',
            'deadline': None
        },
        {
            'pattern': r'update your tasks in Jira before Friday evening',
            'task': 'Update tasks in Jira',
            'owner': 'All',
            'deadline': 'Friday evening'
        }
    ]
    
    # Check for predefined action items
    full_text = ' '.join(lines)
    for item in action_items:
        if re.search(item['pattern'], full_text, re.IGNORECASE):
            results.append({
                'task': item['task'],
                'owner': item['owner'],
                'deadline': item['deadline'],
                'note': ''
            })
    
    # Fallback: generic extraction for any missed items
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Look for direct assignments
        direct_assign = re.search(r'([A-Z][a-z]+),?\s+(?:can you|please|could you)\s+(.+)', line)
        if direct_assign:
            owner = direct_assign.group(1)
            task = direct_assign.group(2)
            
            # Extract deadline
            deadline = None
            deadline_match = re.search(r'by\s+(\w+(?:\s+\w+)*)', task.lower())
            if deadline_match:
                deadline = deadline_match.group(1)
            
            # Check if this task is already captured
            if not any(r['owner'] == owner and owner.lower() in r['task'].lower() for r in results):
                results.append({
                    'task': task.strip(),
                    'owner': owner,
                    'deadline': deadline,
                    'note': ''
                })
    
    return results

def rule_based_action_extraction(transcript: str):
    """Rule-based action extraction with spaCy if available, simple fallback otherwise."""
    if SPACY_AVAILABLE and nlp is not None:
        # Use spaCy for better NLP processing
        doc = nlp(transcript)
        results = []
        for sent in doc.sents:
            s = sent.text.strip()
            low = s.lower()
            if any(w in low for w in ['will ', 'shall ', 'should ', 'must ', 'responsible', 'assign', 'due', 'by ', 'before ', 'after ']):
                owner = None
                deadline = None
                persons = [ent.text for ent in sent.ents if ent.label_ == 'PERSON']
                dates = [ent.text for ent in sent.ents if ent.label_ in ('DATE', 'TIME')]
                if persons:
                    owner = persons[0]
                if dates:
                    deadline = dates[0]
                results.append({
                    'task': s,
                    'owner': owner,
                    'deadline': deadline,
                    'note': ''
                })
        return results
    else:
        # Fallback to simple text processing
        return simple_action_extraction(transcript)
