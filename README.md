<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# Runtime performance comparison of spaCy against other NLP libraries

> ⚠️ **This repository is old and deprecated.** For up-to-date benchmark scripts, see the [`projects`](https://github.com/explosion/projects/) repo.

## Set up the corpus DB

The speed test expects to read documents from a simple SQLite table. More corpus
injestors need to be written. So far there's one to create the table from the Gigaword
corpus.

```bash
fab corpus.giga:path_to_gigaword/
```

## Set up the tools

```bash
fab init
```

This should download and install spaCy and other NLP libraries.

## Run a benchmark

```bash
fab speed:parse,spacy,n=1000
fab speed:tag,spacy
fab speed:tag,spacy,nltk,n=10000
fab speed:tokenize,spacy,clearnlp
```
