"""
Manufacturing Crew
Defines the crew with agents and tasks loaded from YAML config files
"""

import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM

# Import all tools
from tools.manufacturing_tools import (
    parse_production_order,
    generate_manufacturing_sequence,
    coordinate_robots,
    adapt_plan_for_disruption,
    track_production_progress,
    translate_to_motion_primitives,
    read_sensor_data,
    execute_motion,
    check_human_proximity,
    emergency_stop,
    inspect_product_quality,
    analyze_quality_trends,
    suggest_process_improvements,
    predict_maintenance_needs,
    detect_anomalies,
    generate_recovery_strategy,
    validate_safety_protocols,
    log_incident
)

# Configure Gemini LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")

llm = LLM(
    model="gemini/gemini-flash-lite-latest",
    api_key=GEMINI_API_KEY,
    temperature=0.7
)

class ManufacturingCrew():
    """Manufacturing Multi-Agent Crew"""
    
    def __init__(self):
        """Initialize crew with config files"""
        # Load YAML configs
        with open('config/agents.yaml', 'r') as f:
            self.agents_config = yaml.safe_load(f)
        
        with open('config/tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)
    
    # ========================
    # DEFINE AGENTS
    # ========================
    
    def planning_agent(self) -> Agent:
        config = self.agents_config['planning_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config['verbose'],
            allow_delegation=config['allow_delegation'],
            tools=[
                parse_production_order,
                generate_manufacturing_sequence,
                coordinate_robots,
                adapt_plan_for_disruption,
                track_production_progress
            ],
            llm=llm
        )
    
    def robot_control_agent(self) -> Agent:
        config = self.agents_config['robot_control_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config['verbose'],
            allow_delegation=config['allow_delegation'],
            tools=[
                translate_to_motion_primitives,
                read_sensor_data,
                execute_motion,
                check_human_proximity,
                emergency_stop
            ],
            llm=llm
        )
    
    def quality_agent(self) -> Agent:
        config = self.agents_config['quality_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config['verbose'],
            allow_delegation=config['allow_delegation'],
            tools=[
                inspect_product_quality,
                analyze_quality_trends,
                suggest_process_improvements,
                predict_maintenance_needs
            ],
            llm=llm
        )
    
    def exception_agent(self) -> Agent:
        config = self.agents_config['exception_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config['verbose'],
            allow_delegation=config['allow_delegation'],
            tools=[
                detect_anomalies,
                generate_recovery_strategy,
                validate_safety_protocols,
                log_incident
            ],
            llm=llm
        )
    
    # ========================
    # DEFINE TASKS
    # ========================
    
    def parse_and_plan_task(self) -> Task:
        config = self.tasks_config['parse_and_plan']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.planning_agent()
        )
    
    def execute_production_task(self) -> Task:
        config = self.tasks_config['execute_production']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.robot_control_agent(),
            context=[self.parse_and_plan_task()]
        )
    
    def monitor_quality_task(self) -> Task:
        config = self.tasks_config['monitor_quality']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.quality_agent(),
            context=[self.parse_and_plan_task(), self.execute_production_task()]
        )
    
    def handle_exceptions_task(self) -> Task:
        config = self.tasks_config['handle_exceptions']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.exception_agent(),
            context=[self.parse_and_plan_task(), self.execute_production_task()]
        )
    
    def generate_report_task(self) -> Task:
        config = self.tasks_config['generate_report']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.planning_agent(),
            context=[
                self.parse_and_plan_task(),
                self.execute_production_task(),
                self.monitor_quality_task(),
                self.handle_exceptions_task()
            ],
            output_file='manufacturing_report.md'
        )
    
    # ========================
    # CREATE CREW
    # ========================
    
    def crew(self) -> Crew:
        """Creates the Manufacturing Multi-Agent Crew"""
        return Crew(
            agents=[
                self.planning_agent(),
                self.robot_control_agent(),
                self.quality_agent(),
                self.exception_agent()
            ],
            tasks=[
                self.parse_and_plan_task(),
                self.execute_production_task(),
                self.monitor_quality_task(),
                self.handle_exceptions_task(),
                self.generate_report_task()
            ],
            process=Process.sequential,
            verbose=True
        )