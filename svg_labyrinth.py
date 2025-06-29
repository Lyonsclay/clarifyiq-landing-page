import math

def get_coords(radius, angle_degrees, center_x=100, center_y=100):
    """Calculates x, y coordinates on a circle given radius and angle."""
    angle_radians = math.radians(angle_degrees)
    x = center_x + radius * math.cos(angle_radians)
    y = center_y + radius * math.sin(angle_radians)
    return round(x, 2), round(y, 2)

def calculate_svg_arc_segment(radius, center_x, center_y, start_angle_deg, end_angle_deg):
    """
    Calculates the 'd' attribute string for an SVG arc segment.
    Ensures start and end points are precise and flags are correct for arcs.
    """
    start_x, start_y = get_coords(radius, start_angle_deg, center_x, center_y)
    end_x, end_y = get_coords(radius, end_angle_deg, center_x, center_y)

    # Calculate the difference in angles, handling wrap-around for large-arc-flag
    angle_diff = end_angle_deg - start_angle_deg
    if angle_diff < 0:
        angle_diff += 360 # Adjust for arcs that cross 0/360, e.g., 300 to 30

    large_arc_flag = 1 if angle_diff > 180 else 0
    sweep_flag = 1 # Always clockwise for this design

    path_d = f"M {start_x},{start_y} A {radius},{radius} 0 {large_arc_flag},{sweep_flag} {end_x},{end_y}"
    return path_d

def generate_labyrinth_segments_d_attributes(linear_gap_width=15, center_x=100, center_y=100):
    """
    Generates the 'd' attributes for all segments of the labyrinth.
    Applies consistent linear gap width at specified angles.
    """

    radii = [30, 45, 60, 75]

    # Define the 8 conceptual 45-degree "divider" angles (0, 45, 90, ..., 315, 360)
    segment_dividers = [0, 45, 90, 135, 180, 225, 270, 315, 360]

    # Angles where gaps are centered (0/360 is handled by adjusting segments around it)
    gap_centers_deg = [0, 45, 90, 135, 180, 225, 270, 315, 360] # These are the 5 locations for gaps

    all_segments_d_attrs = []

    for circle_idx, r in enumerate(radii):
        # Calculate the angular width required for the linear gap for this specific radius
        if r == 0: # Avoid division by zero for central point, though not used here
            half_gap_angle = 0
        else:
            total_gap_angular_width = math.degrees(linear_gap_width / r)
            half_gap_angle = total_gap_angular_width / 2

        # Iterate through the 8 conceptual 45-degree segments
        for i in range(8):
            theoretical_segment_start_angle = segment_dividers[i]
            theoretical_segment_end_angle = segment_dividers[i+1]

            actual_start_angle = theoretical_segment_start_angle
            actual_end_angle = theoretical_segment_end_angle

            # Adjust start angle if it's at a gap center
            if theoretical_segment_start_angle in gap_centers_deg:
                actual_start_angle += half_gap_angle
            elif theoretical_segment_start_angle == 360 and 0 in gap_centers_deg: # Handle 360 as 0
                actual_start_angle = 0 + half_gap_angle

            # Adjust end angle if it's at a gap center
            if theoretical_segment_end_angle in gap_centers_deg:
                actual_end_angle -= half_gap_angle
            elif theoretical_segment_end_angle == 360 and 0 in gap_centers_deg: # Handle 360 as 0
                actual_end_angle = 360 - half_gap_angle

            # Edge case: If a segment theoretically spans a gap center, it gets shortened from both ends.
            # Example: segment from 0 to 45, if 0 and 45 are gap centers.
            # This logic already handles it because `actual_start_angle` and `actual_end_angle` are adjusted independently.

            # Ensure angles wrap correctly for `calculate_svg_arc_segment` if needed
            if actual_start_angle >= 360: actual_start_angle -= 360
            if actual_end_angle >= 360: actual_end_angle -= 360

            # Special handling for arcs that cross 360 (e.g., 340 to 20 deg).
            # The `calculate_svg_arc_segment` function's `large_arc_flag` and `sweep_flag` logic handles this.

            d_attr = calculate_svg_arc_segment(r, center_x, center_y, actual_start_angle, actual_end_angle)
            all_segments_d_attrs.append(f'<path id="C{circle_idx}-S{i}" class="concentric-circle-path" d="{d_attr}" />')

    return all_segments_d_attrs

# --- Generate the segments and print for copying into HTML ---
if __name__ == "__main__":
    generated_segments_html = generate_labyrinth_segments_d_attributes()
    # print("\n".join(generated_segments_html)) # Uncomment to see the output
