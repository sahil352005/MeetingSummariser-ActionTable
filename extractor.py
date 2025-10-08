from typing import List, Dict, Any
import spacy
from utils import extract_json_from_text

nlp = spacy.load('en_core_web_sm')

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

def rule_based_action_extraction(transcript: str):
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
