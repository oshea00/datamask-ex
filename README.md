# Anonymizing via Data Masking
This example shows how to anonymize text before passing to an LLM API.

Two examples are given, each using the [Microsoft Presidio](https://microsoft.github.io/presidio/) framework:
* ```fakeranon.py``` - Custom opeators using Faker to replace PII with faked values of the the same type.
* ```replaceanon.py``` - entity replacement of PII for passing to LLM for categorization and summary.

