from openai import OpenAI

client = OpenAI()

categoryies = open("prompts/categories.txt", "r").read()
example_emails = open("prompts/example_emails.txt", "r").read()
generate_prompt = categoryies + "\n" + "Here are some examples of 'category - email_text' pairs" + "\n" + example_emails + """
\nPlease create 20 email examples of your own selecting randomly from the above categories.
list each category and email pair in the following format:
{ "category": "CATEGORY", "email_text": "EMAIL_TEXT" }
"""
print(generate_prompt)

client.chat.completions.create(
    model="gpt-4o", 
    messages=[{"role": "system", "content": generate_prompt}])
response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": generate_prompt}])
print(response.choices[0].message.content)

