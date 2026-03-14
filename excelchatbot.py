import logging
import requests
import pandas as pd
from fuzzywuzzy import fuzz
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# === Telegram Bot Token ===
TELEGRAM_BOT_TOKEN = ""

# === Local LLaMA 3 API endpoint from LM Studio ===
LLM_API_URL = "http://localhost:1234/v1/chat/completions"

# === Excel Files ===
EXCEL_FILES = ["data1.xlsx", "data2.xlsx"]  # Place both Excel files in the same directory as this script
SEARCH_COLUMNS = ["Name", "Department"]     # Modify based on your Excel structure

# === Logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Function: Search Across Multiple Excel Files ===
def search_excel(query, threshold=70):
    query = query.lower()
    best_match = None
    best_score = 0
    source_file = ""

    for file in EXCEL_FILES:
        try:
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                for col in SEARCH_COLUMNS:
                    if col not in df.columns:
                        continue
                    cell_value = str(row[col]).lower()
                    score = fuzz.partial_ratio(query, cell_value)

                    if score > best_score and score >= threshold:
                        best_match = row
                        best_score = score
                        source_file = file

        except Exception as e:
            return f"Error reading {file}: {e}"

    if best_match is not None:
        # Auto-detect columns
        response = "\n".join([f"{col}: {best_match[col]}" for col in best_match.index])
        return f"Match found in {source_file} (score: {best_score}):\n{response}"
    else:
        return None

# === Function: Summarize Excel Content ===
def summarize_excel():
    summaries = []
    for file in EXCEL_FILES:
        try:
            df = pd.read_excel(file)
            preview = df.head(10).to_string(index=False)
            summaries.append(f"File: {file}\n{preview}")
        except Exception as e:
            summaries.append(f"Error reading {file}: {e}")

    combined = "\n\n".join(summaries)

    prompt = (
        f"Here are previews from 2 Excel files:\n{combined}\n\n"
        "Please summarize the key information in a simple way."
    )

    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes tabular data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(LLM_API_URL, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error summarizing with LLaMA: {e}"

# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am the official chatbot of the All India Radio Akashvani.")

# === Message Handler ===
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # 1. Check for Excel summary request
    if "summary" in user_input.lower() or "overview" in user_input.lower():
        reply = summarize_excel()
        await update.message.reply_text(reply)
        return

    # 2. Try searching Excel files first
    excel_result = search_excel(user_input)
    if excel_result:
        await update.message.reply_text(excel_result)
        return

    # 3. Fall back to LLaMA if no Excel match
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(LLM_API_URL, json=payload)
        result = response.json()
        reply_text = result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        reply_text = f"Error using LLaMA: {e}"

    await update.message.reply_text(reply_text)

# === Main ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
