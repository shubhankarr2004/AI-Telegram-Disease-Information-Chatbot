# 🤖 AI Telegram Disease Information Chatbot

An intelligent **Telegram chatbot** that retrieves disease information from structured datasets and answers user queries using **fuzzy search and a local LLaMA model**.

The chatbot can provide **disease descriptions, precautions, and conversational responses** by combining dataset lookup with AI-generated answers.

---

# ✨ Features

* 📊 Searches **structured datasets (CSV / Excel)** for disease information
* 🧠 Uses **fuzzy matching** to understand approximate queries
* 🩺 Provides **disease descriptions and recommended precautions**
* 🤖 AI fallback responses powered by **LLaMA 3 (via LM Studio)**
* 💬 Fully functional **Telegram chatbot interface**
* 🔍 Handles spelling mistakes and partial disease names
* ⚡ Fast information retrieval from datasets

---

# 🗂️ Project Structure

```
.
├── excelchatbot.py              # Telegram chatbot for Excel dataset queries
├── excelread.py                 # Telegram chatbot for disease dataset queries
├── symptom_Description.csv      # Disease descriptions dataset
├── symptom_precaution.csv       # Disease precautions dataset
├── README.md                    # Project documentation
```

---

# ⚙️ Technologies Used

### Programming Language

* Python

### Libraries

* pandas
* fuzzywuzzy
* python-telegram-bot
* requests
* logging

### AI Model

* LLaMA 3 (running locally using **LM Studio**)

##**Workflow**

User message
↓
Telegram handler
↓
Query processing
↓
Information retrieval
↓
Bot response


**Medical Knowledge Retrieval**

User question
↓
Embedding
↓
Vector search
↓
Medical documents
↓
LLM answer



### Datasets

* `symptom_Description.csv`
* `symptom_precaution.csv`

---

# ⚡ Setup Instructions

## 1️⃣ Clone the Repository

```
git clone https://github.com/shubhankarr2004/disease-telegram-chatbot
```

---

## 2️⃣ Create Virtual Environment & Install Dependencies

```
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

Install required packages:

```
pip install pandas fuzzywuzzy python-telegram-bot requests
```

---

## 3️⃣ Install and Run LM Studio

Download LM Studio and run **LLaMA 3 model locally**.

Ensure the local API server is running at:

```
http://localhost:1234/v1/chat/completions
```

---

## 4️⃣ Set Your Telegram Bot Token

Create a Telegram bot using **BotFather** and replace the token inside:

```
excelchatbot.py
excelread.py
```

Example:

```
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
```

---

## 5️⃣ Add Dataset Files

Place the following files in the project directory:

```
symptom_Description.csv
symptom_precaution.csv
```

---

## 6️⃣ Run the Chatbot

Run either of the scripts:

```
python excelchatbot.py
```

or

```
python excelread.py
```

If successful, the terminal will show:

```
Bot is running...
```

Now open Telegram and start chatting with your bot.

---

# 💬 Example Queries

User:

```
dengue
```

Bot:

```
Disease information found

Description: Dengue is a mosquito-borne viral infection...

Precautions:
- Avoid mosquito bites
- Drink plenty of fluids
- Rest adequately
```

---

User:

```
what is malaria
```

Bot:

```
AI-generated response using the LLaMA model
```

---

# 🚀 Future Improvements

* Vector database integration (**FAISS / ChromaDB**)
* Better NLP-based disease detection
* Web interface using **React or HTML/CSS**
* Cloud deployment (AWS / Render / Railway)
* Multi-language support

---

# 🩺 Applications

* Healthcare information assistants
* Hospital helpdesk chatbots
* Government health information systems
* Educational medical tools

---

# 📜 License

This project is intended for **educational and research purposes**.

---

# 👨‍💻 Author

Developed by Shubhankar Singh✨
LinkedIn: www.linkedin.com/in/shubhankarr
GitHub: https://github.com/shubhankarr2004
