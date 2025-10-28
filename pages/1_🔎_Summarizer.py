import os
import pandas as pd
import streamlit as st
import json
from nlp_summarizer import generate_summary, analyze_meeting_insights, enhanced_action_extraction

from audio_processor import transcribe_audio

# Custom CSS for modern styling
st.markdown("""
<style>
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .input-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .result-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    .summary-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #0ea5e9;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
    }
    .summary-card h4 {
        color: #0c4a6e;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .summary-card ul {
        margin: 0.5rem 0;
        padding-left: 1rem;
    }
    .action-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #16a34a;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.15);
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 2px solid #e2e8f0;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .metric-card h4 {
        color: #1e293b;
        font-size: 1.5rem;
        margin-bottom: 0.25rem;
        font-weight: 700;
    }
    .metric-card p {
        color: #64748b;
        font-size: 0.875rem;
        margin: 0;
        font-weight: 500;
    }
    .upload-area {
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: #f8fafc;
    }
    .tab-content {
        padding: 1rem 0;
    }
    .insight-section {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    .summary-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🔎 Summarizer & Action Items</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Transform your meetings into actionable insights</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for transcript persistence
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

# Input section
st.markdown("## 📥 Input Options")

tab1, tab2 = st.tabs(["📝 Text Input", "🎤 Audio Input"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### Paste your meeting transcript below:")
    transcript = st.text_area(
        'Meeting Transcript', 
        value=st.session_state.transcript,
        height=300,
        placeholder="Paste your meeting transcript here...\n\nExample:\nJohn: Let's discuss the Q4 project timeline.\nSarah: I think we should aim for completion by December 15th.\nMike: I'll prepare the budget report by Friday.",
        key="text_input"
    )
    # Update session state when text changes
    if transcript != st.session_state.transcript:
        st.session_state.transcript = transcript
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### Upload an audio file:")
    
    audio_file = st.file_uploader(
        "Choose audio file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
        help="Supported formats: MP3, WAV, M4A, OGG, FLAC"
    )
    
    if audio_file:
        st.success(f"✅ File uploaded: {audio_file.name}")
        
        if st.button("🎯 Transcribe Audio", type="primary"):
            progress = st.progress(0.0, text="Transcribing audio...")
            temp_path = f"temp_{audio_file.name}"
            with open(temp_path, "wb") as f:
                f.write(audio_file.getbuffer())
            
            def on_progress(p: float):
                try:
                    progress.progress(p, text=f"Transcribing... {int(p*100)}%")
                except Exception:
                    pass
            
            audio_transcript = transcribe_audio(temp_path, on_progress=on_progress)
            os.remove(temp_path)
            progress.empty()
            
            if audio_transcript:
                st.success("🎉 Transcription completed!")
                # Update session state with transcribed text
                st.session_state.transcript = audio_transcript
                st.rerun()  # Refresh to show the transcribed text
            else:
                st.error("❌ Failed to transcribe audio. Please try again.")
    else:
        st.info("👆 Upload an audio file to transcribe it to text.")
    st.markdown('</div>', unsafe_allow_html=True)

# Show current transcript if available
if st.session_state.transcript:
    st.markdown("## 📄 Current Transcript")
    with st.expander("View/Edit Current Transcript", expanded=False):
        edited_transcript = st.text_area(
            "Edit transcript if needed",
            value=st.session_state.transcript,
            height=200,
            key="edit_transcript"
        )
        if edited_transcript != st.session_state.transcript:
            st.session_state.transcript = edited_transcript
            st.rerun()

# Processing section
st.markdown("## ⚙️ Processing Options")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🧠 Enhanced NLP Analysis Enabled**")
    st.info("Advanced natural language processing for comprehensive meeting analysis")
with col2:
    st.markdown("")

if st.button('🚀 Generate Summary & Actions', type="primary", use_container_width=True):
    if not st.session_state.transcript or not st.session_state.transcript.strip():
        st.error('❌ Please provide a transcript first!')
    else:
        # Summary and insights generation
        st.markdown("## 📊 Results")
        
        # Generate meeting insights
        with st.spinner('🔍 Analyzing meeting insights...'):
            try:
                insights = analyze_meeting_insights(st.session_state.transcript)
            except Exception as e:
                st.warning(f'⚠️ Could not generate insights: {e}')
                insights = None
        
        # Display insights if available
        if insights:
            st.markdown("### 📈 Meeting Analytics Dashboard")
            st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                meeting_type = insights.get("meeting_type", "N/A")
                type_icon = "💼" if "Product" in meeting_type else "📋"
                st.markdown(f'<div class="metric-card"><h4>{type_icon}</h4><h4>{meeting_type}</h4><p>Meeting Type</p></div>', unsafe_allow_html=True)
            with col2:
                participant_count = insights.get("participant_count", "N/A")
                st.markdown(f'<div class="metric-card"><h4>👥</h4><h4>{participant_count}</h4><p>Participants</p></div>', unsafe_allow_html=True)
            with col3:
                productivity = insights.get("productivity_score", "N/A")
                prod_color = "#22c55e" if productivity >= 7 else "#f59e0b" if productivity >= 4 else "#ef4444"
                st.markdown(f'<div class="metric-card"><h4 style="color: {prod_color}">📈</h4><h4 style="color: {prod_color}">{productivity}/10</h4><p>Productivity</p></div>', unsafe_allow_html=True)
            with col4:
                sentiment = insights.get("sentiment", "N/A")
                sentiment_icon = "😊" if sentiment == "Positive" else "😐" if sentiment == "Neutral" else "🙁"
                sentiment_color = "#22c55e" if sentiment == "Positive" else "#64748b" if sentiment == "Neutral" else "#ef4444"
                st.markdown(f'<div class="metric-card"><h4 style="color: {sentiment_color}">{sentiment_icon}</h4><h4 style="color: {sentiment_color}">{sentiment}</h4><p>Sentiment</p></div>', unsafe_allow_html=True)
        
        with st.spinner('🧠 Generating summary...'):
            summary = generate_summary(st.session_state.transcript)
            
            st.markdown("### 📝 Meeting Summary")
            # Convert markdown-style formatting to HTML for better display
            html_summary = summary.replace('**', '<strong>').replace('**', '</strong>')
            html_summary = html_summary.replace('\n\n', '</p><p>').replace('\n', '<br>')
            html_summary = html_summary.replace('•', '<li style="margin: 0.5rem 0; color: #374151;">')
            html_summary = html_summary.replace('   •', '<li style="margin: 0.3rem 0 0.3rem 20px; color: #6b7280;">')
            html_summary = f'<div style="font-size: 1rem; line-height: 1.7;"><p>{html_summary}</p></div>'
            st.markdown(f'<div class="summary-card">{html_summary}</div>', unsafe_allow_html=True)

        # Action items extraction
        with st.spinner('🎯 Extracting action items...'):
            items = enhanced_action_extraction(st.session_state.transcript)

            if items:
                df = pd.DataFrame(items)
                
                st.markdown("### ✅ Action Items")
                
                # Action Items Metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.markdown(f'<div class="metric-card"><h4>{len(df)}</h4><p>Total Items</p></div>', unsafe_allow_html=True)
                with col2:
                    owners = df['owner'].dropna().astype(str).str.strip()
                    unique_owners = owners[owners != ''].nunique()
                    st.markdown(f'<div class="metric-card"><h4>{unique_owners}</h4><p>Assigned</p></div>', unsafe_allow_html=True)
                with col3:
                    deadlines = df['deadline'].dropna().astype(str).str.strip()
                    with_deadlines = (deadlines != '').sum()
                    st.markdown(f'<div class="metric-card"><h4>{with_deadlines}</h4><p>With Deadlines</p></div>', unsafe_allow_html=True)
                with col4:
                    if 'priority' in df.columns:
                        high_priority = (df['priority'] == 'High').sum()
                        st.markdown(f'<div class="metric-card"><h4>{high_priority}</h4><p>High Priority</p></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="metric-card"><h4>-</h4><p>High Priority</p></div>', unsafe_allow_html=True)
                with col5:
                    st.markdown(f'<div class="metric-card"><h4>🧠 NLP</h4><p>Enhanced Analysis</p></div>', unsafe_allow_html=True)
                
                # Action items table with enhanced display
                st.markdown('<div class="action-card">', unsafe_allow_html=True)
                
                # Configure column display
                column_config = {
                    "task": st.column_config.TextColumn("Task Description", width="large"),
                    "owner": st.column_config.TextColumn("Owner", width="medium"),
                    "deadline": st.column_config.TextColumn("Deadline", width="medium"),
                    "priority": st.column_config.SelectboxColumn(
                        "Priority",
                        options=["High", "Medium", "Low"],
                        width="small"
                    ) if 'priority' in df.columns else None,
                    "status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["Pending", "In Progress", "Completed"],
                        width="small"
                    ) if 'status' in df.columns else None,
                    "note": st.column_config.TextColumn("Notes", width="medium")
                }
                
                # Remove None values from column_config
                column_config = {k: v for k, v in column_config.items() if v is not None}
                
                st.dataframe(
                    df, 
                    use_container_width=True,
                    column_config=column_config,
                    hide_index=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download buttons and additional insights
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        '📥 Download CSV', 
                        df.to_csv(index=False).encode('utf-8'), 
                        'action_items.csv', 
                        'text/csv',
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        '📥 Download JSON', 
                        df.to_json(orient='records').encode('utf-8'), 
                        'action_items.json', 
                        'application/json',
                        use_container_width=True
                    )
                with col3:
                    if insights:
                        # Enhanced insights download with more data
                        enhanced_insights = insights.copy()
                        if 'readability_metrics' in insights:
                            enhanced_insights['readability_summary'] = f"Readability: {insights['readability_metrics']}"
                        
                        insights_json = json.dumps(enhanced_insights, indent=2, default=str)
                        st.download_button(
                            '📊 Download Advanced Insights',
                            insights_json.encode('utf-8'),
                            'advanced_meeting_insights.json',
                            'application/json',
                            use_container_width=True
                        )
                
                # Display comprehensive insights
                if insights:
                    st.markdown("---")
                    st.markdown("### 🔍 Advanced Meeting Analytics")
                    
                    # Advanced metrics if available
                    if insights.get('complexity_analysis'):
                        complexity = insights['complexity_analysis']
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(f'<div class="metric-card"><h4>📊</h4><h4>{complexity["complexity_score"]}/10</h4><p>Complexity</p></div>', unsafe_allow_html=True)
                        with col2:
                            st.markdown(f'<div class="metric-card"><h4>🔧</h4><h4>{complexity["technical_level"]}</h4><p>Technical Level</p></div>', unsafe_allow_html=True)
                        with col3:
                            confidence = insights.get('sentiment_confidence', 0.7)
                            st.markdown(f'<div class="metric-card"><h4>🎯</h4><h4>{int(confidence*100)}%</h4><p>Confidence</p></div>', unsafe_allow_html=True)
                        with col4:
                            entities_count = len(insights.get('named_entities', {}).get('PERSON', []))
                            st.markdown(f'<div class="metric-card"><h4>🏷️</h4><h4>{entities_count}</h4><p>Named Entities</p></div>', unsafe_allow_html=True)
                    
                    # Detailed insights in columns
                    insight_col1, insight_col2, insight_col3 = st.columns(3)
                    
                    with insight_col1:
                        if insights.get('key_phrases'):
                            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                            st.markdown("**🔑 Key Phrases**")
                            for phrase in insights['key_phrases'][:4]:
                                st.markdown(f"<div style='padding: 0.25rem 0; color: #475569;'>• {phrase}</div>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        elif insights.get('topics_covered'):
                            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                            st.markdown("**🎯 Topics Discussed**")
                            for topic in insights['topics_covered'][:4]:
                                st.markdown(f"<div style='padding: 0.25rem 0; color: #475569;'>• {topic}</div>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    with insight_col2:
                        if insights.get('decisions_made'):
                            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                            st.markdown("**✅ Key Decisions**")
                            for decision in insights['decisions_made'][:3]:
                                clean_decision = decision.replace('"', '').strip()[:80] + "..." if len(decision) > 80 else decision.replace('"', '').strip()
                                st.markdown(f"<div style='padding: 0.25rem 0; color: #475569;'>• {clean_decision}</div>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    with insight_col3:
                        if insights.get('named_entities') and insights['named_entities'].get('PERSON'):
                            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                            st.markdown("**👥 Key People**")
                            for person in insights['named_entities']['PERSON'][:4]:
                                st.markdown(f"<div style='padding: 0.25rem 0; color: #475569;'>• {person}</div>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        elif insights.get('issues_raised'):
                            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                            st.markdown("**⚠️ Issues Identified**")
                            for issue in insights['issues_raised'][:3]:
                                clean_issue = issue.replace('"', '').strip()[:80] + "..." if len(issue) > 80 else issue.replace('"', '').strip()
                                st.markdown(f"<div style='padding: 0.25rem 0; color: #475569;'>• {clean_issue}</div>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info('ℹ️ No action items found in the transcript.')
                
                # Still show insights even if no action items
                if insights and any(insights.get(key) for key in ['topics_covered', 'decisions_made', 'issues_raised']):
                    st.markdown("### 🔍 Meeting Insights")
                    
                    insight_col1, insight_col2, insight_col3 = st.columns(3)
                    
                    with insight_col1:
                        if insights.get('topics_covered'):
                            st.markdown("**📋 Topics Covered:**")
                            for topic in insights['topics_covered']:
                                st.markdown(f"• {topic}")
                    
                    with insight_col2:
                        if insights.get('decisions_made'):
                            st.markdown("**✅ Decisions Made:**")
                            for decision in insights['decisions_made']:
                                st.markdown(f"• {decision}")
                    
                    with insight_col3:
                        if insights.get('issues_raised'):
                            st.markdown("**⚠️ Issues Raised:**")
                            for issue in insights['issues_raised']:
                                st.markdown(f"• {issue}")

