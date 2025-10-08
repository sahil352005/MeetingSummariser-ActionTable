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
    sentences = transcript.split('\n')
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Look for action words
        action_patterns = [
            r'\b(will|shall|should|must|need to|have to|going to)\b',
            r'\b(responsible|assign|due|by|before|after)\b',
            r'\b(action|task|todo|follow up|follow-up)\b'
        ]
        
        if any(re.search(pattern, sentence.lower()) for pattern in action_patterns):
            # Try to extract person names (simple heuristic)
            person_match = re.search(r'\b([A-Z][a-z]+)\s+(?:will|shall|should|must|is responsible|needs to)', sentence)
            owner = person_match.group(1) if person_match else None
            
            # Try to extract dates/times
            date_patterns = [
                r'\b(today|tomorrow|yesterday)\b',
                r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
                r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b\d{1,2}:\d{2}\b'
            ]
            
            deadline = None
            for pattern in date_patterns:
                match = re.search(pattern, sentence.lower())
                if match:
                    deadline = match.group(0)
                    break
            
            results.append({
                'task': sentence,
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
