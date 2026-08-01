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
