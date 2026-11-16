#!/usr/bin/env python3
"""
Minimal LongLLMLingua example for RAG prompt compression.
Requires: pip install llmlingua
"""

from llmlingua import PromptCompressor

def compress_rag_context(
    chunks: list[str],
    question: str,
    instruction: str = "Answer the question using only the provided context.",
    target_token: int = 500,
) -> dict:
    """
    Compress retrieved chunks with LongLLMLingua (query-aware).

    Returns the full compressor result dict containing:
    - compressed_prompt
    - origin_tokens
    - compressed_tokens
    - ratio
    """
    compressor = PromptCompressor()  # uses default small model

    result = compressor.compress_prompt(
        context=chunks,
        instruction=instruction,
        question=question,
        target_token=target_token,
        rank_method="longllmlingua",
        condition_in_question="after",
        reorder_context="sort",
        dynamic_context_compression_ratio=0.3,
        condition_compare=True,
        force_tokens=["\n", "?", "```", "###"],  # protect structure
    )
    return result


if __name__ == "__main__":
    # Example retrieved chunks (replace with real retrieval output)
    example_chunks = [
        "Document 1: The refund policy allows returns within 30 days of purchase with original receipt.",
        "Document 2: Shipping usually takes 3-5 business days for domestic orders.",
        "Document 3: Customer support is available Monday-Friday 9am-5pm EST via email or chat.",
        "Document 4: Extended warranties can be purchased at checkout for selected products.",
    ]

    question = "What is the refund policy?"

    result = compress_rag_context(example_chunks, question, target_token=80)

    print("=== Compressed Prompt ===")
    print(result["compressed_prompt"])
    print()
    print(f"Original tokens : {result.get('origin_tokens')}")
    print(f"Compressed tokens: {result.get('compressed_tokens')}")
    print(f"Ratio           : {result.get('ratio')}")
