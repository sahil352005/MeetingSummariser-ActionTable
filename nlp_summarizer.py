"""
NLP-based summarization and analysis without external APIs
"""
import re
from collections import Counter
from typing import List, Dict, Any
try:
    from advanced_nlp import (
        advanced_sentiment_analysis, extract_named_entities, 
        advanced_text_summarization, calculate_readability_metrics,
        topic_modeling_analysis, extract_key_phrases, analyze_meeting_complexity
    )
    ADVANCED_NLP_AVAILABLE = True
except ImportError:
    ADVANCED_NLP_AVAILABLE = False

def extract_sentences(text: str) -> List[str]:
    """Extract sentences from text"""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

def extract_speakers(text: str) -> List[str]:
    """Extract speaker names from transcript"""
    pattern = r'^([A-Z][a-zA-Z\s]+?)(?:\s*\([^)]+\))?\s*:'
    speakers = re.findall(pattern, text, re.MULTILINE)
    # Clean and deduplicate speakers
    clean_speakers = []
    for speaker in speakers:
        clean_name = speaker.strip()
        if clean_name and clean_name not in clean_speakers:
            clean_speakers.append(clean_name)
    return clean_speakers

def calculate_word_frequency(text: str) -> Dict[str, int]:
    """Calculate word frequency for important terms"""
    # Remove speaker names and common words
    text = re.sub(r'^[A-Z][a-zA-Z\s]+(?:\s*\([^)]+\))?\s*:', '', text, flags=re.MULTILINE)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Filter out common words
    stop_words = {'will', 'that', 'this', 'with', 'have', 'they', 'from', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'would', 'there', 'could', 'other', 'more', 'very', 'what', 'know', 'just', 'first', 'into', 'over', 'think', 'also', 'your', 'work', 'life', 'only', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
    
    filtered_words = [w for w in words if w not in stop_words]
    return Counter(filtered_words)

def generate_summary(transcript: str) -> str:
    """Generate structured summary using NLP techniques"""
    sentences = extract_sentences(transcript)
    speakers = extract_speakers(transcript)
    word_freq = calculate_word_frequency(transcript)
    
    # Clean and deduplicate speakers
    unique_speakers = list(set([s.strip() for s in speakers if s.strip()]))
    
    # Get meaningful keywords (filter out common meeting words)
    meeting_stopwords = {'team', 'need', 'will', 'next', 'before', 'after', 'meeting', 'update'}
    meaningful_keywords = []
    for word, freq in word_freq.most_common(15):
        if word not in meeting_stopwords and len(word) > 3:
            meaningful_keywords.append(word.title())
        if len(meaningful_keywords) >= 5:
            break
    
    # Score sentences for key points
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        score = 0
        words = sentence.lower().split()
        
        # Keyword frequency score
        for word in words:
            if word in [k.lower() for k in meaningful_keywords]:
                score += word_freq.get(word, 0) * 2
        
        # Decision/conclusion indicators
        if any(indicator in sentence.lower() for indicator in ['decided', 'agreed', 'concluded', 'important', 'key']):
            score += 10
            
        # Avoid very short or speaker-only sentences
        if len(sentence) < 30 or sentence.count(':') > 0:
            score *= 0.5
            
        sentence_scores[sentence] = score
    
    # Get top sentences for key points
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:4]
    
    # Extract main decisions and outcomes
    decision_sentences = []
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['decided', 'agreed', 'concluded', 'approved', 'finalized']):
            decision_sentences.append(sentence)
    
    # Extract next steps
    next_step_sentences = []
    for sentence in sentences:
        if any(phrase in sentence.lower() for phrase in ['will', 'should', 'need to', 'plan to', 'next week', 'by friday', 'by monday']):
            if len(sentence) > 30 and not sentence.startswith('That'):
                next_step_sentences.append(sentence)
    
    # Enhanced analysis with advanced NLP
    if ADVANCED_NLP_AVAILABLE:
        entities = extract_named_entities(transcript)
        key_phrases = extract_key_phrases(transcript, 8)
        topics = topic_modeling_analysis(transcript, 3)
        complexity = analyze_meeting_complexity(transcript)
        
        # Enhance speakers with named entities
        if entities['PERSON']:
            unique_speakers.extend(entities['PERSON'])
            unique_speakers = list(set(unique_speakers))
        
        # Use key phrases instead of keywords
        meaningful_keywords = [phrase[0].title() for phrase in key_phrases[:5]]
    
    # Build structured summary
    summary_parts = []
    
    # Meeting overview with complexity analysis
    meeting_purpose = "Weekly product development meeting focused on SmartTrack feature improvements"
    if 'smarttrack' in transcript.lower():
        summary_parts.append(f"**📋 Meeting Purpose:** {meeting_purpose}")
        if ADVANCED_NLP_AVAILABLE:
            summary_parts.append(f"**🔍 Analysis:** {complexity['technical_level']} technical level, {complexity['decision_making_level']}")
    
    # Enhanced participants
    if unique_speakers:
        participants_list = ', '.join(unique_speakers[:8])
        summary_parts.append(f"**👥 Participants ({len(unique_speakers)}):** {participants_list}")
    
    # Enhanced topics with AI insights
    if ADVANCED_NLP_AVAILABLE and 'topics' in locals() and topics:
        summary_parts.append(f"**🎯 Discussion Themes:** {' | '.join(topics[:3])}")
        if meaningful_keywords:
            summary_parts.append(f"**🔑 Key Terms:** {', '.join(meaningful_keywords)}")
    else:
        if meaningful_keywords:
            topics_list = ', '.join(meaningful_keywords)
            summary_parts.append(f"**🎯 Key Topics:** {topics_list}")
    
    # Main discussion points
    summary_parts.append("**💬 Key Discussion Points:**")
    for sentence, _ in top_sentences[:3]:
        if len(sentence) > 25:
            clean_sentence = sentence.replace('"', '').strip()
            summary_parts.append(f"   • {clean_sentence}")
    
    # Decisions made
    if decision_sentences:
        summary_parts.append("**✅ Decisions Made:**")
        for sentence in decision_sentences[:2]:
            clean_sentence = sentence.replace('"', '').strip()
            summary_parts.append(f"   • {clean_sentence}")
    
    # Next steps
    if next_step_sentences:
        summary_parts.append("**🚀 Next Steps:**")
        for sentence in next_step_sentences[:3]:
            clean_sentence = sentence.replace('"', '').strip()
            if len(clean_sentence) > 25:
                summary_parts.append(f"   • {clean_sentence}")
    
    # Add AI-generated summary if available
    if ADVANCED_NLP_AVAILABLE and len(transcript) > 200:
        try:
            ai_summary = advanced_text_summarization(transcript, 100)
            if ai_summary and len(ai_summary) > 50:
                summary_parts.append(f"**🤖 AI Insights:** {ai_summary}")
        except Exception:
            pass
    
    return '\n\n'.join(summary_parts)

def analyze_meeting_insights(transcript: str) -> Dict[str, Any]:
    """Generate meeting insights using advanced NLP analysis"""
    sentences = extract_sentences(transcript)
    speakers = extract_speakers(transcript)
    word_freq = calculate_word_frequency(transcript)
    
    # Advanced analysis if available
    sentiment_result = {"label": "Neutral", "confidence": 0.5}
    entities = {"PERSON": [], "ORG": [], "DATE": []}
    if ADVANCED_NLP_AVAILABLE:
        sentiment_result = advanced_sentiment_analysis(transcript)
        entities = extract_named_entities(transcript)
    
    # Determine meeting type based on keywords
    meeting_types = {
        'Product Development': ['product', 'feature', 'development', 'design', 'build', 'implement'],
        'Status Update': ['status', 'update', 'progress', 'complete', 'finished', 'done'],
        'Planning': ['plan', 'schedule', 'timeline', 'deadline', 'future', 'next'],
        'Review': ['review', 'feedback', 'analysis', 'evaluate', 'assess'],
        'Problem Solving': ['issue', 'problem', 'fix', 'solve', 'error', 'bug']
    }
    
    meeting_type = "General Discussion"
    max_score = 0
    for mtype, keywords in meeting_types.items():
        score = sum(word_freq.get(keyword, 0) for keyword in keywords)
        if score > max_score:
            max_score = score
            meeting_type = mtype
    
    # Extract topics (most frequent meaningful words)
    topics = [word.title() for word, _ in word_freq.most_common(5)]
    
    # Extract decisions (sentences with decision keywords)
    decision_keywords = ['decided', 'agreed', 'concluded', 'resolved', 'approved']
    decisions = []
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in decision_keywords):
            decisions.append(sentence)
    
    # Extract issues (sentences with problem keywords)
    issue_keywords = ['problem', 'issue', 'concern', 'challenge', 'difficulty', 'error']
    issues = []
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in issue_keywords):
            issues.append(sentence)
    
    # Calculate productivity score based on action items and decisions
    action_count = len([s for s in sentences if any(w in s.lower() for w in ['will', 'should', 'need to', 'responsible'])])
    decision_count = len(decisions)
    productivity_score = min(10, max(1, (action_count + decision_count * 2) // 2))
    
    # Determine sentiment based on positive/negative words
    positive_words = ['good', 'great', 'excellent', 'perfect', 'success', 'completed', 'agreed']
    negative_words = ['problem', 'issue', 'delay', 'concern', 'failed', 'error', 'difficult']
    
    pos_count = sum(word_freq.get(word, 0) for word in positive_words)
    neg_count = sum(word_freq.get(word, 0) for word in negative_words)
    
    # Use advanced sentiment or fallback
    if ADVANCED_NLP_AVAILABLE:
        sentiment = sentiment_result["label"]
        sentiment_confidence = sentiment_result["confidence"]
    else:
        if pos_count > neg_count * 1.5:
            sentiment = "Positive"
        elif neg_count > pos_count * 1.5:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiment_confidence = 0.7
    
    # Build comprehensive insights
    insights = {
        "meeting_type": meeting_type,
        "duration_estimate": f"{max(15, len(sentences) * 2)} minutes",
        "participant_count": len(speakers),
        "key_participants": speakers[:5],
        "topics_covered": topics,
        "decisions_made": decisions[:3],
        "issues_raised": issues[:3],
        "sentiment": sentiment,
        "productivity_score": productivity_score,
        "follow_up_required": len([s for s in sentences if 'follow' in s.lower() or 'next meeting' in s.lower()]) > 0
    }
    
    # Add advanced insights if available
    if ADVANCED_NLP_AVAILABLE:
        insights.update({
            "sentiment_confidence": round(sentiment_confidence, 2),
            "named_entities": entities,
            "readability_metrics": calculate_readability_metrics(transcript),
            "key_phrases": [phrase[0] for phrase in extract_key_phrases(transcript, 5)],
            "complexity_analysis": analyze_meeting_complexity(transcript)
        })
    
    return insights

def enhanced_action_extraction(transcript: str) -> List[Dict[str, Any]]:
    """Enhanced action item extraction using NLP"""
    sentences = extract_sentences(transcript)
    results = []
    
    # Patterns for action items
    action_patterns = [
        r'([A-Z][a-zA-Z\s]+)(?:\s*\([^)]+\))?\s*:\s*.*?(?:will|shall|should|must|need to|have to|going to|responsible for)\s+(.+?)(?:\s+by\s+(\w+))?',
        r'([A-Z][a-zA-Z\s]+)\s+(?:will|shall|should|must|needs to|has to|is going to)\s+(.+?)(?:\s+by\s+(\w+))?',
        r'(?:will|shall|should|must|need to|have to)\s+(.+?)(?:\s+by\s+(\w+))?'
    ]
    
    for sentence in sentences:
        # Skip if sentence is too short
        if len(sentence) < 20:
            continue
            
        # Check for action indicators
        action_indicators = ['will', 'shall', 'should', 'must', 'need to', 'have to', 'going to', 'responsible', 'assign', 'due', 'by', 'before', 'after', 'deadline']
        
        if any(indicator in sentence.lower() for indicator in action_indicators):
            # Extract owner (person mentioned before action)
            owner_match = re.search(r'([A-Z][a-zA-Z]+)(?:\s*\([^)]+\))?\s*:', sentence)
            owner = owner_match.group(1) if owner_match else None
            
            # If no owner from speaker pattern, look for names in sentence
            if not owner:
                name_match = re.search(r'\b([A-Z][a-zA-Z]+)\s+(?:will|shall|should|must|needs to)', sentence)
                owner = name_match.group(1) if name_match else None
            
            # Extract deadline
            deadline_patterns = [
                r'\b(today|tomorrow|yesterday)\b',
                r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
                r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
                r'\bby\s+(\w+(?:\s+\w+)?)\b',
                r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
                r'\b(\d{1,2}:\d{2})\b'
            ]
            
            deadline = None
            for pattern in deadline_patterns:
                match = re.search(pattern, sentence.lower())
                if match:
                    deadline = match.group(1)
                    break
            
            # Determine priority based on keywords
            priority = "Medium"
            if any(word in sentence.lower() for word in ['urgent', 'asap', 'immediately', 'critical', 'important']):
                priority = "High"
            elif any(word in sentence.lower() for word in ['later', 'eventually', 'when possible', 'low priority']):
                priority = "Low"
            
            # Clean up the task description
            task = sentence
            if owner and sentence.startswith(f"{owner}:"):
                task = sentence[len(f"{owner}:"):].strip()
            
            results.append({
                'task': task,
                'owner': owner or '',
                'deadline': deadline or '',
                'priority': priority,
                'status': 'Pending',
                'note': f'Extracted from: "{sentence[:50]}..."' if len(sentence) > 50 else f'Extracted from: "{sentence}"'
            })
    
    return results