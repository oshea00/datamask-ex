import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from openai import OpenAI

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# load openai client
client = OpenAI()

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
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content

example_emails = [
"""Hi, I am writing to inquire about my account balance. My account number is 1234567-0 and my name is John Doe.
My email is johnd@gmail.com, and my phone number is (555) 123-4567.""",
"""Dave Edwards. My account number is SN1234567 and I'd like to withdraw all funds from my account.
My email is johnd@gmail.com, and my phone number is (206) 555-1212.""",
"""Hi Mark, My account number is ABN123 and I'd like to deposit 10,000 USD into my account.
Will this trigger any CTR? My credit card is Amex 378282246310005 expiration 12/2027""",
"""Robots are stealing my luggage Dave. Sincerely, Hal"""
]

summarize_prompt = "Summarize the following email:"
classify_prompt = """
You know about the following categories of "name - description" format:
ACCOUNT_INFORMATION - Request for information about an account, such as balance, or recent transactions.
NEW_ACCOUNT - Request for information about a product or service.
UPDATE_ACCOUNT - Request to change information on an account, such as address, or account holder name.
ACCOUNT_TRANSACTION - Request to withdraw or deposit money or securities from an account.
UNKNOWN - Request that does not fit into any of the above categories.

Please classify the following email into one of the above categories by returning the category name.
"""

# print supported entities of the analyzer
print(f'Supported entities: {entities}')
print("--------------------------------------------------")

for email_text in example_emails:
    print("Email text:", email_text)
    masked_email = mask_pii(email_text)
    print("Masked:", masked_email)
    categorized = process_with_openai(masked_email, classify_prompt)
    result = process_with_openai(masked_email, summarize_prompt)
    print(f'Category: {categorized}')
    print(f'Summarized email: {result}')
    print("--------------------------------------------------")

