#!/usr/bin/env python
import sys
import warnings

from discogsworkflow.crew import Discogsworkflow

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'username': 'simonallocca6'
    }

    try:
        print("\n" + "="*60)
        print("🎵 Starting Discogs Collection Workflow")
        print("="*60)
        print(f"\nUsername: {inputs['username']}")
        print("\nThis workflow will:")
        print("  1. Analyze your Discogs collection")
        print("  2. Generate 10 personalized song suggestions")
        print("  3. Search for available releases on Discogs")
        print("  4. Create a 'CrewSuggested' folder with all matches")
        print("  5. Identify the top 3 most popular releases")
        print("  6. Create a 'CrewPopular' folder with the top picks")
        print("\n" + "="*60 + "\n")
        
        result = Discogsworkflow().crew().kickoff(inputs=inputs)
        
        print("\n" + "="*60)
        print("✅ Discogs Workflow Completed Successfully!")
        print("="*60)
        print("\nCheck your Discogs collection for the new folders:")
        print("  • CrewSuggested_[timestamp]")
        print("  • CrewPopular_[timestamp]")
        print("\n" + "="*60 + "\n")
        
        return result
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ Error occurred while running the crew")
        print("="*60)
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "username": "simonallocca6"
    }
    try:
        Discogsworkflow().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Discogsworkflow().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "username": "simonallocca6"
    }

    try:
        Discogsworkflow().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "username": "simonallocca6"
    }

    try:
        result = Discogsworkflow().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
