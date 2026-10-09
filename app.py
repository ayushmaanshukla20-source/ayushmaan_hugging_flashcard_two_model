
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

def main():
    topic = input("Enter a topic: ").strip()

    if not topic:
        print("Please enter a topic.")
        return

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY not found in .env")
        return

    client = genai.Client(api_key=api_key)

    models = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite"
]

    prompt = f"""
    Generate exactly 5 study flashcards about {topic}
    for a second-year B.Tech AI and ML student.

    Include a question and a concise, accurate answer
    for each flashcard. Number them from 1 to 5.
    """

    results = {}

    for model in models:
        print(f"\n{'=' * 45}")
        print(f"Model: {model}")
        print("=" * 45)

        try:
            start = time.time()

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            elapsed = time.time() - start

            print(response.text)
            print(f"\nResponse time: {elapsed:.2f} seconds")

            results[model] = elapsed

        except Exception as e:
            print(f"Model failed: {e}")

    print("\n\nMODEL COMPARISON")
    print("-" * 35)

    if results:
        for model, elapsed in results.items():
            print(f"{model}: {elapsed:.2f} seconds")

        if len(results) == 2:
            faster = min(results, key=results.get)
            print(f"\nFaster model in this run: {faster}")
    else:
        print("Neither model completed successfully.")
        print("Check the API error messages above.")

if __name__ == "__main__":
    main()