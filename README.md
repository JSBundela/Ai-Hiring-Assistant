Below is a sample `README.md` file you can use for your GitHub repository:

---

# TalentScout AI Interviewer 🤖

TalentScout AI Interviewer is an AI-powered technical screening assistant built with Streamlit. It guides candidates through a conversational interview process, collects personal and technical details, generates dynamic technical questions based on a candidate’s technical stack and experience, and performs sentiment analysis on responses.

## Features

- **Conversational Interface:** Engaging chatbot-style conversation powered by Streamlit.
- **Candidate Information Collection:** Gathers candidate details such as full name, email, phone, location, years of experience, and the position being applied for.
- **Dynamic Technical Assessment:** Automatically generates technical interview questions for each technology in the candidate’s stack using the Ollama API and the Mistral model.
- **Follow-Up Questions:** Creates tailored follow-up questions based on candidate answers.
- **Sentiment Analysis:** Analyzes the sentiment of candidate responses using NLTK’s VADER sentiment analyzer.
- **Multi-Language Support:** Translates messages using Deep Translator, supporting languages like English, French, Spanish, German, and Hindi.
- **Session State Management:** Maintains conversation context using Streamlit’s session state.

## Installation

### Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Deep Translator](https://pypi.org/project/deep-translator/)
- [Ollama](https://github.com/ollama/ollama) (Ensure you have access to this API/model)
- [nltk](https://www.nltk.org/)
- [certifi](https://pypi.org/project/certifi/)

### Setup Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/talentscout-ai-interviewer.git
   cd talentscout-ai-interviewer
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**

   Create a `requirements.txt` file with the following content:

   ```txt
   streamlit
   python-dotenv
   deep-translator
   ollama
   nltk
   certifi
   ```

   Then install the packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the NLTK VADER Lexicon:**

   Although the application downloads the lexicon automatically, you can manually ensure it’s available by running:

   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

5. **Set Up Environment Variables:**

   Create a `.env` file in the project root for any necessary environment variables. For example:

   ```env
   API_KEY=your_api_key_here
   OTHER_VARIABLE=your_value
   ```

## Usage

To run the application, execute the following command:

```bash
streamlit run app.py
```

*(Replace `app.py` with the actual name of your main script if it differs.)*

Open your browser and navigate to `http://localhost:8501` to interact with the TalentScout AI Interviewer.

## Project Structure

```
talentscout-ai-interviewer/
├── app.py               # Main Streamlit application script
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies list
├── .env                 # Environment variables file (ensure this is not committed)
└── ...                  # Additional files and assets
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:  
   `git checkout -b feature/your-feature-name`
3. Commit your changes:  
   `git commit -m "Add new feature"`
4. Push to your branch:  
   `git push origin feature/your-feature-name`
5. Open a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) – For making interactive web app development simple.
- [NLTK](https://www.nltk.org/) – For providing powerful natural language processing tools.
- [Ollama](https://github.com/ollama/ollama) – For the AI-driven question generation.
- [Deep Translator](https://pypi.org/project/deep-translator/) – For enabling multi-language support.

---

Feel free to adjust the content to match any additional details or customizations in your project.
