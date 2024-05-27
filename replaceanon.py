import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from openai import OpenAI
import json

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# load openai client
client = OpenAI()

# client = OpenAI(
#     base_url='http://localhost:11434/v1',
#     api_key='ollama',
# )

LLM_MODEL = "gpt-4o"
#LLM_MODEL = "llama3"

# Initialize Presidio Analyzer and Anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
entities = ['PERSON', 'ORGANIZATION', 'EMAIL_ADDRESS', 'CREDIT_CARD', 'US_SSN', 'AU_ABN', 'IN_AADHAAR', 'US_DRIVER_LICENSE', 'US_PASSPORT', 
            'AU_TFN', 'US_BANK_NUMBER', 'EMAIL', 'PHONE_NUMBER', 'IN_PAN', 'URL', 'CRYPTO', 'AU_ACN']

# Function to detect and mask PII in text
def mask_pii(text):
    results = analyzer.analyze(text=text, entities=entities, language='en')
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized_text.text

# Function to process text with OpenAI completions API
def process_with_openai(text, prompt):
    messages = [{'role': 'user', 'content': f'{prompt} {text}'}]
    response = client.chat.completions.create(model=LLM_MODEL, messages=messages)
    return response.choices[0].message.content

example_emails_json = open('test_emails.json').read()
example_emails = json.loads(example_emails_json)

summarize_prompt = "Summarize the following email:"
classify_prompt = """
You know about the following categories of "name - description" format:
ACCOUNT_INFORMATION - Request for information about an account, such as balance, or recent transactions.
NEW_ACCOUNT - Request for information about a product or service.
UPDATE_ACCOUNT - Request to change information on an account, such as address, or account holder name.
ACCOUNT_TRANSACTION - Request to withdraw or deposit money or securities from an account.
UNKNOWN - Request that does not fit into any of the above categories.

Please classify the following email into one of the above categories.
Return only the category name matching the given email:
"""

# print supported entities of the analyzer
print(f'Supported entities: {entities}')
print("--------------------------------------------------")

correctly_categorized_count = 0

for email in example_emails:
    print(f"Email:", email['email_text'])
    masked_email = mask_pii(email['email_text'])
    print("Masked:", masked_email)
    raw_categorized = process_with_openai(masked_email, classify_prompt)
    categorized = raw_categorized.split()[0].strip().upper()
    result = process_with_openai(masked_email, summarize_prompt)
    print(f'Analyzed Category: {raw_categorized}')
    print(f'Actual Category: {email["category"]}')
    print(f'Summarized email: {result}')
    correctly_categorized = email['category'] == categorized
    if correctly_categorized:
        correctly_categorized_count += 1
    print(f'Correctly categorized: {correctly_categorized}')
    print("--------------------------------------------------")

print(f'Correctly categorized {correctly_categorized_count} out of {len(example_emails)} or {100*correctly_categorized_count/len(example_emails)}% emails.')

