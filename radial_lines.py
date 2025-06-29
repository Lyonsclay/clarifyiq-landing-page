import math

def calculate_radial_line(center_x, center_y, angle_degrees, start_radius, line_length):
    """
    Calculates the start and end coordinates for a line at a specific angle
    around a center point.

    Args:
        center_x (int): The x-coordinate of the center point.
        center_y (int): The y-coordinate of the center point.
        angle_degrees (int): The angle of the line in degrees (0 is to the right).
        start_radius (int): The distance from the center to where the line begins.
        line_length (int): The length of the line.

    Returns:
        dict: A dictionary containing the 'start' (x1, y1) and 'end' (x2, y2)
              coordinates for the line.
    """
    # Convert the angle from degrees to radians for math functions
    angle_radians = math.radians(angle_degrees)

    # Calculate the start point (x1, y1) on the inner circle
    x1 = center_x + start_radius * math.cos(angle_radians)
    y1 = center_y + start_radius * math.sin(angle_radians)

    # Calculate the end point (x2, y2) by extending the line outwards
    end_radius = start_radius + line_length
    x2 = center_x + end_radius * math.cos(angle_radians)
    y2 = center_y + end_radius * math.sin(angle_radians)

    coordinates = {
        'start': (round(x1), round(y1)),
        'end': (round(x2), round(y2))
    }

    return coordinates

# --- Example Usage ---
# Center point of your SVG animation
center_x = 400
center_y = 300

# Parameters for your graphic
# Distance from the center of the logo to the start of the line
distance_from_center = 80
# The length of the connector line
length_of_line = 60
# The angle for the line you want to calculate
angle_for_line = 45 # Example: 45 degrees

# Get the coordinates for a single line
line_coords = calculate_radial_line(
    center_x,
    center_y,
    angle_for_line,
    distance_from_center,
    length_of_line
)

# Print the results
x1, y1 = line_coords['start']
x2, y2 = line_coords['end']
print(f"Line at {angle_for_line} degrees: x1=\"{x1}\" y1=\"{y1}\" x2=\"{x2}\" y2=\"{y2}\"")

# --- Example for all 5 documents ---
print("\n--- Coordinates for 5 Documents ---")
angles = [0, 72, 144, 216, 288] # 360 / 5 = 72 degree steps

for i, angle in enumerate(angles):
    coords = calculate_radial_line(
        center_x,
        center_y,
        angle,
        distance_from_center,
        length_of_line
    )
    x1, y1 = coords['start']
    x2, y2 = coords['end']
    print(f"Document {i+1} (Angle {angle}°): x1=\"{x1}\" y1=\"{y1}\" x2=\"{x2}\" y2=\"{y2}\"")
