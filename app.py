import argparse, pandas as pd
from prompts import SUMMARY_PROMPT, ACTION_ITEM_PROMPT
from extractor import parse_mistral_action_items, rule_based_action_extraction
try:
    from mistral_client import call_mistral
except Exception:
    call_mistral = None

def summarize_transcript(transcript: str, use_mistral=True):
    if use_mistral and call_mistral is not None:
        prompt = SUMMARY_PROMPT.format(transcript=transcript)
        try:
            resp = call_mistral(prompt, max_tokens=200)
            return resp.strip()
        except Exception as e:
            print('Mistral error:', e)
            use_mistral = False
    # fallback naive summary
    sents = [s.strip() for s in transcript.split('\n') if s.strip()]
    return '\n'.join(sents[:5])

def extract_actions(transcript: str, use_mistral=True):
    if use_mistral and call_mistral is not None:
        prompt = ACTION_ITEM_PROMPT.format(transcript=transcript)
        try:
            resp = call_mistral(prompt, max_tokens=512)
            items = parse_mistral_action_items(resp)
            if items:
                return items
            else:
                print('Mistral returned no parsable JSON, falling back to rule-based extractor.')
        except Exception as e:
            print('Mistral error:', e)
    return rule_based_action_extraction(transcript)

def main(args):
    inpath = args.input
    use_mistral = args.mistral
    with open(inpath, 'r', encoding='utf-8') as f:
        transcript = f.read()

    print('=== Generating summary ===')
    summary = summarize_transcript(transcript, use_mistral=use_mistral)
    print(summary)
    print('\n=== Extracting action items ===')
    items = extract_actions(transcript, use_mistral=use_mistral)
    df = pd.DataFrame(items)
    if df.empty:
        print('No action items found.')
    else:
        print(df.to_string(index=False))
        out_csv = args.output or 'action_items.csv'
        df.to_csv(out_csv, index=False)
        print(f'\nSaved action items to {out_csv}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', default='sample_transcript.txt', help='Input transcript file')
    parser.add_argument('--output', '-o', help='Output CSV for action items')
    parser.add_argument('--mistral', action='store_true', help='Use Mistral API (requires env vars)')
    args = parser.parse_args()
    main(args)
