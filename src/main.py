"""Main application module for the AI-driven email generation prototype."""
import os
import json
import sys
import logging
from typing import Dict, Any, List

from app.data_handler import DataHandler
from app.llm_interface import LLMInterface
from app.agent import EmailCrewAgent


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("email_generator")


def generate_emails_for_all_leads(data_path: str, output_path: str = "output") -> List[Dict[str, Any]]:
    """Generate emails for all leads in the dataset.

    Args:
        data_path: Path to the JSON data file
        output_path: Path to save the generated emails

    Returns:
        List of dictionaries containing lead info and generated emails
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Initialize components
    try:
        logger.info(f"Loading data from {data_path}")
        data_handler = DataHandler(data_path)
        
        # Check if API key is set
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            return []
            
        logger.info("Initializing LLM interface")
        llm_interface = LLMInterface()
        
        logger.info("Setting up email agent")
        email_agent = EmailCrewAgent(llm_interface)
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return []
    
    # Get leads and product info
    leads = data_handler.get_all_leads()
    if not leads:
        logger.warning("No leads found in data file")
        return []
        
    product = data_handler.get_product_info()
    if not product:
        logger.warning("No product information found in data file")
        return []
    
    logger.info(f"Found {len(leads)} leads to process")
    results = []
    
    # Generate email for each lead
    for lead in leads:
        lead_name = lead.get("name", "Unknown Lead")
        logger.info(f"Generating email for {lead_name}...")
        
        try:
            subject_line, email_body = email_agent.generate_email_for_lead(lead, product)
            
            result = {
                "lead_id": lead.get("id", "unknown"),
                "lead_name": lead_name,
                "company": lead.get("company", "Unknown Company"),
                "subject_line": subject_line,
                "email_body": email_body
            }
            
            results.append(result)
            
            # Save individual email to file
            lead_filename = f"{output_path}/email_{lead.get('id', 'unknown')}_{lead_name.replace(' ', '_')}.json"
            with open(lead_filename, 'w') as f:
                json.dump(result, f, indent=2)
                
            logger.info(f"Email saved to {lead_filename}")
            
        except Exception as e:
            logger.error(f"Error generating email for {lead_name}: {e}")
    
    if results:
        # Save all results to a single file
        all_emails_path = f"{output_path}/all_generated_emails.json"
        with open(all_emails_path, 'w') as f:
            json.dump({"generated_emails": results}, f, indent=2)
        
        logger.info(f"All emails saved to {all_emails_path}")
    else:
        logger.warning("No emails were successfully generated")
    
    return results


def main():
    """Main entry point for the application."""
    try:
        logger.info("Starting email generation process")
        
        # Get configuration from environment variables with fallbacks
        data_path = os.environ.get("DATA_PATH", "data/sample_leads.json")
        output_path = os.environ.get("OUTPUT_PATH", "output")
        
        if not os.path.exists(data_path):
            logger.error(f"Data file not found: {data_path}")
            sys.exit(1)
        
        generate_emails_for_all_leads(data_path, output_path)
        logger.info("Email generation process completed")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()