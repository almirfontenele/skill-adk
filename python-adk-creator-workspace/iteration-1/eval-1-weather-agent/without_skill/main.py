"""Main entry point for the Weather Agent."""

import logging
import sys
from src.weather_agent import WeatherAgent
from src.weather_agent.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the weather agent."""
    
    try:
        # Initialize the agent
        logger.info("Initializing Weather Agent...")
        agent = WeatherAgent()
        
        # Example queries
        queries = [
            "What's the current weather in San Francisco?",
            "What's the forecast for New York for the next 7 days?",
            "Compare the weather between London and Paris",
            "Are there any weather alerts for Tokyo?"
        ]
        
        logger.info("Weather Agent started successfully")
        print("\n" + "="*60)
        print("WEATHER AGENT - Interactive Demo")
        print("="*60)
        
        # Run example queries
        for query in queries:
            print(f"\nQuery: {query}")
            print("-" * 60)
            
            response = agent.answer_question(query)
            
            print(f"Response:\n{response.response}")
            if response.tool_calls:
                print(f"\nTools Called: {', '.join(response.tool_calls)}")
            print()
        
        # Interactive mode
        print("="*60)
        print("Enter your own weather questions (type 'quit' to exit):")
        print("="*60)
        
        while True:
            try:
                user_query = input("\nYour question: ").strip()
                
                if user_query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not user_query:
                    print("Please enter a question.")
                    continue
                
                print("-" * 60)
                response = agent.answer_question(user_query)
                
                print(f"Response:\n{response.response}")
                if response.tool_calls:
                    print(f"\nTools Called: {', '.join(response.tool_calls)}")
            
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                print(f"Error: {e}")
    
    except Exception as e:
        logger.error(f"Failed to initialize Weather Agent: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
