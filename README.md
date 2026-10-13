# Private Legal AI Workbench

A local-first proof of concept for source-grounded legal knowledge work: retrieve relevant passages, preserve citations, and expose uncertainty.

> This is research assistance infrastructure, not legal advice. It uses synthetic sample matter text.

The code searches passages you pass in memory. It keeps each hit tied to a source and a matter, and it returns an empty list when nothing matches. Matching is token overlap. There is no language model and no network call.

## Philosophy

A private legal AI system should answer from the record, show where an answer came from, respect matter boundaries, and say when the record is insufficient. Retrieval is not authority. Human review remains required.

## Setup

The modules use the Python standard library only (`dataclasses`, `re`, and `unittest`). There is no dependency file and nothing to install with pip. GitHub Actions runs the tests on Python 3.12.

Clone with HTTPS and run commands from the repository root so Python can import `legal_ai`:

```bash
git clone https://github.com/yellowlotuscg/private-legal-ai-workbench.git
cd private-legal-ai-workbench
```

On a machine where the interpreter is `python3` rather than `python`, use `python3` in the commands below. The workflow calls `python` after `actions/setup-python` installs it.

## Usage

### Demo

`legal_ai/demo.py` builds two synthetic passages and searches `matter-a` for `renewal notice`:

| Matter | Source | Text |
| --- | --- | --- |
| `matter-a` | `contract.md` | The agreement renews annually unless notice is given thirty days before renewal. |
| `matter-b` | `memo.md` | The payment dispute was referred to mediation. |

```bash
python3 -m legal_ai.demo
```

That prints:

```text
{'answer_supported': True, 'citations': ['contract.md'], 'matter_boundary': 'matter-a'}
```

`answer_supported` is true when `retrieve` returned at least one passage. `citations` is the `source` of each hit. `matter_boundary` is the matter that was searched. The memo is on `matter-b`, so it is not included.

### Calling retrieval

`legal_ai/__init__.py` is empty. Import from `legal_ai.retrieval`.

```python
from legal_ai.retrieval import Passage, retrieve

passages = [
    Passage(
        "matter-a",
        "contract.md",
        "The agreement renews annually unless notice is given thirty days before renewal.",
    ),
    Passage(
        "matter-b",
        "memo.md",
        "The payment dispute was referred to mediation.",
    ),
]

hits = retrieve("renewal notice", passages, "matter-a")
```

`Passage` is a frozen dataclass with three fields: `matter`, `source`, and `text`.

`retrieve(query, passages, matter, limit=3)` works like this:

1. It splits `query` into lowercase tokens with the regular expression `[a-z0-9]+`. Punctuation is not part of a token, so `thirty-days` becomes the tokens `thirty` and `days`.
2. It keeps passages whose `matter` is exactly equal to the `matter` argument. The comparison is case-sensitive.
3. It scores each remaining passage by how many query tokens also appear in that passage's text, using the same tokenizer.
4. It sorts higher scores first. Passages with the same score stay in their original order.
5. It drops passages with a score of zero, then returns at most `limit` passages. The default limit is 3.

An empty query, an unknown matter, or a query that shares no tokens with the allowed passages returns `[]`. The function does not fill that gap with another passage.

Read `source` and `text` on each returned `Passage` before treating it as support for an answer.

## Tests

`tests/test_retrieval.py` checks two behaviors:

- `test_matter_boundary`: the same text is stored on matters `a` and `b`. A query for `notice` limited to matter `a` returns only `a.md`.
- `test_no_answer`: a query that shares no tokens with the passage returns `[]`.

From the repository root:

```bash
python3 -m unittest discover -s tests -v
```

`.github/workflows/tests.yml` runs `python -m unittest discover -s tests -v` on every push to `main` and every pull request into `main`. The job checks out the repository, sets up Python 3.12, and sets `permissions.contents` to `read`.

## Layout

```text
legal_ai/retrieval.py         Passage and retrieve
legal_ai/demo.py              sample two-matter run
legal_ai/__init__.py          empty package marker
tests/test_retrieval.py       matter boundary and empty-result tests
.github/workflows/tests.yml   unittest on Python 3.12
```

## Limits

Implemented here: deterministic local retrieval, source citations, matter labels, and an explicit no-answer state.

The corpus is the list passed to `retrieve`. Nothing in this repository stores documents, encrypts them, authenticates a user, or applies a retention policy. Production work would add authenticated storage, encryption, retention controls, privilege handling, evaluation datasets, and formal deployment review.

Ranking is a count of shared lowercase alphanumeric tokens. The code does not stem words, expand synonyms, or compare embeddings. A returned passage is a pointer to text you supplied. It is not a legal conclusion. The tests cover matter filtering and the empty result, not a review workflow.

## License

MIT. Copyright (c) 2026 Matthew Coggins. See [LICENSE](LICENSE).
