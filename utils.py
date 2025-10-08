import re, json

def extract_json_from_text(text: str):
    """Try to find the first JSON array/object in text and parse it."""
    m = re.search(r'(\[\s*\{.*\}\s*\])', text, flags=re.S)
    if not m:
        m = re.search(r'(\{.*\})', text, flags=re.S)
    if not m:
        return None
    json_text = m.group(1)
    try:
        return json.loads(json_text)
    except Exception:
        try:
            fixed = json_text.replace("'", '"')
            return json.loads(fixed)
        except Exception:
            return None
