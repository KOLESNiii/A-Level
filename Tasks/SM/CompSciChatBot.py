import os
import openai
openai.api_key = "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"
#print(openai.Model.retrieve("text-curie-001"))
while True:
    inp = str(input("Enter question:"))
    result = openai.Completion.create(
        model="text-curie-001",
        prompt=inp + " OCR J277",
        max_tokens=1000,
        temperature=0.9,
        presence_penalty=0.6,
        frequency_penalty=0.5
    )["choices"][0]["text"]
    print(result)