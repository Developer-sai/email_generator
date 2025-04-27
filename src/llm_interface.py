"""Interface for interacting with Language Learning Models."""
import os
from typing import Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage


class LLMInterface:
    """Interface for interacting with Language Learning Models."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """Initialize the LLM interface.

        Args:
            api_key: OpenAI API key (optional, can use env var)
            model_name: Name of the model to use
            temperature: Temperature setting for generation (0.0-1.0)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            
        try:
            self.llm = ChatOpenAI(
                openai_api_key=self.api_key,
                model=model_name,
                temperature=temperature
            )
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            raise RuntimeError(f"Failed to initialize LLM: {e}")

    def generate_content(self, prompt: str) -> str:
        """Generate content using the LLM.

        Args:
            prompt: Prompt text to send to the LLM

        Returns:
            Generated content as string
        """
        if not prompt:
            return "Error: Empty prompt provided"
            
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"Error generating content: {e}")
            return f"Error generating content: {str(e)}"

    def create_email_prompt(self, lead: Dict[str, Any], product: Dict[str, Any]) -> str:
        """Create a prompt for email generation based on lead and product info.

        Args:
            lead: Dictionary containing lead information
            product: Dictionary containing product information

        Returns:
            Formatted prompt string
        """
        # Handle missing data gracefully
        lead_name = lead.get('name', 'Prospect')
        lead_title = lead.get('job_title', 'Professional')
        lead_company = lead.get('company', 'Company')
        lead_industry = lead.get('industry', 'Industry')
        lead_interests = ', '.join(lead.get('interests', ['professional growth']))
        lead_pain_points = ', '.join(lead.get('pain_points', ['efficiency']))
        lead_activity = lead.get('linkedin_activity', 'None')
        
        product_name = product.get('name', 'Our Product')
        product_desc = product.get('description', 'A solution designed to help businesses')
        product_features = ', '.join(product.get('key_features', ['customizable features']))
        product_benefits = ', '.join(product.get('benefits', ['improved efficiency']))
        
        prompt = f"""
        Create a personalized sales email for the following prospect:
        
        LEAD INFORMATION:
        Name: {lead_name}
        Job Title: {lead_title}
        Company: {lead_company}
        Industry: {lead_industry}
        Interests: {lead_interests}
        Pain Points: {lead_pain_points}
        Recent LinkedIn Activity: {lead_activity}
        
        PRODUCT INFORMATION:
        Product Name: {product_name}
        Description: {product_desc}
        Key Features: {product_features}
        Benefits: {product_benefits}
        
        INSTRUCTIONS:
        1. Generate a compelling subject line that references the lead's pain points or interests
        2. Create a personalized email body that:
           - Starts with a personalized opening that references their LinkedIn activity or industry
           - Addresses their specific pain points
           - Briefly introduces our product as a solution
           - Mentions 1-2 relevant benefits or features
           - Ends with a clear, low-pressure call to action
        3. Keep the email concise (150-200 words)
        4. Use a professional but conversational tone
        
        FORMAT YOUR RESPONSE AS:
        Subject Line: [Your subject line here]
        
        [Your email body here]
        """
        return prompt