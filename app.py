import json
from pathlib import Path
import streamlit as st
from engine import analyze, error_message, MODEL, MAX_BYTES

st.set_page_config(page_title="Document Intelligence", page_icon="📄", layout="wide")
st.title("Business Document Intelligence")
st.caption("Local Gemini sandbox · evidence-based document analysis")
st.warning("Only submit synthetic or non-sensitive documents. Live analysis sends document content to Google and may incur charges.")
for key, default in {"attempts": 0, "history": [], "last": None}.items():
    if key not in st.session_state:
        st.session_state[key] = default
with st.sidebar:
    st.header("Experiment controls")
    st.code(MODEL)
    st.caption("2 MiB maximum file size · 2,048 output tokens per analysis")
    st.write(f"Session attempts: {st.session_state.attempts}/10")
    st.caption("Session limit is not a billing cap and resets when the session ends.")
    st.link_button("Gemini usage", "https://aistudio.google.com/usage")
    st.link_button("Gemini billing", "https://aistudio.google.com/billing")

source = st.radio("Document source", ["Sample invoice", "Upload document"], horizontal=True)
if source == "Sample invoice":
    name = "invoice.txt"
    data = (Path(__file__).parent / "samples" / name).read_bytes()
    st.code(data.decode(), language=None)
else:
    upload = st.file_uploader("PDF, PNG, JPG, TXT or Markdown", type=["pdf","png","jpg","jpeg","txt","md"])
    name, data = (upload.name, upload.getvalue()) if upload else ("", b"")
focus = st.selectbox("Analysis focus", ["General business review", "Invoice and payment review", "Contract obligations and risks", "Report insights and actions"])
consent = st.checkbox("I understand this sends the selected document to Gemini and may cost money.")
if st.button("Run live analysis", type="primary", disabled=not consent or not data or len(data)>MAX_BYTES or st.session_state.attempts>=10):
    st.session_state.attempts += 1
    st.session_state.last = None
    try:
        with st.spinner("Analysing document..."):
            result, tokens, latency = analyze(name, data, focus)
        st.session_state.last = (name, result.model_dump(), tokens, latency)
        st.session_state.history.append({"file": name, "model": MODEL, "latency_ms": latency, **tokens})
    except Exception as exc:
        st.error(error_message(exc))

if st.session_state.last:
    filename, result, tokens, latency = st.session_state.last
    st.subheader("Results: " + filename)
    st.caption("AI-generated findings require human verification.")
    st.write(result["document_type"])
    st.write(result["summary"])
    left, right = st.columns(2)
    with left:
        st.subheader("Key facts")
        for item in result["key_facts"]:
            st.write(item["detail"])
            st.caption(item["evidence"])
    with right:
        st.subheader("Risks")
        for item in result["risks"]:
            st.write(item["detail"])
            st.caption(item["evidence"])
    st.subheader("Recommended actions")
    for item in result["recommended_actions"]:
        st.write("• " + item)
    st.subheader("Missing information")
    for item in result["missing_information"]:
        st.write("• " + item)
    st.download_button("Export analysis JSON", json.dumps(result, indent=2), "analysis.json", "application/json")
    st.metric("Latest request latency (ms)", latency)
    st.json(tokens)

st.divider()
st.subheader("Session usage")
st.caption("Reported token counts only, not actual billed cost or credit balances. Failed requests may still incur charges.")
if st.session_state.history:
    st.dataframe(st.session_state.history, use_container_width=True)
    totals = [x["total_token_count"] for x in st.session_state.history]
    st.metric("Reported total tokens", sum(x for x in totals if x is not None))
else:
    st.info("No successful requests yet.")
