from crewai import Agent,Crew,Task
from custom_crewai_tool import stock_news,stock_price,income_stmt,balance_sheet,insider_transactions,scrape_tool
import os
from datetime import datetime as dt
from dotenv import load_dotenv

load_dotenv()

company=os.environ.get("COMPANY","")
date=dt.now().strftime("%m-%d")
timestamp=dt.now().timestamp()
data_dir=f"output/{date}/{company}"
while (company==""):
    company=input("검색할 회사명 : ")


researcher=Agent(
    role="Researcher",
    goal="""Gather and interpret vast amounts of data to provide a comprehensive overview of the sentiment and news surrounding a stock.""",
    backstory="""You're skilled in gathering and interpreting data from various sources. You read each data source carefuly and extract the most important information. Your insights are crucial for making informed investment decisions.""",
    tools=[
        scrape_tool,stock_news
    ],
)

technical_analyst=Agent(
    role="Technial Analyst",
    goal="""Analyzes stock movements, providing insights into trends, entry points and levels""",
    backstory="""These technical analysts are experts at predicting stock movements, and the insights they provide are invaluable to their clients.""",
    tools=[
        stock_price
    ],
)

financial_analyst=Agent(
    role="Financial Analyst",
    goal="""Use financial statements to evaluate a stock's financial health and performance.""",
    backstory="""He is an experienced investment expert who makes recommendations based on the company's financial soundness.""",
    tools=[
        income_stmt,
        balance_sheet,
        insider_transactions
    ],
)

hedge_fund_manager=Agent(
    role="Hedge Fund Manager",
    goal="""We want to manage our stock portfolio and maximize profits.""",
    backstory="""He is an investment expert with frequent experience in making profitable investment decisions.""",
    verbose=True,
)


research = Task(
    description="""Gather and analyze the latest news and market sentiment surrounding {company}'s stock. Provide a summary of the news and any notable shifts in sentiment.""",
    agent=researcher,
    expected_output="""Your final answer MUST be a detailed summary of the news and market sentiment surrounding the stock.""",
    async_execution=True,
)

technical_analysis = Task(
    description="""Conduct a technical analysis of the {company}'s stock price movements and identify key support and resistance levels chart patterns.""",
    agent=technical_analyst,
    expected_output="""Your final answer MUST be a report with potential entry points, price targets and any other relevant information.""",
    output_file=f"{data_dir}/technical_analysis_{timestamp:.0f}.md",
    async_execution=True,
)

financial_analysis = Task(
    description="""Analyze the {company}'s financial statements, balance sheet, insider trading data and other metrics to evaluate {company}'s financial health and performance.""",
    agent=financial_analyst,
    expected_output="""Your final answer MUST be a report with an overview of {company}'s revenue, earnings, cash flow, and other key financial metrics.""",
    output_file=f"{data_dir}/financial_analysis_{timestamp:.0f}.md",
    async_execution=True,
)
investment_recommendation = Task(
    description="""Based on the Current market situation, research, technical analysis, and financial analysis reports, provide a detailed investment recommendation for {company} stock.""",
    agent=hedge_fund_manager,
    expected_output="""Your final answer MUST be a detailed recommendation to BUY, SELL or HOLD the stock. Provide a clear rationale for your recommendation.""",
    context=[research, technical_analysis, financial_analysis],
    output_file=f"{data_dir}/investment_recommendation_{timestamp:.0f}.md"
)

crew=Crew(
    tasks=[research,technical_analysis,financial_analysis,investment_recommendation],
    agents=[researcher,technical_analyst,financial_analyst,hedge_fund_manager],
    verbose=2
)

result=crew.kickoff(inputs={"company":company})