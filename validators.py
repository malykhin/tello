def is_distance_valid(value):
    return value >= 20 and value <= 500


def is_degree_valid(value):
    return value >= 1 and value <= 360


def is_flip_direction_valid(direction):
    return direction in ['l', 'r', 'f', 'b']


def is_speed_valid(value):
    return value >= 10 and value <= 100


def is_curve_speed_valid(value):
    return value >= 1 and value <= 60


def is_rc_control_valid(value):
    return value >= -100 and value <= 100


def is_string_valid(value):
    return isinstance(value, str)


def validate_go(x, y, z, speed):
    if not is_distance_valid(x):
        return 'error_invalid_distance:x'
    if not is_distance_valid(y):
        return 'error_invalid_distance:y'
    if not is_distance_valid(z):
        return 'error_invalid_distance:z'
    if not is_speed_valid(speed):
        return 'error_invalid_speed'
    return None


def validate_curve(x1, y1, z1, x2, y2, z2, speed):
    if not is_distance_valid(x1):
        return 'error_invalid_distance:x1'
    if not is_distance_valid(y1):
        return 'error_invalid_distance:y1'
    if not is_distance_valid(z1):
        return 'error_invalid_distance:z1'
    if not is_distance_valid(x2):
        return 'error_invalid_distance:x2'
    if not is_distance_valid(y2):
        return 'error_invalid_distance:y2'
    if not is_distance_valid(z2):
        return 'error_invalid_distance:z2'
    if not is_curve_speed_valid(speed):
        return 'error_invalid_curve_speed'
    return None


def validate_rc_control(a, b, c, d):
    if not is_rc_control_valid(a):
        return 'error_invalid_rc_control:a'
    if not is_rc_control_valid(b):
        return 'error_invalid_rc_control:b'
    if not is_rc_control_valid(c):
        return 'error_invalid_rc_control:c'
    if not is_rc_control_valid(d):
        return 'error_invalid_rc_control:d'
    return None


def validate_move(distance):
    print(distance)
    if not is_distance_valid(distance):
        return 'error_invalid_distance'
    return False


def validate_flip(direction):
    if not is_flip_direction_valid(direction):
        return 'error_invalid_direction'
    return None


def validate_rotate(degree):
    if not is_degree_valid(degree):
        return 'error_invalid_degree'
    return None
