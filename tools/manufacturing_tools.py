"""
Manufacturing Tools for Multi-Agent System
Contains all tools used by the 4 agents
"""

import json
import random
from datetime import datetime
from crewai.tools import tool

# Load scenario data
with open('manufacturing_scenario.json', 'r') as f:
    scenario = json.load(f)

# Global state for simulation
manufacturing_state = {
    "current_unit": 0,
    "total_units": 0,
    "current_product": None,
    "disruptions_handled": 0,
    "quality_checks_passed": 0,
    "cycle_times": [],
    "incidents": [],
    "agent_actions": [],
    "sensor_readings": []
}

# ========================
# PLANNING AGENT TOOLS
# ========================

@tool("Parse Production Order")
def parse_production_order(order_text: str) -> str:
    """
    Converts natural language or JSON production requirements into structured format.
    Returns parsed order details including product type, quantity, and description.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Planning",
        "action": "parse_production_order",
        "timestamp": datetime.now().isoformat()
    })
    
    orders = scenario["production_orders"]
    result = "📋 Parsed Production Orders:\n"
    total = 0
    for order in orders:
        result += f"  → {order['quantity']}x {order['product']} ({order['description']})\n"
        total += order['quantity']
    
    manufacturing_state["total_units"] = total
    return result + f"\nTotal units to produce: {total}"

@tool("Generate Manufacturing Sequence")
def generate_manufacturing_sequence(product_name: str) -> str:
    """
    Creates step-by-step manufacturing plan for a given product.
    Returns sequence of operations with timing estimates.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Planning",
        "action": "generate_sequence",
        "product": product_name,
        "timestamp": datetime.now().isoformat()
    })
    
    if product_name not in scenario["products"]:
        return f"❌ Product {product_name} not found in catalog"
    
    product = scenario["products"][product_name]
    steps = " → ".join(product["steps"])
    
    result = f"✓ Manufacturing sequence for {product_name}:\n"
    result += f"  Steps: {steps}\n"
    result += f"  Estimated cycle time: {product['cycle_time_seconds']}s\n"
    result += f"  Required tools: {', '.join(product['required_tools'])}"
    
    return result

@tool("Coordinate Robots")
def coordinate_robots(product_name: str, unit_number: int) -> str:
    """
    Assigns manufacturing tasks to appropriate robots based on their capabilities.
    Returns robot assignment and task allocation.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Planning",
        "action": "coordinate_robots",
        "product": product_name,
        "unit": unit_number,
        "timestamp": datetime.now().isoformat()
    })
    
    product = scenario["products"][product_name]
    equipment = scenario["equipment"]
    
    # Check for disruptions at this unit
    for disruption in scenario["disruptions"]:
        if disruption["occurs_at_unit"] == unit_number and disruption["type"] == "equipment_failure":
            robot = disruption["target"]
            if robot in equipment:
                equipment[robot]["status"] = "failed"
    
    # Assign based on capabilities and status
    assigned_robot = None
    for robot_name, robot_info in equipment.items():
        if "robot" in robot_name and robot_info["status"] == "operational":
            required = set(step.split("_")[0] for step in product["steps"])
            if required.issubset(set(robot_info["capabilities"])):
                assigned_robot = robot_name
                break
    
    if not assigned_robot:
        for robot_name, robot_info in equipment.items():
            if "robot" in robot_name and robot_info["status"] == "operational":
                assigned_robot = robot_name
                break
    
    if assigned_robot:
        result = f"🤝 Robot coordination for {product_name} Unit {unit_number}:\n"
        result += f"  → Assigned: {assigned_robot} at {equipment[assigned_robot]['station']}\n"
        result += f"  → Capabilities: {', '.join(equipment[assigned_robot]['capabilities'])}"
        return result
    else:
        return "❌ No operational robots available"

@tool("Adapt Plan for Disruption")
def adapt_plan_for_disruption(disruption_type: str, target: str, unit_number: int) -> str:
    """
    Modifies manufacturing plan when disruptions occur.
    Returns adapted plan with alternative resource allocation.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Planning",
        "action": "adapt_plan",
        "disruption": disruption_type,
        "target": target,
        "timestamp": datetime.now().isoformat()
    })
    manufacturing_state["disruptions_handled"] += 1
    
    result = f"🔄 Adapting plan for {disruption_type}:\n"
    
    if disruption_type == "equipment_failure":
        equipment = scenario["equipment"]
        alternate = None
        for robot_name, robot_info in equipment.items():
            if "robot" in robot_name and robot_name != target and robot_info["status"] == "operational":
                alternate = robot_name
                break
        
        if alternate:
            result += f"  → Reallocating tasks from {target} to {alternate}\n"
            result += f"  → Adjusting sequence for {alternate} capabilities\n"
            result += "  → Estimated delay: +5s per unit"
        else:
            result += "  → No alternate robot available. Requesting maintenance."
    
    elif disruption_type == "material_shortage":
        result += f"  → Material {target} depleted\n"
        result += "  → Switching to backup inventory (bin_3)\n"
        result += "  → Estimated delay: +15s for retrieval"
    
    elif disruption_type == "human_intervention":
        result += f"  → Human detected at {target}\n"
        result += "  → Pausing production for safety\n"
        result += "  → Will resume after clearance"
    
    return result

@tool("Track Production Progress")
def track_production_progress() -> str:
    """
    Monitors completion toward production goals.
    Returns current progress metrics and completion percentage.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Planning",
        "action": "track_progress",
        "timestamp": datetime.now().isoformat()
    })
    
    current = manufacturing_state["current_unit"]
    total = manufacturing_state["total_units"]
    percentage = (current / total * 100) if total > 0 else 0
    
    result = f"📊 Production Progress:\n"
    result += f"  → Units completed: {current}/{total} ({percentage:.0f}%)\n"
    result += f"  → Disruptions handled: {manufacturing_state['disruptions_handled']}\n"
    result += f"  → Quality checks passed: {manufacturing_state['quality_checks_passed']}"
    
    return result

# ========================
# ROBOT CONTROL AGENT TOOLS
# ========================

@tool("Translate to Motion Primitives")
def translate_to_motion_primitives(task: str, robot: str) -> str:
    """
    Converts high-level manufacturing tasks into low-level robot motion commands.
    Returns sequence of motion primitives for execution.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Robot Control",
        "action": "translate_motion",
        "task": task,
        "robot": robot,
        "timestamp": datetime.now().isoformat()
    })
    
    motion_map = {
        "pick_component": ["move_to_bin", "open_gripper", "approach", "close_gripper", "lift"],
        "assemble": ["move_to_assembly", "position", "apply_force", "verify_fit"],
        "weld": ["move_to_weld", "position", "ignite_torch", "weld_seam", "cool_down"],
        "quality_check": ["move_to_inspection", "scan", "measure", "validate"],
        "place_finished": ["move_to_output", "position", "open_gripper", "retract"]
    }
    
    primitives = motion_map.get(task, ["move", "execute", "return"])
    
    result = f"🤖 Motion primitives for '{task}' on {robot}:\n"
    result += f"  → {' | '.join(primitives)}"
    
    return result

@tool("Read Sensor Data")
def read_sensor_data(sensor_type: str = "all") -> str:
    """
    Retrieves real-time data from manufacturing sensors.
    Returns current sensor readings including position, force, temperature.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Robot Control",
        "action": "read_sensors",
        "sensor": sensor_type,
        "timestamp": datetime.now().isoformat()
    })
    
    sensors = scenario["sensors"]
    
    reading = {
        "timestamp": datetime.now().isoformat(),
        "position": f"{random.uniform(0, 100):.2f}mm",
        "force": f"{random.uniform(20, 50):.1f}N",
        "temperature": f"{random.uniform(20, 25):.1f}°C"
    }
    manufacturing_state["sensor_readings"].append(reading)
    
    result = "📡 Sensor readings:\n"
    result += f"  → Position: {reading['position']} (accuracy: {sensors['position_sensor']['accuracy']})\n"
    result += f"  → Force: {reading['force']} (threshold: {sensors['force_sensor']['threshold']}N)\n"
    result += f"  → Temperature: {reading['temperature']}"
    
    return result

@tool("Execute Motion")
def execute_motion(step: str, robot: str, duration: int) -> str:
    """
    Performs robot movement with real-time sensor feedback.
    Returns execution status and time taken.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Robot Control",
        "action": "execute_motion",
        "step": step,
        "robot": robot,
        "timestamp": datetime.now().isoformat()
    })
    
    actual_duration = duration + random.randint(-1, 2)
    
    result = f"⚙️ Executing: {step}...\n"
    result += f"  → Robot: {robot}\n"
    result += f"  → Duration: {actual_duration}s\n"
    result += f"  → Status: ✓ Complete"
    
    manufacturing_state["cycle_times"].append(actual_duration)
    
    return result

@tool("Check Human Proximity")
def check_human_proximity(location: str) -> str:
    """
    Monitors for human presence near robots to ensure safe interaction.
    Returns proximity status and safety recommendations.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Robot Control",
        "action": "check_proximity",
        "location": location,
        "timestamp": datetime.now().isoformat()
    })
    
    for disruption in scenario["disruptions"]:
        if disruption["type"] == "human_intervention" and disruption["location"] == location:
            if disruption["occurs_at_unit"] == manufacturing_state["current_unit"]:
                result = f"🚨 Human detected at {location}!\n"
                result += f"  → Distance: 1.5m (safe threshold: {scenario['safety_protocols']['human_detection_distance']}m)\n"
                result += "  → Recommendation: EMERGENCY STOP required"
                return result
    
    result = f"✓ Human proximity check: {location}\n"
    result += f"  → Status: Clear (safe distance maintained)"
    
    return result

@tool("Emergency Stop")
def emergency_stop(reason: str) -> str:
    """
    Immediately halts all robot motion for safety.
    Returns stop confirmation and safety status.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Robot Control",
        "action": "emergency_stop",
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    })
    
    stop_time = scenario["safety_protocols"]["emergency_stop_time"]
    
    result = f"🛑 EMERGENCY STOP ACTIVATED\n"
    result += f"  → Reason: {reason}\n"
    result += f"  → All robot motion halted\n"
    result += f"  → Stop time: {stop_time}s\n"
    result += "  → Waiting for safety clearance..."
    
    return result

# ========================
# QUALITY AGENT TOOLS
# ========================

@tool("Inspect Product Quality")
def inspect_product_quality(product: str, unit: int) -> str:
    """
    Performs quality inspection on manufactured product.
    Returns inspection results with pass/fail status.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Quality",
        "action": "inspect_quality",
        "product": product,
        "unit": unit,
        "timestamp": datetime.now().isoformat()
    })
    
    product_spec = scenario["products"][product]
    tolerance = product_spec["quality_tolerance"]
    
    deviation = random.uniform(0, tolerance * 0.8)
    
    result = f"🔍 Inspecting {product} Unit {unit}:\n"
    result += f"  → Dimensional check: ✓ Within tolerance ({deviation:.3f}mm deviation)\n"
    result += f"  → Surface finish: ✓ {scenario['quality_standards']['surface_finish']}\n"
    result += f"  → Inspection points: {scenario['quality_standards']['inspection_points']}/3 passed\n"
    result += "  → Status: ✓ PASS"
    
    manufacturing_state["quality_checks_passed"] += 1
    
    return result

@tool("Analyze Quality Trends")
def analyze_quality_trends(product: str, batch_size: int) -> str:
    """
    Analyzes quality patterns across multiple production runs.
    Returns trend analysis and identifies potential issues.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Quality",
        "action": "analyze_trends",
        "product": product,
        "timestamp": datetime.now().isoformat()
    })
    
    if len(manufacturing_state["cycle_times"]) >= batch_size:
        recent_times = manufacturing_state["cycle_times"][-batch_size:]
        avg_time = sum(recent_times) / len(recent_times)
        target_time = scenario["products"][product]["cycle_time_seconds"]
        
        result = f"📊 Quality trend analysis for {product} batch ({batch_size} units):\n"
        result += f"  → Average cycle time: {avg_time:.0f}s (target: {target_time}s)\n"
        result += f"  → Quality pass rate: {manufacturing_state['quality_checks_passed']}/{batch_size} (100%)\n"
        
        if avg_time > target_time:
            result += f"  → ⚠️ Cycle time exceeded target by {avg_time - target_time:.0f}s"
        else:
            result += "  → ✓ Performance within expectations"
    else:
        result = f"Insufficient data for trend analysis (need {batch_size} units)"
    
    return result

@tool("Suggest Process Improvements")
def suggest_process_improvements(issue: str) -> str:
    """
    Recommends optimizations based on production data analysis.
    Returns actionable improvement suggestions.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Quality",
        "action": "suggest_improvements",
        "issue": issue,
        "timestamp": datetime.now().isoformat()
    })
    
    result = f"💡 Process improvement recommendations:\n"
    
    if "robot_1" in issue.lower() or "failure" in issue.lower():
        result += "  → Robot_1: Schedule preventive maintenance for servo motor\n"
        result += "  → Impact: Reduce cycle time variance by ~5s\n"
        result += "  → Priority: HIGH"
    elif "material" in issue.lower():
        result += "  → Inventory: Increase material buffer stock for component_B\n"
        result += "  → Impact: Prevent supply chain delays\n"
        result += "  → Priority: MEDIUM"
    elif "cycle" in issue.lower():
        result += "  → Motion optimization: Review robot path planning\n"
        result += "  → Impact: Potential 10% cycle time reduction\n"
        result += "  → Priority: MEDIUM"
    else:
        result += "  → Continue monitoring production metrics\n"
        result += "  → No immediate action required"
    
    return result

@tool("Predict Maintenance Needs")
def predict_maintenance_needs(robot: str) -> str:
    """
    Forecasts equipment maintenance requirements based on usage patterns.
    Returns maintenance predictions and recommended timing.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Quality",
        "action": "predict_maintenance",
        "robot": robot,
        "timestamp": datetime.now().isoformat()
    })
    
    equipment = scenario["equipment"]
    if robot in equipment:
        cycles = equipment[robot]["cycles_completed"]
        maintenance_threshold = 500
        remaining = maintenance_threshold - cycles
        
        result = f"🔮 Predictive maintenance for {robot}:\n"
        result += f"  → Current cycles: {cycles}\n"
        result += f"  → Maintenance threshold: {maintenance_threshold}\n"
        result += f"  → Remaining cycles: {remaining}\n"
        
        if remaining < 50:
            result += "  → ⚠️ URGENT: Schedule maintenance within 50 cycles"
        elif remaining < 150:
            result += "  → ⚡ Schedule maintenance soon (within 150 cycles)"
        else:
            result += "  → ✓ Equipment healthy, monitor regularly"
    else:
        result = f"❌ Robot {robot} not found in equipment database"
    
    return result

# ========================
# EXCEPTION HANDLING AGENT TOOLS
# ========================

@tool("Detect Anomalies")
def detect_anomalies(unit_number: int) -> str:
    """
    Identifies deviations from normal manufacturing operations.
    Returns anomaly details if detected, otherwise confirms normal operation.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Exception Handler",
        "action": "detect_anomaly",
        "unit": unit_number,
        "timestamp": datetime.now().isoformat()
    })
    
    for disruption in scenario["disruptions"]:
        if disruption["occurs_at_unit"] == unit_number:
            incident = {
                "type": disruption["type"],
                "unit": unit_number,
                "description": disruption.get("description", "Unknown"),
                "timestamp": datetime.now().isoformat()
            }
            manufacturing_state["incidents"].append(incident)
            
            result = f"🚨 ANOMALY DETECTED!\n"
            result += f"  → Type: {disruption['type']}\n"
            result += f"  → Unit: {unit_number}\n"
            
            if disruption['type'] == "equipment_failure":
                result += f"  → Target: {disruption['target']}\n"
                result += f"  → Description: {disruption['description']}\n"
                result += f"  → Severity: {disruption['severity'].upper()}"
            elif disruption['type'] == "material_shortage":
                result += f"  → Material: {disruption['target']}\n"
                result += f"  → Cause: {disruption['description']}"
            elif disruption['type'] == "human_intervention":
                result += f"  → Location: {disruption['location']}\n"
                result += f"  → Reason: {disruption['reason']}\n"
                result += f"  → Duration: {disruption['duration_seconds']}s"
            
            return result
    
    return f"✓ No anomalies detected for Unit {unit_number}"

@tool("Generate Recovery Strategy")
def generate_recovery_strategy(disruption_type: str, target: str) -> str:
    """
    Creates alternative plans to recover from disruptions.
    Returns recovery options with estimated impact.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Exception Handler",
        "action": "generate_recovery",
        "disruption": disruption_type,
        "timestamp": datetime.now().isoformat()
    })
    
    result = f"🛠️ Generating recovery strategy for {disruption_type}:\n"
    
    if disruption_type == "equipment_failure":
        result += "  → Option 1: Switch to alternate robot ✓ SELECTED\n"
        result += "  → Option 2: Manual intervention (20min delay)\n"
        result += "  → Recommendation: Reallocate tasks to operational equipment\n"
        result += "  → Estimated recovery time: 5 seconds"
    
    elif disruption_type == "material_shortage":
        result += "  → Checking alternate material sources...\n"
        result += "  → Found: Backup inventory in bin_3 ✓ SELECTED\n"
        result += "  → Recommendation: Use backup materials\n"
        result += "  → Estimated recovery time: 15 seconds"
    
    elif disruption_type == "human_intervention":
        result += "  → Activating safety protocols...\n"
        result += "  → Action: Emergency stop and wait for clearance ✓ SELECTED\n"
        result += "  → Recommendation: Pause all robot motion\n"
        result += "  → Estimated recovery time: 20 seconds"
    
    return result

@tool("Validate Safety Protocols")
def validate_safety_protocols(scenario_name: str) -> str:
    """
    Ensures all safety rules are maintained during operations.
    Returns safety validation status and any violations.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Exception Handler",
        "action": "validate_safety",
        "scenario": scenario_name,
        "timestamp": datetime.now().isoformat()
    })
    
    protocols = scenario["safety_protocols"]
    
    result = f"🛡️ Safety protocol validation: {scenario_name}\n"
    result += f"  → Human detection distance: {protocols['human_detection_distance']}m ✓\n"
    result += f"  → Emergency stop time: {protocols['emergency_stop_time']}s ✓\n"
    result += f"  → Restricted zones: {', '.join(protocols['restricted_zones'])} ✓\n"
    result += "  → Status: All safety protocols maintained"
    
    return result

@tool("Log Incident")
def log_incident(incident_type: str, details: str) -> str:
    """
    Records exception events for analysis and learning.
    Returns confirmation of logged incident.
    """
    manufacturing_state["agent_actions"].append({
        "agent": "Exception Handler",
        "action": "log_incident",
        "incident": incident_type,
        "timestamp": datetime.now().isoformat()
    })
    
    log_entry = {
        "type": incident_type,
        "details": details,
        "timestamp": datetime.now().isoformat(),
        "resolved": True
    }
    manufacturing_state["incidents"].append(log_entry)
    
    result = f"📝 Incident logged:\n"
    result += f"  → Type: {incident_type}\n"
    result += f"  → Details: {details}\n"
    result += f"  → Timestamp: {log_entry['timestamp']}\n"
    result += "  → Status: Recorded for analysis"
    
    return result