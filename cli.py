import os
from dotenv import load_dotenv
import openai
import argparse

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_initial_context(file_path):
    if not file_path:
        return []
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            return [{"role": "user", "content": content}]
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found. Starting without initial context.")
        return []

def create_conversation(prompt, model, temperature, chat_log):
    chat_log.append({"role": "user", "content": prompt})
    completion = openai.chat.completions.create(
        model=model,
        messages=chat_log,
        temperature=temperature,
    )
    chat_log.append({"role": "assistant", "content":  completion.choices[0].message.content})
    chat_log_str = "\n".join([f"{message['role'].title()}: {message['content']}" for message in chat_log])
    return chat_log_str

def main(temperature, file_path):
    initial_context = load_initial_context(file_path)
    print("Starting the conversation. Type 'quit' to exit.")
    chat_log = initial_context
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        chat_log_str = create_conversation(user_input, model="gpt-4", temperature=temperature, chat_log=chat_log)
        print(chat_log_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with OpenAI's GPT model.")
    parser.add_argument("--temperature", type=float, default=0.7, help="The temperature setting for the conversation.")
    parser.add_argument("--file-path", type=str, help="Optional file path to load initial conversation context.", default=None)
    args = parser.parse_args()

    main(args.temperature, args.file_path)
