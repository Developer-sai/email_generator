# AI-Driven Email Generation Prototype

A professional-grade system for generating personalized sales emails by combining lead data and product information through AI reasoning.

## Features

- **Intelligent Email Generation**: Creates compelling, personalized emails based on lead data
- **Multi-Agent Reasoning**: Uses specialized agents to analyze leads and craft effective messaging
- **Flexible Input Processing**: Handles varied lead and product information formats
- **Production-Ready Implementation**: Includes logging, error handling, and security best practices
- **Containerized Deployment**: Simple deployment with Docker

## System Architecture

The application follows a modular design with these key components:

- **Data Handler**: Processes lead and product information from JSON files
- **LLM Interface**: Integrates with OpenAI's API for text generation
- **Email Generator**: Manages the email creation process and output formatting
- **Agent System**: Coordinates the reasoning process using CrewAI
- **Application Core**: Orchestrates the overall workflow

## Project Structure

```
email-generator/
├── app/
│   ├── __init__.py         # Package initialization
│   ├── data_handler.py     # Data loading and processing
│   ├── llm_interface.py    # LLM API integration
│   ├── email_generator.py  # Email content generation
│   ├── agent.py            # CrewAI agent implementation
│   ├── main.py             # Application entry point
├── data/
│   ├── sample_leads.json   # Sample data for testing
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── approach.md             # Technical approach document
```

## Setup & Installation

### Prerequisites

- Docker installed on your system
- OpenAI API key

### Running with Docker

1. **Build the Docker image**:
   ```
   docker build -t email-generator .
   ```

2. **Run the container**:
   ```
   docker run -e OPENAI_API_KEY="your-api-key" -v $(pwd)/output:/app/output email-generator
   ```

3. **Check the results**:
   The generated emails will be available in the `output` directory.

### Local Development Setup

1. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set your API key**:
   ```
   export OPENAI_API_KEY="your-api-key"  # On Windows: set OPENAI_API_KEY=your-api-key
   ```

4. **Run the application**:
   ```
   python app/main.py
   ```

## Configuration

The application can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `DATA_PATH` | Path to the JSON data file | `data/sample_leads.json` |
| `OUTPUT_PATH` | Directory for output files | `output` |

## Using Custom Data

To use your own data, create a JSON file following this structure:

```json
{
  "leads": [
    {
      "id": 1,
      "name": "Lead Name",
      "job_title": "Job Title",
      "company": "Company Name",
      "industry": "Industry",
      "interests": ["interest1", "interest2"],
      "pain_points": ["pain1", "pain2"],
      "linkedin_activity": "Recent LinkedIn activity"
    }
  ],
  "product": {
    "name": "Product Name",
    "description": "Product description",
    "key_features": ["feature1", "feature2"],
    "benefits": ["benefit1", "benefit2"]
  }
}
```

## Output Format

The application generates:

1. Individual JSON files for each lead's email
2. A summary JSON file with all generated emails

Example output:
```json
{
  "lead_id": 1,
  "lead_name": "Sarah Johnson",
  "company": "TechGrowth Solutions",
  "subject_line": "Transforming Marketing Automation for TechGrowth",
  "email_body": "Hi Sarah,\n\nI noticed your recent article about marketing automation ROI..."
}
```

## Error Handling

The application includes comprehensive error handling:

- **Data Validation**: Validates input data structure
- **API Error Handling**: Manages LLM API communication issues
- **Fallback Mechanisms**: Multiple generation strategies if primary approach fails
- **Detailed Logging**: Provides information for troubleshooting

## Security Considerations

- Container runs as non-root user
- API keys passed via environment variables
- Minimal container permissions
- No sensitive data written to logs

## License

This project is licensed under the MIT License - see the LICENSE file for details.