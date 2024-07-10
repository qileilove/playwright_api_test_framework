import os
import json
import openai
import subprocess

# 设置 OpenAI API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_tests():
    try:
        result = subprocess.run(["pytest"], capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        return None

def get_test_report():
    try:
        with open("report.json") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Report file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from report file.")
        return None

def analyze_with_chatgpt(report):
    try:
        summary = "Please analyze the following pytest report. Provide insights on any failures and suggestions for improvement:\n\n"
        summary += json.dumps(report, indent=2)

        response = openai.Completion.create(
            engine="davinci",
            prompt=summary,
            max_tokens=150
        )

        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Analysis failed due to an error with OpenAI."


def main():
    print("Running tests...")
    test_output = run_tests()
    if test_output is None:
        return

    print("Tests completed. Generating report...")
    report = get_test_report()
    if report is None:
        return

    analysis = analyze_with_chatgpt(report)
    print("ChatGPT Analysis:")
    print(analysis)

if __name__ == "__main__":
    main()
