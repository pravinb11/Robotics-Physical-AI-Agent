from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Explain what a Physical AI agent is in one paragraph."
)

print(response.text)
