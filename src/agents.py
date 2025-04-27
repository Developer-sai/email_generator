"""Agent module using CrewAI for orchestrating the email generation process."""
from typing import Dict, Any, List, Tuple
from crewai import Agent, Task, Crew

from app.data_handler import DataHandler
from app.llm_interface import LLMInterface
from app.email_generator import EmailGenerator


class EmailCrewAgent:
    """Agent class using CrewAI for orchestrating email generation."""

    def __init__(self, llm_interface: LLMInterface):
        """Initialize with an LLM interface.

        Args:
            llm_interface: An instance of LLMInterface
        """
        self.llm_interface = llm_interface
        self.email_generator = EmailGenerator(llm_interface)

    def create_agents(self) -> List[Agent]:
        """Create the agents needed for the email generation process.

        Returns:
            List of CrewAI agents
        """
        try:
            lead_analyst = Agent(
                role="Lead Analyst",
                goal="Analyze lead data to identify key interests and pain points",
                backstory="An expert in understanding customer needs and preferences",
                verbose=True,
                llm=self.llm_interface.llm
            )
            
            email_writer = Agent(
                role="Email Writer",
                goal="Write compelling personalized emails that address lead needs",
                backstory="A skilled copywriter specializing in sales communications",
                verbose=True,
                llm=self.llm_interface.llm
            )
            
            return [lead_analyst, email_writer]
        except Exception as e:
            print(f"Error creating agents: {e}")
            raise RuntimeError(f"Failed to create CrewAI agents: {e}")

    def create_tasks(self, agents: List[Agent], lead: Dict[str, Any], product: Dict[str, Any]) -> List[Task]:
        """Create tasks for the agents.

        Args:
            agents: List of CrewAI agents
            lead: Dictionary containing lead information
            product: Dictionary containing product information

        Returns:
            List of CrewAI tasks
        """
        if len(agents) < 2:
            raise ValueError("Need at least two agents for the CrewAI workflow")
            
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
        
        try:
            lead_analysis_task = Task(
                description=f"""
                Analyze the following lead information:
                Name: {lead_name}
                Job Title: {lead_title}
                Company: {lead_company}
                Industry: {lead_industry}
                Interests: {lead_interests}
                Pain Points: {lead_pain_points}
                LinkedIn Activity: {lead_activity}
                
                Identify:
                1. Key pain points to address
                2. Relevant interests to mention
                3. Personalization opportunities based on LinkedIn activity
                4. Appropriate tone and approach for their position
                """,
                agent=agents[0],
                output_file="lead_analysis.txt"
            )
            
            email_writing_task = Task(
                description=f"""
                Using the lead analysis and product information, create a personalized email:
                
                Product Name: {product_name}
                Description: {product_desc}
                Key Features: {product_features}
                Benefits: {product_benefits}
                
                Create:
                1. An attention-grabbing subject line
                2. A personalized email body that addresses the lead's pain points
                3. A concise mention of relevant product benefits
                4. A clear call to action
                
                Format your response as:
                Subject Line: [Your subject line here]
                
                [Your email body here]
                """,
                agent=agents[1],
                context=[lead_analysis_task],
                output_file="generated_email.txt"
            )
            
            return [lead_analysis_task, email_writing_task]
        except Exception as e:
            print(f"Error creating tasks: {e}")
            raise RuntimeError(f"Failed to create CrewAI tasks: {e}")

    def generate_email_for_lead(self, lead: Dict[str, Any], product: Dict[str, Any]) -> Tuple[str, str]:
        """Generate an email for a specific lead using CrewAI.

        Args:
            lead: Dictionary containing lead information
            product: Dictionary containing product information

        Returns:
            Tuple of (subject_line, email_body)
        """
        try:
            # Direct approach using EmailGenerator for simplicity and efficiency
            return self.email_generator.generate_email(lead, product)
        except Exception as e:
            print(f"Error with direct generation, falling back to CrewAI: {e}")
            
            try:
                # Fallback to CrewAI (more complex but provides reasoning)
                agents = self.create_agents()
                tasks = self.create_tasks(agents, lead, product)
                
                crew = Crew(
                    agents=agents,
                    tasks=tasks,
                    verbose=True
                )
                
                result = crew.kickoff()
                
                # Parse the CrewAI result
                return self.email_generator._parse_generated_content(result)
            except Exception as crew_error:
                print(f"Error with CrewAI generation: {crew_error}")
                return "Error", f"Failed to generate email: {str(crew_error)}"