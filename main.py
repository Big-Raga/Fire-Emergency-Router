import pandas as pd
import heapq
from datetime import datetime, timedelta, time 


def create_dict():
    """
    Load the specified sheet into a DataFrame, then create a dictionary with each pair of coordinates and times.
    Returns:
            A dictionary with coordinates as keys and times as values for the sites and thier times
    """
    
    #load the specific sheet into a DataFrame
    df_emergency_sites = pd.read_excel(file_path, sheet_name=sheetname1)

    #load the specific sheet into a DataFrame
    df_emergency_sites = pd.read_excel(file_path, sheet_name= sheetname1)

    #create a dictionary
    emergency_dict = {}

    #for loop to store each pair
    for index, row in df_emergency_sites.iterrows():
        #extracting the cooridnate and time
        coordinate = row['Coordinates']
        time = row['Time']
       
        #create key and value pairs
        emergency_dict[coordinate] = time
 
    return emergency_dict

#GLOBAL VARIABLES
#information of the Excel file
file_path = "D:/zzPersonal stuff/Nust/3rd semester/AI/W11/Lab 9/data.xlsx"
sheetname1 = "Emergency Site" 
sheetname2 = "road_traffic_data"

#fire station coordinates
f1 = '(1, 1)'
f2 = '(10, 10)' 

#dictionary for coordinates and times
emergency_dict = create_dict()


def get_RouteInfo(coordinate, time):
    """
    Load the specified sheet into a DataFrame, filter for the given coordinate and time(open routes only),
    and return the filtered DataFrame.
    Returns:
            A DataFrame with the filtered road traffic data
    """

    #get the DataFrame
    df = pd.read_excel(file_path, sheet_name=sheetname2)
    
    #convert the time into the desired fomrat
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

    #convert the input time to the correct datetime type
    if isinstance(time, str):
        time = pd.to_datetime(time, format='%H:%M:%S').time()

    #filter for rows where the coordinate appears in `Road Segment Start`
    df_start = df[(df['Road Segment Start'] == coordinate) & (df['Time'] == time) & (df['Status'] == 'Open')]

    #filter for rows where the coordinate appears in `Road Segment End`
    df_end = df[(df['Road Segment End'] == coordinate) & (df['Time'] == time) & (df['Status'] == 'Open')]

    #switch columns for the second dataframe
    df_end = df_end.rename(columns={'Road Segment Start': 'Road Segment End', 'Road Segment End': 'Road Segment Start'})

    #combine the two DataFrames
    df_combined = pd.concat([df_start, df_end], ignore_index=True)

    return df_combined



def ucs(firestation, site, time):
    """
    Finds the shortest path from a fire station to an emergency site using Uniform Cost Search.
    The node with the smallest time will be given preference

    Args:
        firestation: Starting point.
        site: Target point.
        time : Current time of emergency.

    Returns:
        tuple: (cost, path) where:
            - cost : Minimum travel cost (time) to the target.
            - path : Shortest path as a list of nodes, or an empty list if no path exists.

    This function uses a priority queue to explore nodes in order of cost, updating paths only when 
    a cheaper route is found. The path is reconstructed using a parent mapping.
    """

    p_queue = [(0, firestation)]    #priority queue with the fire station as the initial state
    parents = {}                    #to reconstruct the path followed
    visited = set()                 #nodes that are fully processed
    cost_map = {}                   #tracks the minimum cost to each node

    #while there are nodes in the priority queue
    while p_queue:
        #get the state with the smallest cost
        cost, state = heapq.heappop(p_queue)

        #if this node is already fully processed, skip it
        if state in visited:
            continue

        #mark the node as fully processed
        visited.add(state)

        #if this is the goal state, backtrack to get the path
        if state == site:
            #reconstruct the path
            path = []
            while state is not None:
                path.append(state)
                state = parents.get(state)

            path.reverse()
            
            #return the cost and path
            return cost, path   

        #get all open neighbors of the state
        current_df = get_RouteInfo(state, time)
        

        #expand neighbors
        for _, row in current_df.iterrows():
            neighbor = row['Road Segment End']
            edge_cost = 1 / row['Current Speed (km/h)']  #caculate the time 
            new_cost = cost + edge_cost                 

            #if the neighbor is not visited or a cheaper path is found, update
            if neighbor not in visited and (neighbor not in cost_map or new_cost < cost_map[neighbor]):
                cost_map[neighbor] = new_cost                   #update the cost map
                heapq.heappush(p_queue, (new_cost, neighbor))   #push the neighbor into the queue
                
                #update parent if the new path is cheaper
                if neighbor not in parents or new_cost < cost_map.get(neighbor, float('inf')):
                    #update the parent of the neighbor
                    parents[neighbor] = state  

    #if no path is found
    return float('inf'), []


def find_min_path_between_firestations_with_time(firestation1, firestation2, site,):
    """
    Finds the shortest path and cost from two fire stations to the given site,
    incrementing time if no path is available at the current time.

    Args:
    firestation1 : The starting coordinate of the first fire station.
    firestation2 : The starting coordinate of the second fire station.
    site : The target emergency site.

    Returns:
    tuple: A tuple containing the shortest cost, path, and the final time used.
    """
    #get the initial time of the emergency
    time = emergency_dict[site]
    
    #a counter
    counter = 0

    #until we find a path
    while counter < 24:
        print(f"Attempting to find a path with time: {time}")

        #run UCS for both fire stations
        cost1, path1 = ucs(firestation1, site,time)
        cost2, path2 = ucs(firestation2, site, time)

        #check if at least one valid path exists
        if path1 or path2:
            #compare and return the minimum path
            if cost1 < cost2:
                return cost1, path1, time
            else:
                return cost2, path2, time
        
        #increment the time by 1 hour if no valid paths are found
        print(f"No valid paths found at time: {time}. Incrementing time by 1 hour.")
        time = increment_time_by_one_hour(time)

        #increment counter
        counter += 1


def increment_time_by_one_hour(time_input):
    """
    Increments a given time by one hour.

    Args:
    time_input: The time to increment.

    Returns:
    str: The incremented time as a string in the format "HH:MM:SS".
    """

    #if the input is a datetime.time object, convert it to a string
    if isinstance(time_input, time):
        time_str = time_input.strftime("%H:%M:%S")
    else:
        time_str = time_input

    #convert the string to a datetime object
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    
    #increment by 1 hour
    incremented_time = time_obj + timedelta(hours=1)
    
    #convert back to string format
    return incremented_time.strftime("%H:%M:%S")



#Main FUNCTION
for site in emergency_dict:
    print(f"EMERGENCY AT SITE: {site}  TIME: {emergency_dict[site]}") 

    #find the minimum path with time adjustment
    min_cost, min_path, final_time = find_min_path_between_firestations_with_time(f1, f2, site)

    #print the results
    print(f"Minimum time taken: {min_cost * 60} minutes ")
    print(f"Firestations: {min_path[0]}")
    print(f"Path: {min_path}")
    print(f"Final Time Used: {final_time}")
    print("-------------------------\n\n")
