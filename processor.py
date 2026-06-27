import os
import re
from typing import List, Dict, Any


class DocumentProcessor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        # Ensure the data directory exists locally
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load_and_chunk_file(self, filename: str) -> List[Dict[str, Any]]:
        """
        Reads a text file and breaks it down into small text chunks (sentences).
        Returns a list of dictionaries containing the chunk text and metadata.
        """
        file_path = os.path.join(self.data_dir, filename)
        chunks = []

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

            # Clean up excessive whitespaces or newlines
            text = re.sub(r'\s+', ' ', text).strip()

            # A simple sentence-splitting regex (looks for ., !, or ? followed by a space)
            sentences = re.split(r'(?<=[.!?])\s+', text)

            for index, sentence in enumerate(sentences):
                if len(sentence.strip()) > 10:  # Skip empty or meaningless short fragments
                    chunks.append({
                        "source": filename,
                        "chunk_index": index,
                        "text": sentence.strip()
                    })
        return chunks

    def process_all_files(self) -> List[Dict[str, Any]]:
        """Scans the data directory and processes every text file."""
        all_chunks = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt"):
                print(f"Processing: {filename}")
                file_chunks = self.load_and_chunk_file(filename)
                all_chunks.extend(file_chunks)
        return all_chunks


# בדיקה פשוטה לחלק הזה בקוד
if __name__ == "__main__":
    # 1. Initialize our processor
    processor = DocumentProcessor()

    # 2. Actually invoke the processing loop on your 3 files
    processed_chunks = processor.process_all_files()

    # 3. Print out what we found in memory
    print("\n--- Processing Complete! ---")
    print(f"Total text chunks extracted to RAM: {len(processed_chunks)}")

    # Let's peek at the first 3 chunks to see what they look like
    print("\nPeeking at the first few chunks in memory:")
    for chunk in processed_chunks[:3]:
        print(f"Source File: {chunk['source']} | Index: {chunk['chunk_index']}")
        print(f"Text: \"{chunk['text']}\"")
        print("-" * 40)