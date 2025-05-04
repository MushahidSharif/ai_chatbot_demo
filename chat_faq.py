from openai import OpenAI
import json

API_KEY="<USE YOUR OWN KEY>"
MODEL= "gpt-4o-mini"

# Sample FAQ data (replace with a file load or API call as needed)
FAQS = [
    {
        "question": "What is BoostNutri+?",
        "answer": "BoostNutri+ is a plant-based nutritional supplement designed to support energy, immunity, and overall wellness. It combines essential vitamins, minerals, and organic superfoods."
    },
    {
        "question": "What are the key ingredients in BoostNutri+?",
        "answer": "BoostNutri+ contains organic spirulina, ashwagandha, turmeric, green tea extract, Vitamin B12, Vitamin D3, and magnesium."
    },
    {
        "question": "Is BoostNutri+ suitable for vegans?",
        "answer": "Yes, BoostNutri+ is 100% vegan, gluten-free, and non-GMO. It contains no animal-derived ingredients."
    },
    {
        "question": "What package sizes are available for BoostNutri+?",
        "answer": "BoostNutri+ is available in 30-serving (300g), 60-serving (600g), and 90-serving (900g) packages."
    },
    {
        "question": "How much does BoostNutri+ cost?",
        "answer": "The 30-serving package is priced at $29.99, 60-serving at $49.99, and 90-serving at $69.99."
    },
    {
        "question": "How do I use BoostNutri+?",
        "answer": "Mix one scoop (10g) of BoostNutri+ with water, juice, or a smoothie once daily, preferably in the morning."
    },
    {
        "question": "Can children use BoostNutri+?",
        "answer": "BoostNutri+ is formulated for adults. Please consult a pediatrician before giving it to children under 12."
    },
    {
        "question": "Does BoostNutri+ contain caffeine?",
        "answer": "Yes, it contains a small amount of natural caffeine (40mg per serving) from green tea extract."
    },
    {
        "question": "Where is BoostNutri+ manufactured?",
        "answer": "BoostNutri+ is manufactured in the USA in an FDA-registered, GMP-certified facility."
    },
    {
        "question": "How should I store BoostNutri+?",
        "answer": "Store in a cool, dry place away from direct sunlight. Reseal the package tightly after each use."
    }
]

def search_faqs(search_word_list):
    if len(search_word_list) ==0       :
        raise ValueError("Atleast one search word is required.")

    # Normalize search terms (ignore case)
    terms = [term.lower() for term in search_word_list if term]

    matches = []
    for faq in FAQS:
        answer_lower = faq["answer"].lower()
        if any(term in answer_lower for term in terms):
            matches.append(faq["answer"])

    return matches if matches else ["No relevant information found."]

def get_answer_from_chatbot(question):

    tools = [
    {
        "type": "function",
        "function": {
            "name": "search_faqs",
            "description": "Searches FAQs about the BoostNutri+ product that matches one or more keywords in the paramter list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_word_list": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of all words to search in the FAQ answers.",
                    }
                },
                "required": ["search_word_list"]

            }
        }
    }
    ]


    user_input = question

    # client = OpenAI(
    #   api_key=API_KEY,
    # )

    client = OpenAI(
      base_url="https://models.inference.ai.azure.com",  #use this url for free testing of openai models from azure. # For using OpenAI remove this base_url.
      api_key=API_KEY,
    )

    # Step 1: Send user's message to GPT with function tool
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.function.name == "search_faqs":
                args = json.loads(tool_call.function.arguments)
                print('calling function:', tool_call.function.name, args)
                keywords = args.get("search_word_list", [])
                results = search_faqs(keywords)

                followup = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "user", "content": user_input},
                        message,
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": "search_faqs",
                            "content": json.dumps(results)
                        }
                    ]
                )

                print("\nAssistant:", followup.choices[0].message.content)
    else:
        print("\nAssistant:", message.content)

if __name__ == "__main__":

    get_answer_from_chatbot("What are BoostNutri+ affect on health")
