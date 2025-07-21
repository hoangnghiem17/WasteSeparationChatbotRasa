# Waste Separation Chatbot - RASA AI Implementation

A conversational AI chatbot built with RASA framework that helps users with waste separation and disposal information in Frankfurt am Main, Germany. The chatbot provides detailed guidance on recycling, waste collection schedules, and proper disposal methods for various items.

## Features

- **Intelligent Waste Classification**: Provides detailed information about different waste categories (paper, organic waste, packaging, residual waste, bulky waste, glass)
- **Item-Specific Disposal Guidance**: Queries a comprehensive database to provide specific disposal instructions for individual items
- **FES Integration**: Offers information about Frankfurt's waste management company (FES) including contact details and services
- **Collection Schedule Information**: Provides guidance on waste collection schedules and calendar access

## Architecture

The application consists of three main components:

1. **RASA Core Server**: Handles natural language understanding and conversation management
2. **RASA Actions Server**: Executes custom actions for database queries and dynamic responses
3. **Flask Web Application**: Provides the user interface and handles communication with RASA

## How It Works

### Natural Language Understanding
The chatbot uses RASA's NLU pipeline to understand user intents and extract entities. It can recognize:
- **Intents**: Greetings, questions about waste types, disposal queries, FES information
- **Entities**: Waste types (abfallart), specific items (item), company names (unternehmen)

### Custom Actions
Two main custom actions provide dynamic responses:

1. **`action_mülltrennung_abfallart`**: Provides detailed information about different waste bins and their contents
2. **`action_mülltrennung_entsorgung_einzelitem`**: Queries the database for specific item disposal instructions using fuzzy matching

### Database Integration
The chatbot connects to a SQLite database (`abfallABC_entsorgung.db`) containing comprehensive waste disposal information from the Frankfurt Recycling Center. The database includes:
- Item names and descriptions
- Disposal methods and locations
- Contact information and links

## Data Sources

The chatbot's knowledge base is built from:
- **Frankfurt Recycling Center Data**: Comprehensive waste disposal information from [Recyclingzentrum Frankfurt](https://www.recyclingzentrum-frankfurt.de/abfall-abc)
- **FES Information**: Official data from Frankfurt's waste management company
- **Local Waste Collection Schedules**: Information about collection times and procedures

## Configuration

### RASA Configuration (`config.yml`)
- Language model: German
- Pipeline: spaCy-based NLU pipeline
- Policies: TED policy for dialogue management

### Domain Configuration (`domain.yml`)
- Intents: 11 different conversation intents
- Entities: 5 entity types for information extraction
- Actions: 2 custom actions for dynamic responses
- Responses: Pre-defined responses for common queries

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WasteSeparationChatbotRasa
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   cd db
   python create_db.py
   cd ..
   ```

4. **Train the RASA model**
   ```bash
   rasa train
   ```

5. **Start the application**
   ```bash
   # Option 1: Use the startup script
   chmod +x start_local.sh
   ./start_local.sh
   
   # Option 2: Start services manually
   # Terminal 1: Start RASA server
   rasa run --enable-api
   
   # Terminal 2: Start RASA actions server
   rasa run actions
   
   # Terminal 3: Start Flask application
   python rasa_app/app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - Start chatting with the waste separation assistant!

## Acknowledgments

- **FES Frankfurt**: For providing comprehensive waste management information
- **Recyclingzentrum Frankfurt**: For the detailed waste disposal database
- **RASA Community**: For the excellent conversational AI framework
