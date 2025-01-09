#!/usr/bin/env python
import sys
import warnings

from technical_analyst.crew import TechnicalAnalyst
from dotenv import load_dotenv
import os
from datetime import datetime as dt

load_dotenv()

company=os.environ.get("COMPANY","")
date=dt.now().strftime("%m-%d")
timestamp=dt.now().timestamp()
data_dir=f"output/{date}/{company}"
while (company==""):
    company=input("검색할 회사명 : ")

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
        'company': company,
    }
    TechnicalAnalyst(data_dir,timestamp).crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'company': company
    }
    try:
         TechnicalAnalyst(data_dir,timestamp).crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TechnicalAnalyst(data_dir,timestamp).crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'company': company
    }
    try:
        TechnicalAnalyst(data_dir,timestamp).crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
