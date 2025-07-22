import os
from typing import Optional, Union, Callable

from docling_core.types.doc.page import SegmentedPage
from dotenv import load_dotenv

from docling.datamodel.pipeline_options_vlm_model import ApiVlmOptions, ResponseFormat


def groq_vlm_options(
    model: str, 
    prompt: Union[str, Callable[[Optional[SegmentedPage]], str]], 
    format: ResponseFormat = ResponseFormat.MARKDOWN
):
    """
    Configure ApiVlmOptions for the Groq API.
    
    Args:
        model: The Groq model to use (e.g., "llama3-70b-8192", "mixtral-8x7b-32768")
        prompt: Static prompt string or dynamic prompt function
        format: Response format (defaults to MARKDOWN)
    
    Returns:
        ApiVlmOptions configured for Groq API
    """
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    options = ApiVlmOptions(
        url="https://api.groq.com/openai/v1/chat/completions",
        params=dict(
            model=model,
        ),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        prompt=prompt,
        timeout=90,  # Similar timeout to other implementations
        scale=1.0,
        response_format=format,
    )
    return options
