from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from technical_analyst.tools.custom_tool import stock_news, stock_price, income_stmt, balance_sheet, insider_transactions,scrape_tool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TechnicalAnalyst():
	"""TechnicalAnalyst crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self,data_dir,timestamp):
		self.data_dir=data_dir
		self.timestamp=timestamp



	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[scrape_tool,stock_news]
		)
	@agent
	def technical_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_analyst'],
			verbose=True,
			tools=[stock_price]
		)
	@agent
	def financial_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['financial_analyst'],
			verbose=True,
			tools=[income_stmt, balance_sheet, insider_transactions]
		)
	@agent
	def hedge_fund_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['hedge_fund_manager'],
			verbose=True,
		)


	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_file=f"{self.data_dir}/research_{self.timestamp:.0f}.md"
		)
	@task
	def technical_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['technical_analysis_task'],
			output_file=f"{self.data_dir}/technical_analysis_{self.timestamp:.0f}.md"
		)
	@task
	def financial_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['financial_analysis_task'],
			output_file=f"{self.data_dir}/financial_analysis_{self.timestamp:.0f}.md"
		)
	@task
	def investment_recommendation_task(self) -> Task:
		return Task(
			config=self.tasks_config['investment_recommendation_task'],
			output_file=f"{self.data_dir}/investment_recommendation_{self.timestamp:.0f}.md"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TechnicalAnalyst crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
