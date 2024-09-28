# Health-ChatBot

## Project Overview

This Django application allows patients to interact with an AI bot regarding their health and care plans. The AI bot can respond to health-related inquiries, provide information about care plans, and escalate requests to doctors. This application is designed to ensure efficient communication while maintaining patient confidentiality.

## Features

- **Patient Information**: A single patient with attributes like First Name, Last Name, Date of Birth, Phone Number, Email, Medical Condition, Medication Regimen, Last Appointment DateTime, Next Appointment DateTime, and Doctor’s Name.
  
- **Chat Functionality**: Users can chat with the AI bot, which displays the conversation history with timestamps.
  
- **AI Bot**: The bot responds to health-related questions, handles appointment modification requests, and extracts key entities from conversations.
  
- **Knowledge Graph Integration**: Integrated a Knowledge Graph to store and query patient-related data.
  
- **Multi-Agent System**: Multi-agent system to handle different tasks.
  
- **Conversation Summaries**: Live conversation summaries and medical insights.

## Technology Stack

- **Backend**: Django
- **Database**: PostgreSQL , Neo4j 
- **Language Model**: Gemini (or any LLM model)
- **Additional Libraries**: Langchain and Langgraph

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- An IDE or text editor of your choice

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd patient_chatbot
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Create a PostgreSQL database for the application.
   - Update the `settings.py` file with your database connection details.

5. **Configure LLM and Neo4j Keys**:
   - Open the `llm_config.json` file located in the root directory of the project.
   - Update the `google_api_key` and `neo4j_key` with your respective keys. 

   **File Location**: [llm_config.json](./llm_config.json)

6. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create a Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Application**:
   ```bash
   python manage.py runserver
   ```

### Accessing the Application

- Open your browser and navigate to `http://127.0.0.1:8000/` to interact with the AI bot.

## Usage

- Once the application is running, you can start a conversation with the AI bot. 
- The bot will respond to health-related inquiries and manage appointment requests. 

## Assumptions

- The application is designed for a single patient. Future implementations could include user authentication.
- The bot's knowledge is limited to health-related topics as per the project's specifications.

## Conclusion

This README provides a comprehensive guide to setting up and using the Django Health AI Bot. Feel free to reach out for any issues or questions regarding the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
