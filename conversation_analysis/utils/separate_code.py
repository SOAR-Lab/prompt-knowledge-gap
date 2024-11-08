from openai import OpenAI
client = OpenAI(api_key='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')

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant for separating code and stack traces (or error "
                                  "messages) from text."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message.content)