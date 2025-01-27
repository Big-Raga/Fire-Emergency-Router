# Fire Emergency Routing

This project implements an AI-based emergency response system designed to determine the shortest path from fire stations to emergency sites using Uniform Cost Search (UCS). The program utilizes road traffic data and time constraints to calculate the optimal route for fire station vehicles.

---

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [File Structure](#file-structure)
5. [How It Works](#how-it-works)
6. [Usage](#usage)
7. [Examples](#examples)
8. [Known Issues](#known-issues)

---

## Overview
This system is designed to:  
- Load emergency site coordinates and their corresponding times from an Excel file.
- Use road traffic data to find open routes between locations.
- Compute the shortest path using Uniform Cost Search (UCS), prioritizing roads with the smallest travel time.
- Adjust the emergency time incrementally if no valid path is initially found.

---

## Requirements
The following dependencies are required:

1. Python 3.8 or higher
2. Libraries:
   - pandas
   - heapq (built-in)
   - datetime (built-in)
   - openpyxl

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/fire-emergency-routing.git
   ```

2. Install the required Python libraries:
   ```bash
   pip install pandas openpyxl
   ```

3. Place the `data.xlsx` file in the appropriate directory as specified in the `file_path` variable.

---

## File Structure
The key files are organized as follows:

- **main.py**: The core script for the emergency routing logic.
- **data.xlsx**: The input data file containing emergency site information and road traffic data.
- **README.md**: Documentation for the project.

---

## How It Works
1. **Emergency Site Data**: The script reads a list of emergency site coordinates and times from an Excel file.
2. **Road Traffic Data**: The script reads road traffic data to find valid routes between nodes (coordinates).
3. **UCS Algorithm**:
   - Implements Uniform Cost Search to explore paths based on the travel time.
   - Prioritizes routes with lower costs (time).
   - Tracks visited nodes and reconstructs the optimal path using parent mapping.
4. **Time Adjustment**:
   - If no path is available at the initial emergency time, the system increments the time by 1 hour (up to 24 hours).
5. **Results**:
   - Outputs the shortest time, the path taken, and the final time used.

---

## Usage
1. Update the global variables at the top of the script:
   - `file_path`: Path to the `data.xlsx` file.
   - `sheetname1`: Name of the sheet containing emergency site data.
   - `sheetname2`: Name of the sheet containing road traffic data.

2. Define the fire stations and emergency sites.
   ```python
   f1 = '(1, 1)'
   f2 = '(10, 10)'
   ```

3. Run the script:
   ```bash
   python main.py
   ```

4. The output will display the shortest path, travel time, and other relevant details for each emergency site.

---

## Examples
Example output for an emergency site:
```text
EMERGENCY AT SITE: (5, 5)  TIME: 12:00:00
Attempting to find a path with time: 12:00:00
Minimum time taken: 30.0 minutes
Firestations: (1, 1)
Path: ['(1, 1)', '(3, 3)', '(5, 5)']
Final Time Used: 12:00:00
-------------------------
```

---

## Known Issues
- **No Path Found**: If no valid paths are available within 24 hours, the script will not provide a result for that site.
- **Edge Cost Calculation**: The edge cost is calculated using `1 / Current Speed (km/h)`, which might result in incorrect times for very low speeds. Additional validation could improve accuracy.

