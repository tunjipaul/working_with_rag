def chunk_by_sentences(text, max_chunk_size=500):
    """
    Split text into chunks by sentences, keeping sentences intact.
    Args:
        text: The text to chunk
        max_chunk_size: Maximum characters per chunk
    Returns:
        List of text chunks
    """
    # Simple sentence splitting (split on . ! ?)
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # Check if adding this sentence would exceed max size
        if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
            # Save current chunk and start new one
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            # Add sentence to current chunk
            current_chunk += " " + sentence if current_chunk else sentence
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
def chunk_by_paragraphs(text, min_chunk_size=100):
    """
    Split text by paragraphs (double newlines).
    Args:
        text: The text to chunk
        min_chunk_size: Minimum characters per chunk (combine small paragraphs)
    Returns:
        List of text chunks
    """
    # Split by double newlines (paragraph separator)
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # If paragraph is too small, combine with next
        if len(para) < min_chunk_size:
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            # Save previous chunk if exists
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Start new chunk with this paragraph
            current_chunk = para
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
def load_and_chunk_pdf(file_path, chunk_size=500):
    """
    Load a PDF file and chunk it.
    Args:
        file_path: Path to the PDF file
        chunk_size: Characters per chunk
    Returns:
        List of chunks with metadata (including page numbers)
    """
    import PyPDF2
    import os
    chunks_with_metadata = []
    file_name = os.path.basename(file_path)
    # Open PDF
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)
        # Process each page
        for page_num in range(num_pages):
            # Extract text from page
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # Chunk the page text
            # page_chunks = chunk_by_sentences(text, max_chunk_size=chunk_size)
            page_chunks = chunk_by_paragraphs(text, min_chunk_size=chunk_size)
            # Add metadata to each chunk
            for chunk_idx, chunk in enumerate(page_chunks):
                chunks_with_metadata.append({
                    'text': chunk,
                    'metadata': {
                        'source': file_name,
                        'page': page_num + 1,  # 1-indexed
                        'total_pages': num_pages,
                        'chunk_on_page': chunk_idx,
                    }
                })
    return chunks_with_metadata
# Example (you would use this with a real PDF file)
print("PDF loading function ready!")
print("\nUsage:")
print("chunks = \n")
for chunk in load_and_chunk_pdf("Python For Dummies.pdf", chunk_size=500):
    print(f"Chunk Text: \n{chunk['text']}\nMetadata: {chunk['metadata']}\n")







