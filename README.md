# Multi-Agent Manufacturing Orchestration System

A CrewAI-based multi-agent system using YAML configuration files that orchestrates a flexible manufacturing cell, capable of adapting to product variations, handling disruptions, and optimizing processes while maintaining quality standards and safety protocols.

## Project Structure

```
project/
├── config/
│   ├── agents.yaml          # Agent definitions (4 agents)
│   └── tasks.yaml           # Task definitions (5 tasks)
├── tools/
│   └── manufacturing_tools.py  # All 24 tools
├── crew.py                  # Crew definition with @CrewBase
├── main.py                  # Main entry point
├── manufacturing_scenario.json  # Simulation data
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## System Overview

This system demonstrates autonomous manufacturing coordination through 4 specialized AI agents:

1. **Planning & Coordination Agent** - Orchestrates production, coordinates robots, adapts plans
2. **Robot Control Agent** - Executes motions, manages sensors, ensures safety
3. **Quality & Optimization Agent** - Monitors quality, suggests improvements, predicts maintenance
4. **Exception Handling Agent** - Detects anomalies, generates recovery strategies, maintains safety

## Features

✅ **YAML Configuration** - Agents and tasks defined in YAML files  
✅ **Product Variation Handling** - Produces multiple product types without reprogramming  
✅ **Disruption Recovery** - Autonomously handles equipment failures, supply issues, human interventions  
✅ **Real-Time Quality Monitoring** - Continuous inspection and optimization  
✅ **Safety Protocols** - Emergency stops, human proximity detection  
✅ **Predictive Maintenance** - Forecasts equipment needs  
✅ **Dynamic Task Reallocation** - Adapts to changing conditions in real-time  

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- **Google Gemini API Key** (Get free key at: https://makersuite.google.com/app/apikey)

### Setup

1. **Clone or download the project files:**
   ```bash
   # Ensure you have these files:
   # - manufacturing_system.py
   # - manufacturing_scenario.json
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Gemini API Key:**
   
   **Option A: Environment Variable (Recommended)**
   ```bash
   # Linux/Mac
   export GEMINI_API_KEY="your-actual-gemini-api-key"
   
   # Windows (Command Prompt)
   set GEMINI_API_KEY=your-actual-gemini-api-key
   
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="your-actual-gemini-api-key"
   ```
   
   **Option B: Edit the Python file directly**
   - Open `manufacturing_system.py`
   - Find line: `GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")`
   - Replace `"your-gemini-api-key-here"` with your actual API key
   - Example: `GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB...")`

### Getting Your Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Use it in one of the configuration methods above

## Running the System

1. **Make sure both files are in the same directory:**
   - `manufacturing_system.py`
   - `manufacturing_scenario.json`

2. **Run the simulation:**
   ```bash
   python manufacturing_system.py
   ```

3. **Watch the terminal output** showing:
   - Agent collaboration in real-time
   - Production progress for 5 units (3x Widget-A, 2x Widget-B)
   - 3 disruption events and their recovery
   - Quality inspections and optimizations
   - Safety protocol enforcement

4. **Check the generated report:**
   - After completion, open `manufacturing_report.md`
   - Contains comprehensive production analysis

## Expected Output

### Terminal Output
The system will display detailed logs showing:
- Production order parsing
- Manufacturing sequence generation
- Robot coordination and execution
- Real-time sensor readings
- Disruption detection and recovery
- Quality inspections
- Process optimization suggestions
- Final production summary

### Generated Report
`manufacturing_report.md` includes:
- Production summary with metrics
- Agent performance breakdown
- Disruption handling details
- Collaboration mechanisms demonstrated
- Process improvement recommendations
- Complete achievement documentation

## Simulation Scenario

The system processes:
- **2 product types:** Widget-A (assembly) and Widget-B (welding)
- **5 total units:** 3x Widget-A, 2x Widget-B
- **3 disruptions:**
  1. Equipment failure (Robot_1) at Unit 2
  2. Material shortage at Unit 4
  3. Human intervention at Unit 5

## Project Structure

```
.
├── manufacturing_system.py       # Main system with agents, tools, and simulation
├── manufacturing_scenario.json   # Simulation data (products, equipment, disruptions)
└── manufacturing_report.md       # Generated after run (production report)
```

## Agent Capabilities

### Planning Agent Tools
- `parse_production_order` - Convert requirements to structured format
- `generate_manufacturing_sequence` - Create step-by-step plans
- `coordinate_robots` - Assign tasks to robots
- `adapt_plan_for_disruption` - Modify plans during issues
- `track_production_progress` - Monitor completion

### Robot Control Tools
- `translate_to_motion_primitives` - High-level to low-level commands
- `read_sensor_data` - Capture real-time sensor readings
- `execute_motion` - Perform robot movements
- `check_human_proximity` - Safety monitoring
- `emergency_stop` - Immediate halt for safety

### Quality Agent Tools
- `inspect_product_quality` - Quality checks against specs
- `analyze_quality_trends` - Pattern identification
- `suggest_process_improvements` - Optimization recommendations
- `predict_maintenance_needs` - Equipment wear forecasting

### Exception Agent Tools
- `detect_anomalies` - Identify deviations
- `generate_recovery_strategy` - Create alternative plans
- `validate_safety_protocols` - Ensure compliance
- `log_incident` - Record for learning

## Key Concepts Demonstrated

1. **Shared Manufacturing Context** - All agents access common scenario data
2. **Real-Time Sensor Integration** - Continuous monitoring and feedback
3. **Continuous Feedback Loops** - Quality insights drive planning adjustments
4. **Dynamic Task Reallocation** - Autonomous resource reassignment during disruptions

## Troubleshooting

**ImportError: No module named 'crewai'**
```bash
pip install --upgrade crewai crewai-tools langchain-google-genai
```

**API Key Error: "GEMINI_API_KEY not configured"**
- Make sure you've set the API key using one of the methods above
- Verify the key is correct (starts with "AIza...")
- Try restarting your terminal after setting environment variable

**Error: "API key not valid"**
- Get a new key from https://makersuite.google.com/app/apikey
- Make sure you're using Gemini API key, not other Google API keys
- Check if API key has proper permissions enabled

**FileNotFoundError: manufacturing_scenario.json**
- Ensure both .py and .json files are in same directory
- Check file names match exactly

**Slow execution**
- Normal behavior - agents are making decisions using Gemini
- Typical runtime: 3-7 minutes (Gemini is fast!)
- First run may be slower as it loads models

## Customization

To modify the simulation, edit `manufacturing_scenario.json`:
- Add more products in `products` section
- Change disruption timing in `disruptions` array
- Adjust equipment capabilities in `equipment` section
- Modify quality tolerances in `quality_standards`

## License

Educational project for classroom demonstration.

## Author

Created for demonstrating multi-agent manufacturing orchestration using CrewAI framework.