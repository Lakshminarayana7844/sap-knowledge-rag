# Retrieval augmented generation

## Idea
Retrieval augmented generation, RAG, answers a question from retrieved documents instead of from model memory alone. The system splits documents into chunks, finds the chunks closest to the question and builds the answer from them.

## Retrieval methods
BM25 is a keyword ranking function that scores chunks by term frequency and rarity. Dense retrieval uses embedding vectors. Hybrid retrieval mixes both.

## Evaluation
Measure retrieval with recall at k, the share of questions where the right chunk is in the top k, and mean reciprocal rank. Check that the system refuses when no chunk is relevant.

## Citations
Return the source file and heading for every answer so users can verify it.
