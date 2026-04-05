# Study Spark: The Demographic-Aware AI Educational Bot 

Study Spark is a next-generation educational assistant built to bridge the gap between generalized AI chatbots and deeply personalized learning. It doesn't just answer questions—it crafts comprehensive, curriculum-aligned learning experiences tailored specifically to the user's age, grade, location, and educational board.

Designed for students and educators alike, Study Spark ingests course materials (PDFs), analyzes context, and delivers multi-tiered explanations paired with quizzes and curated multimedia content.

---

## Why Study Spark? (How It's Different)

Traditional AI chatbots (like ChatGPT or standard customer support bots) provide generic, one-size-fits-all answers. **Study Spark is fundamentally different:**

1. **Demographic-Aware Generation**: Every response is dynamically adjusted based on the student's **Age**, **Grade (Class)**, **Country**, and **Board of Education**. A 10-year-old in a CBSE board learning fractions will get a vastly different explanation and localized examples compared to a college freshman studying abstract algebra.
2. **Contextual Document Analysis (RAG)**: Users can directly interact with their textbooks. The bot parses uploaded PDF documents and restricts its answers to verified source context, mitigating AI hallucinations and ensuring relevance to the syllabus.
3. **Multi-Tiered Learning Output**: Instead of just a wall of text, the bot breaks down complex topics into:
   - **Simple Explanations** (ELI5)
   - **Deep Explanations** (for thorough understanding)
   - **Important Points** (for quick revision)
4. **Built-in Assessment**: Automatically generates contextual quizzes for active recall and self-assessment right inside the chat.
5. **Multimedia Curation**: Automatically fetches and recommends highly relevant educational YouTube videos based on the specific query and demographic context.

---

## Core Features

- **Robust Authentication**: Secure, JWT-based user authentication (with cookies) storing comprehensive demographic profiles in MongoDB.
- **Native PDF Rendering & Split-Screen Dashboard**: A beautiful, modern UI that allows students to view their course materials side-by-side with the AI chat interface.
- **Live AI Processing Pipeline**: A custom classification and handling engine (`main_pipe`) that orchestrates the query understanding and structures the diverse output components.
- **Elegant, Interactive UI**: Responsive design, custom chat bubbles, emoji avatars, and HTML chat exports for saving notes.

---

## Project Structure

```text
edu_bot/
├── apis/                # API route definitions (Blueprint architecture)
│   └── query.py         # Handles PDF uploads and the main query endpoint
├── core/                # Core business logic & database managers
│   ├── main_pipeline.py # The brain of the bot (orchestrates NLP, PDF Search, etc.)
│   └── db_services.py   # MongoDB integration and user management
├── services/            # Specialized service modules
│   ├── pdf_ops.py       # PDF parsing, chunking, and similarity search engine
│   ├── pipeline.py      # Output structuring and formatting
│   └── query_classifier.py # Analyzes query intent based on user demographics
├── static/              # CSS, JavaScript, and static assets
├── templates/           # Flask HTML templates (Dashboard, Login, Profile)
├── .env                 # Environment variables (DB credentials, Secret Keys)
├── config.py            # Application configuration settings
└── app.py               # The main entry point for the Flask application
```

---

## Tech Stack

- **Backend**: Python, Flask, Flask-JWT-Extended
- **Database**: MongoDB
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **AI / NLP**: Custom RAG (Retrieval-Augmented Generation) pipeline, Intelligent Query Classifiers, and contextual prompt engineering.

---

## Getting Started

### Prerequisites
- Python 3.8+
- MongoDB instance (Local or Atlas)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd edu_bot
   ```

2. **Set up a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you have all necessary AI and NLP libraries specified in your requirements)*

4. **Environment Variables**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   SECRET_KEY_FLASK=your_super_secret_key
   DB_ADDR=mongodb+srv://<user>:<password>@cluster...
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```
   The application will be running at `http://localhost:5000`.

---
*Built to empower the next generation of learners through hyper-personalized AI.*
