import json
import os
from groq import Groq
import archive.conversation as conversation
from products import products
from report_format import report_format

# Initialize Groq client
client = Groq(
    api_key="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")

# Create the system message with products and format
system_message = f"""
You are an AI assistant that generates structured retail reports from sales conversations.
Here is the list of products (with aliases):
{products}

Report Format:
{report_format}

Instructions:
- Return strictly a JSON array.
- Detect all products mentioned in the conversation, including aliases.
- If a product alias matches, map it to the correct product.
- Fill in the product details from the provided list.
- Identify all business issues for each product. ONLY include problems or complaints.
- Do NOT include normal business actions like ordering, quantity request, or greetings as issues.
- Use fields from the report format that are non-empty and not "".
- Keep the output in a clean JSON format.
"""


def run_report(conversation_text):
    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Conversation:\n{conversation_text}\n\nGenerate the report as a Python dictionary in the format of report_format. Only output the dictionary, no extra text."}
        ],
        temperature=0.2
    )
    report_str = chat_completion.choices[0].message.content
    try:
        report_dict = eval(report_str, {"__builtins__": None}, {})
    except Exception:
        report_dict = json.loads(report_str)
    return report_dict
