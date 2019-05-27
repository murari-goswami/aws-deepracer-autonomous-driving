def reward_function(params):
    
    import math

    reward_maximum = 1e5
    reward_minimum = -1e5

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering_angle = params['steering_angle']
    steps = params['steps']
    heading = params['heading']
    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']
    speed = params['speed']  

    # Calculated variables
    central_lane = track_width * .25
    middle_of_track = track_width / 2
    SPEED_THRESHOLD = 1.0
    
    if not all_wheels_on_track:
        reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        reward = 0.5
    else:
        reward = 1.0
    
    steering = abs(params['steering_angle']) # We don't care whether it is left or righ
    reward = 1.0
    
    STEERING_THRESHOLD = 20.0
    if steering > STEERING_THRESHOLD:
	    reward *= 0.8
    
    # Read input variable
    steps = params['steps']
    progress = params['progress']
	
	# Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = 300

	# Initialize the reward with typical value 
    reward = 1.0

	# Give additional reward if the car pass every 100 steps faster than expected 
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) :
        reward += 10.0
    
	# Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

	# Initialize the reward with typical value 
    reward = 1.0

	# Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

	# Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
	# Convert to degree
    track_direction = math.degrees(track_direction)

	# Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)

	# Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5


    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    return float(reward)