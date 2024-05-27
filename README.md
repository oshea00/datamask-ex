# Anonymizing via Data Masking
This example shows how to anonymize text before passing to an LLM Model. I run testing against **Gpt-4o**, **Gpt-3.5 Turbo**, **Llama3 8B** and **Phi3 7B** 

The anonymization example uses the [Microsoft Presidio](https://microsoft.github.io/presidio/)
open-source framework for masking personal identifiable information (PII). It also checks to see if the
summarized/masked test emails will work properly when LLM is asked to categorize and summarize. Finally, a score is given
of properly-categorized input.

Scripts:
* ```replaceanon.py``` - entity replacement of PII in test emails, and passing to LLM for categorization and summary.
* ```generate_emails``` - script used to generate a batch of test categorized emails.
* ```fakeranon.py``` - example using custom operators in *Presidio* to replace PII with faked values - not very useful in the LLM, but perhaps useful in generating test cases

## Testing

The output looks like this:
```
...
--------------------------------------------------
Email: Hello, I need to deposit $15,000 to my account. Account number 5566778899, Name: Lisa Chen, contact email lisachen@mail.com, phone (614) 555-1122.
Masked: Hello, I need to deposit $15,000 to my account. Account number <PHONE_NUMBER>, Name: <PERSON>, contact email <EMAIL_ADDRESS>, phone <PHONE_NUMBER>.
Analyzed Category: ACCOUNT_TRANSACTION
Actual Category: ACCOUNT_TRANSACTION
Summarized email: Sure! The email is a request to deposit $15,000 into an account. The sender provides their account number, name, contact email, and phone number for reference.
Correctly categorized: True
--------------------------------------------------
Email: Can cats and dogs communicate with each other?
Masked: Can cats and dogs communicate with each other?
Analyzed Category: UNKNOWN
Actual Category: UNKNOWN
Summarized email: The email is asking if cats and dogs are able to communicate with each other.
Correctly categorized: True
--------------------------------------------------
Correctly categorized 40 out of 40 or 100.0% emails.
```

I thought it would be interesting to compare the performance of other models using Ollama's OpenAI-compatible API.
The outputs of these experiments are here:
* ```test_gpt4o_output.txt``` - 100% accuracy
* ```test_gpt35turbo_output.txt``` - 100% accuracy
* ```test_llama3_output.txt``` - 92.5% accuracy
* ```test_phi3_output.txt``` - 82.5% accuracy

Gpt-4o and Gpt-3.5-Turbo are, of course, very accurate compared to the smaller Llama3 and Phi3 models. Gpt-4o is faster. These smaller models have a difficult time with the "catch-all" categorization of UNKNOWN, and they tend to treat these cases as a NEW_ACCOUNT request. Also, they tend to ignore the
prompt to return only the category name in the categorization prompt - requiring some string handling to make sure the returned
values are single-words.

Phi3 'summarization' is actually too "gabby" - longer than the original email in many cases.

I am using the exact same prompts across all these tests. In a real-world match-up, it might be useful to customize prompts for
the model you intend to use in production, keeping in mind the usefulness of scoring results. Though, in my case I'd say the smaller
quantized models used for llama3 and Phi3 are probably not up to the task - even with careful prompting. It's not a fair fight.

## Running project examples

You may want to create a virtual python environment using ```venv``` or ```Pipenv```.

* Install the dependencies: ```pip3 install -r requirements.txt```
* Get the spacy model: ```python3 -m spacy download en_core_web_lg```
* Setup your OPENAI_API_KEY.
* Run scripts - example: ```python3 replaceanon.py```





