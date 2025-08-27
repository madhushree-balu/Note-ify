import os  # Add this line
import dotenv
from typing import Optional
import google.generativeai as genai

dotenv.load_dotenv(".env")

def get_gemini_response(prompt: str, model_name: str = "gemini-1.5-flash", api_key: Optional[str] = None) -> str:
    """
    Get response from Gemini API for a given prompt.
    
    Args:
        prompt (str): The input prompt/question
        model_name (str): The Gemini model to use (default: "gemini-1.5-flash")
        api_key (str, optional): Your Gemini API key. If None, will use GEMINI_API_KEY env variable
        
    Returns:
        str: The response from Gemini API
        
    Raises:
        ValueError: If API key is not provided
        Exception: If API call fails
    """
    try:
        # Configure API key
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Try to get from environment variable
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("API key not provided. Set GEMINI_API_KEY environment variable or pass api_key parameter")
            genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel(model_name)
        
        # Generate response
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        raise Exception(f"Error getting response from Gemini API: {str(e)}")



