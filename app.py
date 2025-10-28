import argparse, pandas as pd
from nlp_summarizer import generate_summary, enhanced_action_extraction

def summarize_transcript(transcript: str):
    try:
        return generate_summary(transcript)
    except Exception as e:
        print('NLP error:', e)
        return "Error generating summary"

def extract_actions(transcript: str):
    try:
        return enhanced_action_extraction(transcript)
    except Exception as e:
        print('NLP error:', e)
        return []

def main(args):
    inpath = args.input
    with open(inpath, 'r', encoding='utf-8') as f:
        transcript = f.read()

    print('=== Generating NLP Summary ===')
    summary = summarize_transcript(transcript)
    print(summary)
    print('\n=== Extracting Action Items ===')
    items = extract_actions(transcript)
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

    args = parser.parse_args()
    main(args)
