import openai
from openai import OpenAI

# Step 1: Initialize client with your API key
client = OpenAI(api_key="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")

# Step 2: Load the scraped .txt file
filename = "pinnaclefirearmsandtraining_com_text.txt"
with open(filename, "r", encoding="utf-8") as file:
    scraped_text = file.read()

# Step 3: Prompt ChatGPT to extract brand names
prompt = (
    "Here is some text scraped from a retailer's website:\n\n"
    + scraped_text
    + "\n\nBased on this text, list all the brand names the retailer carries. "
    + "Only include proper brand names, not categories or product types. "
    + "Return them as a clean bullet-point list."
)

# Step 4: Call the GPT API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
)

# Step 5: Print the extracted brands
print("\n🔍 GPT Output:\n")
print(response.choices[0].message.content)

# Step 6: Remove duplicate brand names
# Split by lines, strip whitespace and keep unique entries
lines = response.choices[0].message.content.strip().splitlines()
unique_lines = list(dict.fromkeys([line.strip() for line in lines]))

# Step 7: Print cleaned, unique list
print("\n✅ Cleaned Brand List (No Duplicates):\n")
for line in unique_lines:
    print(line)
