from services.llm_service import call_llm


def chunk_text(
    text,
    chunk_size=8000
):
    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):
        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


def summarize_chunk(
    chunk,
    chunk_number,
    total_chunks
):

    prompt = f"""
You are MIDA.

Summarize Part {chunk_number} of {total_chunks}.

TEXT:

{chunk}

Requirements:

- Capture important events and ideas.
- Preserve key details.
- Use concise paragraphs.
- Focus on information that will be useful
  for creating a complete document summary later.
"""

    return call_llm(prompt)


def summarize_document(text):

    if not text.strip():
        return "No content available to summarize."

    chunks = chunk_text(
        text,
        chunk_size=8000
    )

    chunk_summaries = []

    total_chunks = len(chunks)

    for idx, chunk in enumerate(chunks):

        summary = summarize_chunk(
            chunk,
            idx + 1,
            total_chunks
        )

        chunk_summaries.append(
            summary
        )

    combined_summary = "\n\n".join(
        chunk_summaries
    )

    final_prompt = f"""
You are MIDA.

The following are summaries of different sections
of a larger document.

SECTION SUMMARIES:

{combined_summary}

Create a final comprehensive summary.

Requirements:

- Executive Summary
- Main Topics
- Key Findings
- Important Details
- Conclusion

Use markdown headings.
"""

    return call_llm(
        final_prompt
    )