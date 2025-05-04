# A sample AI chatbot which provide specific information about a fictional product.

This Python program demonstrates an AI-powered chatbot that leverages OpenAI's GPT-4 model and custom function tools to provide detailed information about the fictional product BoostNutri+. The chatbot dynamically answers user queries by searching a structured FAQ database, ensuring accurate and context-aware responses.

## Key Features
- **Natural Language Interaction**: Users can ask questions conversationally (e.g., "Can children take BoostNutri+?").

- **FAQ Integration**: Uses a predefined FAQ dataset to retrieve product-specific details like ingredients, pricing, usage guidelines, and certifications.

- **Function Calling**: Implements a custom search_faqs tool to extract keywords from queries and match them to relevant FAQ answers.

- **Dynamic Responses**: Combines OpenAI’s language model with structured data to generate human-like, contextually accurate replies.


## Installation

1. Install the required dependencies:
   - Python 3.x
   - `openai`: To install `openai`, use pip:
   

   ```bash
   pip install openai
   ```

## Usage

### Program Overview

Deploy the chatbot as a customer support tool to handle product inquiries, provide instant responses, and guide users through product details. Users interact naturally, and the system bridges conversational AI with precise FAQ data retrieval.


### Explanation

1. **FAQ Data Structure**:

    It acts as a knowledge base for the chatbot. Predefined questions and answers about the product are stored here. The search_faqs function scans these answers to match user queries.

    Note: This could be replaced with a database or API call in a production environment.

2. **search_faqs Function**:

    Finds FAQ answers containing specific keywords.

    Key Logic:
    - Converts search terms to lowercase for case-insensitive matching.
    - Checks if any keyword appears in FAQ answers.
    - Returns matched answers or a default "no info" message.

3. **OpenAI Tool Definition**:

    Teaches GPT-4 when and how to use the search_faqs function.
    Key Fields:
    - parameters: Defines that the model must provide a search_word_list (array of keywords).
    - required: Ensures the model always provides the search_word_list argument.
   

4. **Function Calling Workflow**:
    - **Step 1**: The user’s question (e.g., "What are BoostNutri+ affect on health?") is sent to OpenAI.
    - **Step 2**: GPT-4 analyzes the query and decides to call search_faqs with inferred keywords (e.g., ["BoostNutri+", "affect", "health"]).
    - **Step** 3: The code executes search_faqs and returns FAQ results.
    - **Step 4**: Results are fed back to GPT-4 to generate a natural-language response.

