import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

# Step 1: Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Step 2: Load the scraped .txt file
filename = "pinnaclefirearmsandtraining_com_text.txt"
with open(filename, "r", encoding="utf-8") as file:
    scraped_text = file.read()

# Step 3: Split the scraped text into chunks
chunk_size = 3000  # characters, safe for gpt-3.5-turbo
chunks = [scraped_text[i:i + chunk_size] for i in range(0, len(scraped_text), chunk_size)]

# Step 4: Send each chunk to GPT and collect results
from openai import OpenAI

client = OpenAI()
all_brands = []

for i, chunk in enumerate(chunks):
    prompt = (
        f"Here is some text scraped from a retailer's website:\n\n{chunk}\n\n"
        "Based on this text, list all the brand names the retailer carries. "
        "Only include proper brand names, not categories or product types. "
        "Return them as a clean bullet list."
    )

    print(f"\n🔹 Processing chunk {i + 1}/{len(chunks)}...\n")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    result = response.choices[0].message.content
    all_brands.append(result)

# Step 5: Print all collected brand names
print("\n✅ All Extracted Brands:")
for part in all_brands:
    print(part)


# Step 6: Remove duplicate brand names
# Split by lines, strip whitespace and keep unique entries
lines = response.choices[0].message.content.strip().splitlines()
unique_lines = list(dict.fromkeys([line.strip() for line in lines]))

# Step 7: Print cleaned, unique list
print("\n✅ Cleaned Brand List (No Duplicates):\n")
for line in unique_lines:
    print(line)
