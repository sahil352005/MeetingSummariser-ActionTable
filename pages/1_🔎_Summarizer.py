import os
import pandas as pd
import streamlit as st
from extractor import parse_mistral_action_items, rule_based_action_extraction
from prompts import SUMMARY_PROMPT, ACTION_ITEM_PROMPT

try:
    from mistral_client import call_mistral
except Exception:
    call_mistral = None

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
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #3b82f6;
    }
    .action-card {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #22c55e;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid #e5e7eb;
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
    use_mistral = st.checkbox('🤖 Use Mistral API (requires env vars)', value=False, help="Enable AI-powered analysis for better results")
with col2:
    st.markdown("")

if st.button('🚀 Generate Summary & Actions', type="primary", use_container_width=True):
    if not st.session_state.transcript or not st.session_state.transcript.strip():
        st.error('❌ Please provide a transcript first!')
    else:
        # Summary generation
        st.markdown("## 📊 Results")
        
        with st.spinner('🧠 Generating summary...'):
            summary = None
            if use_mistral and call_mistral is not None:
                try:
                    summary = call_mistral(SUMMARY_PROMPT.format(transcript=st.session_state.transcript), max_tokens=200)
                except Exception as e:
                    st.warning(f'⚠️ Mistral API unavailable: {str(e)[:100]}... Using fallback method.')
            if not summary:
                sents = [s.strip() for s in st.session_state.transcript.split('\n') if s.strip()]
                summary = '• ' + '\n• '.join(sents[:5]) + '\n\n*Generated using fallback method*'
            
            st.markdown("### 📝 Meeting Summary")
            st.markdown(f'<div class="summary-card">{summary}</div>', unsafe_allow_html=True)

        # Action items extraction
        with st.spinner('🎯 Extracting action items...'):
            items = None
            if use_mistral and call_mistral is not None:
                try:
                    resp = call_mistral(ACTION_ITEM_PROMPT.format(transcript=st.session_state.transcript), max_tokens=512)
                    items = parse_mistral_action_items(resp)
                except Exception as e:
                    st.warning(f'⚠️ Mistral API unavailable: {str(e)[:100]}... Using rule-based extraction.')
            if not items:
                items = rule_based_action_extraction(st.session_state.transcript)

            if items:
                df = pd.DataFrame(items)
                
                # Ensure all required columns exist
                for col in ['task', 'owner', 'deadline', 'note']:
                    if col not in df.columns:
                        df[col] = ''
                
                # Clean up data
                df['owner'] = df['owner'].fillna('').astype(str)
                df['deadline'] = df['deadline'].fillna('').astype(str)
                df['note'] = df['note'].fillna('').astype(str)
                
                st.markdown("### ✅ Action Items")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f'<div class="metric-card"><h4>{len(df)}</h4><p>Total Items</p></div>', unsafe_allow_html=True)
                with col2:
                    unique_owners = len([o for o in df['owner'].unique() if o.strip()])
                    st.markdown(f'<div class="metric-card"><h4>{unique_owners}</h4><p>Assigned Owners</p></div>', unsafe_allow_html=True)
                with col3:
                    with_deadlines = len([d for d in df['deadline'] if d.strip()])
                    st.markdown(f'<div class="metric-card"><h4>{with_deadlines}</h4><p>With Deadlines</p></div>', unsafe_allow_html=True)
                with col4:
                    st.markdown(f'<div class="metric-card"><h4>{"🤖" if use_mistral and call_mistral else "📋"}</h4><p>Method Used</p></div>', unsafe_allow_html=True)
                
                # Action items table
                st.markdown('<div class="action-card">', unsafe_allow_html=True)
                # Reorder columns for better display
                display_df = df[['task', 'owner', 'deadline', 'note']].copy()
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        '📥 Download CSV', 
                        display_df.to_csv(index=False).encode('utf-8'), 
                        'action_items.csv', 
                        'text/csv',
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        '📥 Download JSON', 
                        display_df.to_json(orient='records').encode('utf-8'), 
                        'action_items.json', 
                        'application/json',
                        use_container_width=True
                    )
            else:
                st.info('ℹ️ No action items found in the transcript.')

