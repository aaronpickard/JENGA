import block
import path_to_wall
import gcode
import os

os.remove("output_coordinates.csv")
os.remove("output_instructions.csv")
os.remove("output_instructions.txt")
my_block = block.Block()
my_path = path_to_wall.Basic()
my_code = gcode.GCode()

my_code.print_comment("INSTRUCTION SET BEGINS")
my_code.print_comment("Instruction set initialization")
my_code.set_units()
# my_code.set_output_file(output_file)
neutral = my_code.neutral_point
pickup = [-80, 0, 0]
my_path.load_pickup(pickup[0], pickup[1], pickup[2])
my_code.set_feed_rate(20)
my_code.set_tether_length()
putdown = [0, 0, 0]
my_path.load_putdown(putdown[0], putdown[1], putdown[2])


i = 0
my_code.pickup_brick(pickup)
my_code.move_orrian_algo(pickup, putdown)
# my_code.move_vertical(putdown, my_code.separation_height)
act_height = putdown[2] - my_code.separation_height
my_code.print_command([putdown[0], putdown[1], act_height])
my_code.putdown_brick(putdown)
# my_path.next_brick_in_x_row(putdown)

# my_code.pickup_brick(pickup)
# my_code.move_brick_to_placement(pickup, putdown)  # brick 1
# my_code.putdown_brick(putdown)
# my_code.move_brick_to_placement(putdown, pickup)
"""
while i < 4:
    my_path.mover(pickup, putdown)
    my_path.next_brick_in_x_row(putdown)
    i += 1
"""