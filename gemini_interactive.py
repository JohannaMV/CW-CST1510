from google import genai

api_key = input("Enter your Gemini API key: ")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

history = []

print("Gemini Console Chat (type 'quit' to exit)")
print("-" * 50)

while True:
    user_input = input("You: ")

    if user_input == "quit":
        break

    history.append({"role": "user", "content": user_input})

    prompt = "\n".join(f"{m['role']}: {m['content']}" for m in history)

    response = model.generate_content(prompt)
    reply = response.text

    history.append({"role": "assistant", "content": reply})
    print("AI:", reply, "\n")
