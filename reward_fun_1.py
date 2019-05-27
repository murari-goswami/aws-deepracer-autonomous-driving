def reward_function(params):
    import math
    from statistics import mean

    on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    car_orientation = params['heading']
    progress = params['progress']
    steps = params['steps']
    speed = params['speed']
    steering = abs(params['steering_angle'])
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoint = params['closest_waypoints'][0]
    
    CENTER_LANE = track_width * .25
    HALF_TRACK = track_width / 2
    throttle = (speed * 125)/100

    ABS_STEERING_THRESHOLD = .85

    ####################
    # Locations on track
    ####################

    # Set Base Reward
    if not on_track: # Fail them if off Track
        reward = -1e5
        return reward
    elif progress == 1:
        reward = 1e5
        return reward
    else:        # we want the vehicle to continue making progress
        reward = 1e5 * progress

    # If outside track center than penalize
    if distance_from_center > 0.0 and distance_from_center > CENTER_LANE:
        reward *= 1 - (distance_from_center / HALF_TRACK)

    ##########
    # Steering
    ##########

    # Add penalty for wrong direction
    next_waypoint_yaw = waypoints[min(closest_waypoint+1, len(waypoints)-1)][-1]
    if abs(car_orientation - next_waypoint_yaw) >= math.radians(10):
        reward *= 1 - (abs(car_orientation - next_waypoint_yaw) / 180)
    elif abs(car_orientation - next_waypoint_yaw) < math.radians(10) and abs(steering) > ABS_STEERING_THRESHOLD:    # penalize if stearing to much
        reward *= ABS_STEERING_THRESHOLD / abs(steering)
    else:
        reward *= 1 + (10 - (abs(car_orientation - next_waypoint_yaw) / 10))

    # Add penalty if throttle exsides the steering else add reward
    if abs(steering) > .5 and abs(steering > throttle):
        reward *= 1 - (steering - throttle)
    else:
        reward *= 1 + throttle

    # make sure reward value returned is within the prescribed value range.
    reward = max(reward, -1e5)
    reward = min(reward, 1e5)

    return float(reward)