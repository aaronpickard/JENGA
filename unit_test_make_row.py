import block
import path_to_wall
import gcode
import os
import my_utils

os.remove("output_coordinates.csv")
os.remove("output_instructions.csv")
os.remove("output_instructions.txt")
my_block = block.Block()
my_path = path_to_wall.Basic()
my_code = gcode.GCode()

def test1():
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
    my_code.move_vertical(pickup, my_code.separation_height)
    tmp_u_height = pickup[2] + my_code.separation_height
    tmp_up = [pickup[0], pickup[1], tmp_u_height]
    tmp_d_height = putdown[2] + my_code.separation_height
    tmp_down = [putdown[0], putdown[1], tmp_d_height]
    my_code.move_orrian_algo(my_code.current_point, tmp_down)
    my_code.move_down(my_code.current_point, tmp_d_height)
    print("tmp_down = " + str(tmp_down) + "\ntmp_d_height = " + str(tmp_d_height))
    # my_code.move_orrian_algo(tmp_up, putdown)
    # my_code.move_vertical(putdown, my_code.separation_height)
    """
    act_height = putdown[2] - my_code.separation_height
    my_code.print_command([putdown[0], putdown[1], act_height])
    my_code.putdown_brick(putdown)
    """
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
    my_utils.find_max_z_value("output_coordinates.csv")


def test2():
    """
    Tests move_vertical (up) and move_down (down) functions
    :return:
    """
    my_code.print_comment("INSTRUCTION SET BEGINS")
    my_code.print_comment("Instruction set initialization")
    my_code.set_units()
    # my_code.set_output_file(output_file)
    neutral = my_code.neutral_point
    pickup = [-80, 0, 0]
    my_code.move_vertical(pickup, my_code.separation_height)
    my_code.print_command([-25, 25, my_code.separation_height])
    my_code.move_down(my_code.current_point, my_code.separation_height)


test1()
