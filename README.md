# Private Legal AI Workbench

A local-first proof of concept for source-grounded legal knowledge work: retrieve relevant passages, preserve citations, and expose uncertainty.

> This is research assistance infrastructure, not legal advice. It uses synthetic sample matter text.

## Philosophy

A private legal AI system should answer from the record, show where an answer came from, respect matter boundaries, and say when the record is insufficient. Retrieval is not authority. Human review remains required.

## Run

```bash
python -m legal_ai.demo
python -m unittest discover -s tests -v
```

Implemented here: deterministic local retrieval, source citations, matter labels, and an explicit no-answer state. Production work would add authenticated storage, encryption, retention controls, privilege handling, evaluation datasets, and formal deployment review.

Relevant practices include NIST AI RMF, NIST Privacy Framework, OWASP LLM guidance, least privilege, data classification, retention controls, confidentiality, privilege awareness, and citation traceability.

## Implemented

The repository contains working code, not mockups:

- Deterministic local retrieval (`legal_ai/retrieval.py`): a query is split into lowercase alphanumeric terms and matched against passage text without any external service.
- Source citations: every returned passage keeps its `source` label (for example `contract.md`), so an answer points back to the passage it came from.
- Matter labels: every passage belongs to one `matter`, and retrieval only ever considers passages from the requested matter, so one matter cannot leak into another.
- Ranking by term overlap: passages sharing more query terms rank first, and only passages sharing at least one term are returned.
- An explicit no-answer state: when nothing matches, retrieval returns an empty list rather than a guess.
- A runnable demo (`python -m legal_ai.demo`) that retrieves from a synthetic two-matter corpus and prints whether an answer is supported plus the citation sources.

## Limitations

- The corpus is in-memory and synthetic. There is no document store, ingestion pipeline, or real matter data.
- Matching is keyword overlap on lowercased tokens. There is no semantic search, no embeddings, and no large language model in this proof of concept.
- Retrieval is not authority and the demo output is not legal advice. A human reviewer must read the cited passages before any use.
- There is no storage, encryption, retention control, privilege handling, or authentication in this code; those are listed as production work in the README.
- The suite covers the retrieval core only (matter boundary and no-answer behavior), not a full review workflow.

## Tests

The standard-library `unittest` suite lives in `tests/test_retrieval.py` and verifies that:

- retrieval respects the matter boundary: with two matters containing the same text, a query for one matter returns only that matter's passage;
- an unrelated query returns an empty list (the no-answer state).

Run it locally with `python -m unittest discover -s tests -v`. GitHub Actions runs the same command on every push to `main` and every pull request into `main` (see `.github/workflows/tests.yml`), with read-only token permissions and no credentials stored in the workflow.
