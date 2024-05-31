from openai import OpenAI

client = OpenAI()

categories = open("prompts/categories.txt", "r", encoding="utf-8").read()
example_emails = open("prompts/example_emails.txt", "r", encoding="utf-8").read()
generate_prompt = categories + "\n" + "Here are some examples of 'category - email_text' pairs" + "\n" + \
example_emails + """
\nPlease create 10 email examples of your own selecting randomly from the above categories.
list each category and email pair in the following format:
{ "category": "CATEGORY", "email_text": "EMAIL_TEXT" }
"""
print(generate_prompt)

response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": generate_prompt}])
print(response.choices[0].message.content)

