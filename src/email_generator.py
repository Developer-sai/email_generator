"""Module for generating personalized sales emails."""
from typing import Dict, Any, Tuple

from app.llm_interface import LLMInterface


class EmailGenerator:
    """Class to generate personalized sales emails."""

    def __init__(self, llm_interface: LLMInterface):
        """Initialize with an LLM interface.

        Args:
            llm_interface: An instance of LLMInterface
        """
        self.llm_interface = llm_interface

    def _parse_generated_content(self, content: str) -> Tuple[str, str]:
        """Parse generated content to extract subject line and email body.
        
        Args:
            content: Generated content from LLM
            
        Returns:
            Tuple of (subject_line, email_body)
        """
        subject_line = ""
        email_body = ""
        
        # Clean up the content
        content = content.strip()
        lines = content.split('\n')
        
        # Find the subject line
        for i, line in enumerate(lines):
            line = line.strip()
            if line.lower().startswith("subject line:") or line.lower().startswith("subject:"):
                # Extract subject line without the prefix
                prefix = "subject line:" if line.lower().startswith("subject line:") else "subject:"
                subject_line = line[len(prefix):].strip()
                # The email body is everything after this line
                email_body = "\n".join(lines[i+1:]).strip()
                break
        
        # If no subject line found but content exists, use default subject and full content
        if not subject_line and content:
            return "Generated Email", content
            
        return subject_line, email_body

    def generate_email(self, lead: Dict[str, Any], product: Dict[str, Any]) -> Tuple[str, str]:
        """Generate a personalized email for a lead.

        Args:
            lead: Dictionary containing lead information
            product: Dictionary containing product information

        Returns:
            Tuple of (subject_line, email_body)
        """
        if not lead or not product:
            return "Error", "Insufficient data provided to generate email."
            
        prompt = self.llm_interface.create_email_prompt(lead, product)
        generated_content = self.llm_interface.generate_content(prompt)
        
        # Handle error responses
        if generated_content.startswith("Error"):
            return "Error", generated_content
            
        try:
            return self._parse_generated_content(generated_content)
        except Exception as e:
            print(f"Error parsing generated content: {e}")
            return "Generated Subject", f"Error parsing content: {str(e)}\n\n{generated_content}"