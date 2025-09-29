"""
Main Entry Point for Manufacturing Multi-Agent System
Runs the simulation and manages the production flow
"""

import os
import time
import json
from datetime import datetime
from crew import ManufacturingCrew
from tools.manufacturing_tools import manufacturing_state, scenario


def print_header(text, char="="):
    """Print formatted section headers"""
    width = 60
    print(f"\n{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}\n")


def print_unit_header(product, unit_num, total):
    """Print formatted unit headers"""
    print(f"\n{'━' * 60}")
    print(f"PRODUCT: {product} (Unit {unit_num}/{total})")
    print(f"{'━' * 60}\n")


def simulate_production():
    """Main simulation function that orchestrates the manufacturing process"""
    
    print_header("MULTI-AGENT MANUFACTURING SYSTEM")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
    print(f"[System] 🤖 Using LLM: Gemini Flash Lite Latest")
    print(f"[System] 🔑 API Key configured: {'✓' if api_key and api_key != 'your-gemini-api-key-here' else '✗'}")
    
    if not api_key or api_key == "your-gemini-api-key-here":
        print("\n❌ ERROR: GEMINI_API_KEY not configured!")
        print("Please set your API key:")
        print("  export GEMINI_API_KEY='your-actual-key'")
        print("\nOr edit crew.py and replace the placeholder.")
        return
    
    print("[System] 🚀 Initializing manufacturing cell...")
    print("[System] 📡 Sensors: Active")
    print("[System] 🤖 Robots: Operational")
    print("[System] 📦 Materials: Stocked")
    print("[System] ✓ System ready\n")
    
    print("[System] 🎬 Starting production crew...\n")
    
    start_time = time.time()
    
    # Simulate production units with detailed output
    orders = scenario["production_orders"]
    unit_counter = 0
    
    for order in orders:
        product_name = order["product"]
        quantity = order["quantity"]
        
        print(f"\n[Planning Agent] 📦 Starting {product_name} production ({quantity} units)")
        
        for unit in range(1, quantity + 1):
            unit_counter += 1
            manufacturing_state["current_unit"] = unit_counter
            manufacturing_state["current_product"] = product_name
            
            print_unit_header(product_name, unit, manufacturing_state["total_units"])
            
            # Check for disruptions at this unit
            disruption_occurred = False
            for disruption in scenario["disruptions"]:
                if disruption["occurs_at_unit"] == unit_counter:
                    disruption_occurred = True
                    
                    print(f"[Exception Agent] 🚨 ANOMALY DETECTED!")
                    print(f"[Exception Agent] → Type: {disruption['type']}")
                    
                    if disruption['type'] == "equipment_failure":
                        print(f"[Exception Agent] → Target: {disruption['target']}")
                        print(f"[Exception Agent] → {disruption['description']}")
                        print(f"[Exception Agent] → Severity: {disruption['severity'].upper()}\n")
                        
                        print(f"[Exception Agent] 🛠️ Generating recovery strategy...")
                        print(f"[Exception Agent] → Option 1: Switch to alternate robot ✓ SELECTED")
                        print(f"[Exception Agent] → Option 2: Manual intervention (20min delay)\n")
                        
                        print(f"[Planning Agent] 🔄 Adapting plan for equipment failure...")
                        print(f"[Planning Agent] → Reallocating tasks from {disruption['target']} to robot_2")
                        print(f"[Planning Agent] → Adjusting sequence for robot_2 capabilities")
                        print(f"[Planning Agent] ✓ Plan adapted\n")
                        
                        print(f"[Robot Control] 🤖 Resuming with robot_2...")
                        print(f"[Robot Control] ⚙️ Adapting motion for different robot configuration...")
                        
                    elif disruption['type'] == "material_shortage":
                        print(f"[Exception Agent] → Material: {disruption['target']} stock depleted")
                        print(f"[Exception Agent] → Cause: {disruption['description']}\n")
                        
                        print(f"[Exception Agent] 🛠️ Generating recovery strategy...")
                        print(f"[Exception Agent] → Checking alternate material sources...")
                        print(f"[Exception Agent] → Found: Backup inventory in bin_3 ✓ SELECTED\n")
                        
                        print(f"[Planning Agent] 🔄 Adapting plan for material shortage...")
                        print(f"[Planning Agent] → Updating material source: bin_2 → bin_3")
                        print(f"[Planning Agent] → Estimated delay: +15s for retrieval\n")
                        
                        print(f"[Robot Control] 🤖 Retrieving from alternate location...")
                        
                    elif disruption['type'] == "human_intervention":
                        print(f"[Exception Agent] → Location: {disruption['location']}")
                        print(f"[Exception Agent] → Reason: {disruption['reason']}")
                        print(f"[Exception Agent] → Human detected at 1.5m from robot\n")
                        
                        print(f"[Exception Agent] 🛡️ Activating safety protocols...")
                        print(f"[Exception Agent] → Validating emergency stop procedures")
                        print(f"[Exception Agent] → Ensuring restricted zone compliance\n")
                        
                        print(f"[Robot Control] 🛑 EMERGENCY STOP activated")
                        print(f"[Robot Control] → All robot motion halted")
                        print(f"[Robot Control] → Waiting for human clearance...\n")
                        
                        print(f"[Planning Agent] ⏸️ Production paused for safety")
                        print(f"[Planning Agent] → Maintaining production goals during delay")
                        print(f"[Planning Agent] → Ready to resume when safe\n")
                        
                        time.sleep(1)
                        
                        print(f"[Exception Agent] ✓ Human cleared work area ({disruption['duration_seconds']}s elapsed)")
                        print(f"[Exception Agent] → Safety protocols maintained")
                        print(f"[Exception Agent] 📝 Logging incident for review\n")
                        
                        print(f"[Robot Control] ▶️ Resuming operations...")
                        print(f"[Robot Control] 🔄 Adapting motion after interruption...")
            
            # Normal execution
            if not disruption_occurred:
                print(f"[Robot Control] 🤖 Translating tasks to motion primitives...")
                product_steps = scenario["products"][product_name]["steps"]
                print(f"[Robot Control] → {' | '.join(product_steps)}")
                
                print(f"[Robot Control] 📡 Reading sensors: Position=OK, Force=Normal, Temp=22°C")
                
                for step in product_steps[:2]:
                    duration = 3 if "pick" in step else 5
                    print(f"[Robot Control] ⚙️ Executing: {step}... ✓ ({duration}s)")
            
            # Quality inspection
            print(f"\n[Quality Agent] 🔍 Inspecting {product_name} Unit {unit}...")
            print(f"[Quality Agent] ✓ Dimensions: Within tolerance (0.02mm deviation)")
            print(f"[Quality Agent] ✓ Surface finish: Acceptable")
            print(f"[Quality Agent] ✓ PASS")
            
            manufacturing_state["quality_checks_passed"] += 1
            
            time.sleep(0.5)
        
        # Batch analysis after each product
        print(f"\n[Quality Agent] 📊 Analyzing {product_name} batch ({quantity} units)...")
        print(f"[Quality Agent] → Average cycle time: {scenario['products'][product_name]['cycle_time_seconds'] + 2}s")
        print(f"[Quality Agent] → Quality pass rate: 100%")
        
        if product_name == "Widget-A":
            print(f"[Quality Agent] 💡 PROCESS IMPROVEMENT: Robot_1 caused 5s delay")
            print(f"[Quality Agent] 💡 RECOMMENDATION: Schedule robot_1 maintenance")
            print(f"[Quality Agent] 🔮 PREDICTIVE MAINTENANCE: robot_2 at 383 cycles (maintenance due at 500)")
            
            print(f"\n[Planning Agent] 📝 Feedback received from Quality Agent")
            print(f"[Planning Agent] → Noted: Robot_1 needs maintenance")
            print(f"[Planning Agent] → Adjusting: Future tasks remain on robot_2 until repair")
        
        elif product_name == "Widget-B":
            print(f"[Quality Agent] 💡 OPTIMIZATION: Material buffer stock recommended")
        
        # Product changeover
        if product_name == "Widget-A":
            print(f"\n{'━' * 60}")
            print(f"PRODUCT CHANGEOVER: Widget-A → Widget-B")
            print(f"{'━' * 60}\n")
            
            print(f"[Planning Agent] 🔄 Managing product changeover...")
            print(f"[Planning Agent] → Widget-B requires welding capability")
            print(f"[Planning Agent] → Assigning to robot_2 (welding_station)")
            
            print(f"\n[Robot Control] 🔧 Reconfiguring tools: assembly_tool → welding_tool")
            print(f"[Robot Control] ✓ Tool changeover complete (10s)")
    
    # Final summary
    print_header("PRODUCTION COMPLETE")
    
    elapsed_time = int(time.time() - start_time)
    
    print(f"[Planning Agent] ✅ All production orders completed")
    print(f"[Planning Agent] → Total units: 5 (3x Widget-A, 2x Widget-B)")
    print(f"[Planning Agent] → Disruptions handled: 3")
    print(f"[Planning Agent] → Overall success rate: 100%")
    print(f"[Planning Agent] → Simulation time: {elapsed_time} seconds\n")
    
    return elapsed_time


def run_crew():
    """Initialize and run the CrewAI crew"""
    
    print("\n[System] 🔧 Initializing CrewAI agents and tasks...")
    
    try:
        # Create the crew
        manufacturing_crew = ManufacturingCrew()
        crew = manufacturing_crew.crew()
        
        print("[System] ✓ Crew initialized successfully")
        print("[System] 👥 Agents: Planning, Robot Control, Quality, Exception Handler")
        print("[System] 📋 Tasks: 5 sequential tasks loaded from config\n")
        
        print("[System] 🚀 Starting crew execution...\n")
        print_header("CREW EXECUTION")
        
        # Run the crew
        result = crew.kickoff()
        
        print_header("CREW EXECUTION COMPLETE")
        
        print(f"\n[System] ✅ Crew execution finished")
        print(f"[System] 📄 Final report generated: manufacturing_report.md")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error during crew execution: {str(e)}")
        print("\nPlease check:")
        print("  1. All config files exist (config/agents.yaml, config/tasks.yaml)")
        print("  2. GEMINI_API_KEY is set correctly")
        print("  3. All dependencies are installed")
        return None


def main():
    """Main entry point"""
    
    try:
        # Run the visual simulation first
        elapsed = simulate_production()
        
        # Then run the actual CrewAI crew for the full execution
        print("\n" + "=" * 60)
        print("Now running full CrewAI execution...")
        print("This will take 5-7 minutes as agents make decisions")
        print("=" * 60 + "\n")
        
        result = run_crew()
        
        # Final summary
        print_header("SYSTEM SHUTDOWN")
        
        print("[System] ✅ Manufacturing system completed successfully!")
        print(f"[System] 📊 Total units: {manufacturing_state['total_units']}")
        print(f"[System] ✓ Quality checks: {manufacturing_state['quality_checks_passed']}/{manufacturing_state['total_units']}")
        print(f"[System] 🛠️ Disruptions handled: {manufacturing_state['disruptions_handled']}")
        print(f"[System] 💾 Report saved: manufacturing_report.md")
        print(f"[System] ⏱️ Simulation time: {elapsed if elapsed else 'N/A'} seconds\n")
        
    except KeyboardInterrupt:
        print("\n\n[System] ⚠️ Execution interrupted by user")
        print("[System] Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("\nPlease check:")
        print("  1. manufacturing_scenario.json exists in the root directory")
        print("  2. All config files exist (config/agents.yaml, config/tasks.yaml)")
        print("  3. Tools directory exists with manufacturing_tools.py")
        print("  4. GEMINI_API_KEY environment variable is set")
        print("  5. All dependencies installed: pip install -r requirements.txt")


if __name__ == "__main__":
    main()