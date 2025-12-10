from google import genai

api_key = input("Enter your Gemini API key: ")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello! What is AI?")

print(response.text)


