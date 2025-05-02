from transformers import pipeline

# 强制使用 PyTorch 后端
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")


def summarize_text(text, max_len=120):
    if not text.strip():
        return ""
    result = summarizer(text, max_length=max_len, min_length=30, do_sample=False)[0]
    return result["summary_text"]
