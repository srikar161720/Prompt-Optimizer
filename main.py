import requests
import openai
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

# Azure AI Language Service
LANGUAGE_SERVICE_KEY = "AZqdz7RzZmVV71tT9qs6oHldBxII2MqpYNEgtPFs7qDyFPzzDjafJQQJ99BCACYeBjFXJ3w3AAAaACOGSUsI"
LANGUAGE_SERVICE_ENDPOINT = "https://promptoptimizer-lang-service.cognitiveservices.azure.com/"

# Azure AI Content Safety
CONTENT_SAFETY_KEY = "4vrZyAAm3pdUjGnaAqzWSQ3pG6Q9iIj24eBIt8Pb5BTfHJl28KPvJQQJ99BCACYeBjFXJ3w3AAAHACOGtWT1"
CONTENT_SAFETY_ENDPOINT = "https://promptoptimizer-content-safety.cognitiveservices.azure.com/"

# Azure OpenAI Service
OPENAI_KEY = "<insert Azure OpenAI service key>"
OPENAI_ENDPOINT = "https://promptoptimizer-openai.openai.azure.com/"
OPENAI_DEPLOYMENT_NAME = "PromptOptimizer-openai"

# Azure Clients
text_analytics_client = TextAnalyticsClient(
    endpoint=LANGUAGE_SERVICE_ENDPOINT, credential=AzureKeyCredential(LANGUAGE_SERVICE_KEY)
)
content_safety_client = ContentSafetyClient(
    endpoint=CONTENT_SAFETY_ENDPOINT, credential=AzureKeyCredential(CONTENT_SAFETY_KEY)
)

def check_grammar(prompt):
    documents = [prompt]
    response = text_analytics_client.recognize_pii_entities(documents)
    
    if response:
        corrected_text = response[0].redacted_text
        return corrected_text
    return prompt

def moderate_content(prompt):
    response = content_safety_client.analyze_text(prompt)
    
    if response.hate or response.violence or response.self_harm or response.sexual:
        return f"Warning: Your input contains inappropriate content."
    
    return prompt

def enhance_prompt(prompt):
    openai.api_key = OPENAI_KEY
    response = openai.ChatCompletion.create(
        model=OPENAI_DEPLOYMENT_NAME,
        messages=[{"role": "system", "content": "Rephrase and optimize user input for clarity."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def process_prompt(user_prompt):
    print(f"Original Prompt: {user_prompt}")

    # Step 1: Check Grammar
    corrected_prompt = check_grammar(user_prompt)
    print(f"After Grammar Check: {corrected_prompt}")

    # Step 2: Moderate Content
    moderated_prompt = moderate_content(corrected_prompt)
    print(f"After Content Moderation: {moderated_prompt}")

    # Step 3: Enhance Prompt Clarity
    enhanced_prompt = enhance_prompt(moderated_prompt)
    print(f"Final Optimized Prompt: {enhanced_prompt}")

    return enhanced_prompt

# Example usage
if __name__ == "__main__":
    user_input = input("Enter your prompt: ")
    processed_prompt = process_prompt(user_input)