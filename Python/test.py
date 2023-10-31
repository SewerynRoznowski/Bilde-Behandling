import math

def calculate_triangle_sides(side_c, angle_a, angle_b):
    # Convert angles from degrees to radians

    angle_c = 180 - angle_a - angle_b

    angle_a_rad = math.radians(angle_a)
    angle_b_rad = math.radians(angle_b)
    angle_c_rad = math.radians(angle_c)

    
    # Use the Law of Sines to find the length of side_b
    side_b = (side_c * math.sin(angle_b_rad)) / math.sin(angle_c_rad)
    
    # Use the Law of Sines to find the length of side_c
    side_a = (side_c * math.sin(angle_a_rad)) / math.sin(angle_c_rad)
    
    return side_a, side_b


trekant,trekant1 = calculate_triangle_sides(8, 32, 17)

print (trekant,trekant1)