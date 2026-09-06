import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")or st.secrets.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found! Please check your .env file."
    )
from dotenv import load_dotenv
from google import genai


# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


# Make sure the API key exists before starting the Gemini client
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found! Please check your .env file."
    )


# Create a Gemini client using our API key
client = genai.Client(api_key=api_key)


def process_lead_with_ai(scraped_data: dict) -> dict:
    """
    Use the scraped website data to generate a company summary,
    identify a possible pain point, and create a personalized email pitch.
    """

    # Don't send anything to the AI if the website scraping failed
    if not scraped_data.get("success"):
        return {
            "success": False,
            "error": "The scraped website data is not valid."
        }


    # Give the AI the website information and clearly explain
    # what kind of sales analysis we want it to generate
    prompt = f"""
    You are a world-class B2B sales expert.
    Analyze the following website information:

    Website URL: {scraped_data['url']}
    Title: {scraped_data['title']}
    Meta Description: {scraped_data['meta_description']}
    Website Content: {scraped_data['content']}

    Please provide the following output:

    1. **Summary:** Explain what the company does in exactly 2 sentences.
    2. **Pain Point:** Identify a possible problem or area where this business could improve.
    3. **Personalized Email Pitch:** Write a compelling cold email in exactly 3 sentences.
    """


    try:
        # Send our prompt to Gemini and ask it to generate the analysis
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        # Return the AI-generated response after removing extra spaces
        return {
            "success": True,
            "ai_analysis": response.text.strip()
        }

    except Exception as e:
        # If Gemini fails for any reason, return the error
        # instead of crashing the entire application
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":

    # Use some sample website data to test the AI function
    # This lets us test the AI engine without running the scraper first
    mock_data = {
        "success": True,
        "url": "https://example.com",
        "title": "Example Domain",
        "meta_description": "Illustration domain for documents",
        "content": "This domain is for use in illustrative examples in documents."
    }


    # Start the test and send the sample data to Gemini
    print("Starting AI analysis...")

    result = process_lead_with_ai(mock_data)


    # Display the generated analysis if everything worked
    if result["success"]:
        print("\n--- AI Generated Output ---\n")
        print(result["ai_analysis"])

    else:
        # Display the error if the AI request failed
        print("\nError:", result["error"])