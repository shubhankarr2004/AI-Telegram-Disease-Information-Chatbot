import logging  #this is the test bot for excel file
import requests
import pandas as pd
from fuzzywuzzy import fuzz
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# === Telegram Bot Token ===
TELEGRAM_BOT_TOKEN = "#insert token here"

# === Local LLaMA 3 API endpoint from LM Studio ===
LLM_API_URL = "http://localhost:1234/v1/chat/completions"

# === Logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# === Function: Search for disease info (description + precautions) ===
def search_disease_info(query, threshold=70):
    query = query.lower()
    description_result = None
    precautions_result = None

    # === Search symptom_Description.csv ===
    try:
        df_desc = pd.read_csv("symptom_Description.csv")
        if 'prognosis' in df_desc.columns:
            for index, row in df_desc.iterrows():
                disease = str(row['prognosis']).lower()
                score = fuzz.partial_ratio(query, disease)

                if score >= threshold:
                    description_result = f"🔹 **Description:** {row['Description']}"
                    break  # stop after first valid match
    except Exception as e:
        description_result = f"Error reading symptom_Description.csv: {e}"

    # === Search symptom_precaution.csv ===
    try:
        df_prec = pd.read_csv("symptom_precaution.csv")
        if 'prognosis' in df_prec.columns:
            for index, row in df_prec.iterrows():
                disease = str(row['prognosis']).lower()
                score = fuzz.partial_ratio(query, disease)

                if score >= threshold:
                    precautions = []
                    for col in row.index:
                        if "Precaution" in col:
                            precaution = str(row[col])
                            if precaution != 'nan':
                                precautions.append(f"- {precaution}")

                    precautions_text = "\n".join(precautions)
                    precautions_result = f"🔹 **Precautions:**\n{precautions_text}"
                    break  # stop after first valid match
    except Exception as e:
        precautions_result = f"Error reading symptom_precaution.csv: {e}"

    # === Combine results ===
    if description_result or precautions_result:
        combined = "✅ **Disease information found:**\n\n"
        if description_result:
            combined += description_result + "\n\n"
        if precautions_result:
            combined += precautions_result
        return combined

    else:
        return None


# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am a testbot.")


# === Message Handler ===
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # 1. Try searching both files
    result = search_disease_info(user_input)
    if result:
        await update.message.reply_text(result)
        return

    # 2. Fall back to LLaMA if no match
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
