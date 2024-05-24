import spacy
from faker import Faker
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
from presidio_anonymizer.entities import OperatorConfig
from openai import OpenAI

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
fake = Faker()

# load openai client
client = OpenAI()

def fake_name(x):
    return fake.name()
# fake email
def fake_email(x):
    return fake.email()
# fake phone number
def fake_phone(x):
    return fake.phone_number()

operators = {
    "PERSON": OperatorConfig("custom", {"lambda": fake_name}),
    "EMAIL_ADDRESS": OperatorConfig("custom", {"lambda": fake_email}),
    "PHONE_NUMBER": OperatorConfig("custom", {"lambda": fake_phone}),
}

# Initialize Presidio Analyzer and Anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Function to detect and mask PII in email text
def mask_pii(text):
    results = analyzer.analyze(text=text, entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"], language='en')
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
    return anonymized_text.text

# Function to reverse PII masking
def reverse_pii_masking(masked_text, pii_map):
    # Assuming pii_map is a dictionary mapping masked values to original PII
    for masked_value, original_value in pii_map.items():
        masked_text = masked_text.replace(masked_value, original_value)
    return masked_text

# Function to process text with OpenAI completions API
def process_with_openai(text, prompt):
    messages = [{'role': 'user', 'content': f'{prompt} {text}'}]
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content

# Main function to handle the workflow
def handle_email_workflow(email_text, prompt):
    print("Email text:", email_text)
    # Step 1: Detect and mask PII
    masked_email = mask_pii(email_text)

    # Step 2: Process masked email text with OpenAI API
    processed_text = process_with_openai(masked_email, prompt)
    
    # Step 3: Reverse PII masking in the processed text
    #final_text = reverse_pii_masking(processed_text, pii_map)
    
    return processed_text

# Example usage
email_text = "John Doe's email is john.doe@example.com and his phone number is 123-456-7890, or text 123-333-1212."
prompt = "Summarize the following email:"

result = handle_email_workflow(email_text, prompt)
print(result)

