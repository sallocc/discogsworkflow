from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.mcp import MCPServerStdio
from typing import List
import os
import sys
import logging

# Configure logging for debugging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Counter to track agent instantiations
_agent_instantiation_count = 0

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Discogsworkflow():
    """Discogsworkflow crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    
    @agent
    def song_recommender(self) -> Agent:
        """Agent that generates song recommendations based on user's collection."""
        return Agent(
            config=self.agents_config['song_recommender'], # type: ignore[index]
            verbose=True
        )

    @agent
    def popularity_picker(self) -> Agent:
        """Agent that analyzes and ranks songs by popularity metrics."""
        return Agent(
            config=self.agents_config['popularity_picker'], # type: ignore[index]
            verbose=True
        )

    @agent
    def discogs_api_agent(self) -> Agent:
        """Agent that interacts with Discogs API via MCP server."""
        global _agent_instantiation_count
        _agent_instantiation_count += 1
        
        #logger.debug(f"🔍 DEBUG: discogs_api_agent instantiated (count: {_agent_instantiation_count})")
        
        # Use ultra-short wrapper script to prevent tool name truncation
        # The wrapper has minimal path length: just "d.py"
        parent_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath('.')))))
        mcp_wrapper = os.path.join(parent_folder, "discogs_mcp.py")
        
        #logger.debug(f"🔍 DEBUG: MCP wrapper path: {mcp_wrapper}")
        
        # Configure MCP server using native crewAI MCP support
        # Ultra-short path maximizes room for tool name differentiation within 64-char limit
        mcp_config = MCPServerStdio(
            command="python3",
            args=[mcp_wrapper],
            env=os.environ.copy()
        )
        
        #logger.debug(f"🔍 DEBUG: Creating Agent with ultra-short wrapper 'd.py'")
        
        return Agent(
            config=self.agents_config['discogs_api_agent'], # type: ignore[index]
            mcps=[mcp_config],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    
    @task
    def get_collection_task(self) -> Task:
        """Task to retrieve all releases from user's Discogs collection."""
        return Task(
            config=self.tasks_config['get_collection_task'], # type: ignore[index]
        )

    @task
    def generate_suggestions_task(self) -> Task:
        """Task to generate 50 song suggestions based on collection."""
        return Task(
            config=self.tasks_config['generate_suggestions_task'], # type: ignore[index]
            context=[self.get_collection_task()]
        )

    @task
    def search_and_filter_releases_task(self) -> Task:
        """Task to search for releases and filter to available matches."""
        return Task(
            config=self.tasks_config['search_and_filter_releases_task'], # type: ignore[index]
            context=[self.generate_suggestions_task()]
        )

    @task
    def create_suggested_folder_task(self) -> Task:
        """Task to create folder with all suggested releases."""
        return Task(
            config=self.tasks_config['create_suggested_folder_task'], # type: ignore[index]
            context=[self.search_and_filter_releases_task()]
        )

    @task
    def select_top_popular_task(self) -> Task:
        """Task to select top 10 most popular releases."""
        return Task(
            config=self.tasks_config['select_top_popular_task'], # type: ignore[index]
            context=[self.search_and_filter_releases_task()]
        )

    @task
    def create_popular_folder_task(self) -> Task:
        """Task to create folder with top 10 popular releases."""
        return Task(
            config=self.tasks_config['create_popular_folder_task'], # type: ignore[index]
            context=[self.select_top_popular_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Discogsworkflow crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        
        #logger.debug(f"🔍 DEBUG: Creating crew with {len(self.agents)} agents")
        #logger.debug(f"🔍 DEBUG: Agent types: {[type(agent).__name__ for agent in self.agents]}")
        #logger.debug(f"🔍 DEBUG: Creating crew with {len(self.tasks)} tasks")

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
