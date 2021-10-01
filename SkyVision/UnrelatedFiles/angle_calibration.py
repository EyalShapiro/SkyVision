import math
from fractions import Fraction

horizontal_resolution = int(input("enter the horizontal resolution"))
vertical_resolution = int(input("enter the Vertical resolution"))
diagonal_field_of_view = float(input("enter the diagonal field of view in deg"))
lens_focal_length = float(input("enter the lens focal length in mm"))
frac = Fraction(numerator=horizontal_resolution, denominator=vertical_resolution)  # getting the aspect ratio
horizontal_aspect = frac.numerator
print(f"horizontal_aspect {horizontal_aspect}")
vertical_aspect = frac.denominator
print(f"vertical_aspect {vertical_aspect}")
diagonal_aspect = (vertical_aspect ** 2 + horizontal_aspect ** 2) ** 0.5  # getting the diagonal aspect
print(f"diagonal_field_of_view {diagonal_field_of_view}")
horizontal_field_of_view = math.degrees(math.atan(
    math.tan(math.radians(diagonal_field_of_view / 2)) * (
            horizontal_aspect / diagonal_aspect)) * 2)  # getting the horizontal field of view in degrees
print(f"horizontal_field_of_view {horizontal_field_of_view}")
vertical_field_of_view = math.degrees(math.atan(
    math.tan(math.radians(diagonal_field_of_view / 2)) * (
            vertical_aspect / diagonal_aspect)) * 2)  # getting the vertical field of view in degrees
print(f"vertical_field_of_view {vertical_field_of_view}")
sensor_horizontal_length = math.tan(math.radians(horizontal_field_of_view / 2)) * (
            2 * lens_focal_length)  # getting the sensor horizontal length in mm
print(f"sensor_horizontal_length {sensor_horizontal_length}")
sensor_vertical_length = math.tan(math.radians(vertical_field_of_view / 2)) * (
            2 * lens_focal_length)  # getting the sensor vertical length in mm
print(f"sensor_vertical_length {sensor_vertical_length}")
micro_meter_to_pixel_ratio = sensor_horizontal_length / horizontal_resolution * 1000  # how much one pixel represent in the real world um/pixel
print(f"micro_meter_to_pixel_ratio {micro_meter_to_pixel_ratio}")
