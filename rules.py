import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def bot_speed(front_distance, angle_goal_player):
    rules = []
    # Define the fuzzy variables
    # r_sens = ctrl.Antecedent(np.arange(0, 50, 0.2), 'r_sens')
    # l_sens = ctrl.Antecedent(np.arange(0, 50, 0.2), 'l_sens')



    f_sens = ctrl.Antecedent(np.arange(0, 50, 0.2), 'f_sens')
    f_sens['danger'] = fuzz.trimf(f_sens.universe, [2, 10, 15])
    f_sens['close'] = fuzz.trimf(f_sens.universe, [5, 20, 25])
    f_sens['med'] = fuzz.trimf(f_sens.universe, [15, 30, 40])
    f_sens['far'] = fuzz.trimf(f_sens.universe, [30, 40, 50])

    atg = ctrl.Antecedent(np.arange(-180, 180, 1.0), 'atg')
    atg['full_left'] = fuzz.trimf(atg.universe, [-200, -120, -70])
    atg['left'] = fuzz.trimf(atg.universe, [-100, -60, -20])
    atg['small_left'] = fuzz.trimf(atg.universe, [-30, -15, -2])
    atg['straight'] = fuzz.trimf(atg.universe, [-5, 0, 5])
    atg['small_right'] = fuzz.trimf(atg.universe, [2, 15, 30])
    atg['right'] = fuzz.trimf(atg.universe, [20, 60, 100])
    atg['full_right'] = fuzz.trimf(atg.universe, [70, 120, 200])

    # Define the membership functions for FRONT sensor
    # r_sens['danger'] = fuzz.trimf(r_sens.universe, [2, 10, 15])
    # r_sens['close'] = fuzz.trimf(r_sens.universe, [5, 20, 25])
    # r_sens['med'] = fuzz.trimf(r_sens.universe, [15, 30, 40])
    # r_sens['far'] = fuzz.trimf(r_sens.universe, [30, 40, 50])

    # Define the membership functions for FRONT sensor
    # l_sens['danger'] = fuzz.trimf(l_sens.universe, [2, 10, 15])
    # l_sens['close'] = fuzz.trimf(l_sens.universe, [5, 20, 25])
    # l_sens['med'] = fuzz.trimf(l_sens.universe, [15, 30, 40])
    # l_sens['far'] = fuzz.trimf(l_sens.universe, [30, 40, 50])


    bot_speed = ctrl.Consequent(np.arange(0, 3, 0.1), 'bot_speed')
    # Define the membership functions for bot speed
    bot_speed['stop'] = fuzz.trimf(bot_speed.universe, [0, 0, 0])
    bot_speed['low'] = fuzz.trimf(bot_speed.universe, [0.4, 0.7, 1.1])
    bot_speed['med'] = fuzz.trimf(bot_speed.universe, [0.9, 1.4, 2.2])
    bot_speed['high'] = fuzz.trimf(bot_speed.universe, [2.0, 2.5, 3.0])

    bot_turn = ctrl.Consequent(np.arange(-31, 31, 1.0), 'bot_turn')
    # Define the membership functions for bot turn
    bot_turn['full_left'] = fuzz.trimf(bot_turn.universe, [-7, -4, -1])
    bot_turn['left'] = fuzz.trimf(bot_turn.universe, [-7, -4, -1])
    bot_turn['small_left'] = fuzz.trimf(bot_turn.universe, [-7, -4, -1])
    bot_turn['straight'] = fuzz.trimf(bot_turn.universe, [-2, 0, 2])
    bot_turn['small_right'] = fuzz.trimf(bot_turn.universe, [1, 4, 7])
    bot_turn['right'] = fuzz.trimf(bot_turn.universe, [1, 4, 7])
    bot_turn['full_right'] = fuzz.trimf(bot_turn.universe, [1, 4, 7])


    # Define the speed rules
    rules.append(ctrl.Rule(f_sens['danger'], bot_speed['stop']))
    rules.append(ctrl.Rule(f_sens['close'], bot_speed['low']))
    rules.append(ctrl.Rule(f_sens['med'], bot_speed['med']))
    rules.append(ctrl.Rule(f_sens['far'], bot_speed['high']))


    # Define the turn rules
    rules.append(ctrl.Rule(atg['full_left'], bot_turn['full_right']))
    rules.append(ctrl.Rule(atg['left'], bot_turn['right']))
    rules.append(ctrl.Rule(atg['small_left'], bot_turn['small_right']))
    rules.append(ctrl.Rule(atg['straight'], bot_turn['straight']))
    rules.append(ctrl.Rule(atg['small_right'], bot_turn['small_left']))
    rules.append(ctrl.Rule(atg['right'], bot_turn['left']))
    rules.append(ctrl.Rule(atg['full_right'], bot_turn['full_left']))

    rules.append(ctrl.Rule(f_sens['close'], bot_turn['full_right']))
    rules.append(ctrl.Rule(f_sens['close'] & atg['straight'], bot_turn['straight']))
    rules.append(ctrl.Rule(f_sens['danger'], bot_turn['right']))
    rules.append(ctrl.Rule(f_sens['med'], bot_turn['small_right']))
    rules.append(ctrl.Rule(f_sens['far'], bot_turn['straight']))

    # rules.append(ctrl.Rule(f_sens['danger'] & atg['straight'], bot_turn['full_left']))
    # rules.append(ctrl.Rule(f_sens['close'] & atg['straight'], bot_turn['full_left']))
    # rules.append(ctrl.Rule(f_sens['med'] & atg['straight'], bot_turn['left']))
    #
    #
    # rules.append(ctrl.Rule(f_sens['danger'] & atg['right'], bot_turn['full_right']))
    # rules.append(ctrl.Rule(f_sens['close'] & atg['right'], bot_turn['full_right']))
    # rules.append(ctrl.Rule(f_sens['med'] & atg['right'], bot_turn['right']))


    # rules.append(ctrl.Rule(l_sens['danger'], bot_speed['stop']))
    # rules.append(ctrl.Rule(l_sens['close'], bot_speed['low']))

    # rules.append(ctrl.Rule(r_sens['danger'], bot_speed['stop']))
    # rules.append(ctrl.Rule(r_sens['close'], bot_speed['low']))




    # Define the turn rules
    # rules.append(ctrl.Rule(r_sens['danger'], bot_turn['full_left']))
    # rules.append(ctrl.Rule(r_sens['close'], bot_turn['left']))
    # rules.append(ctrl.Rule(r_sens['med'], bot_turn['small_left']))
    # rules.append(ctrl.Rule(r_sens['far'], bot_turn['straight']))
    #
    # rules.append(ctrl.Rule(l_sens['danger'], bot_turn['full_right']))
    # rules.append(ctrl.Rule(l_sens['close'], bot_turn['right']))
    # rules.append(ctrl.Rule(l_sens['med'], bot_turn['small_right']))
    # rules.append(ctrl.Rule(l_sens['far'], bot_turn['straight']))


    # Create the control system
    bot_control = ctrl.ControlSystem(rules)
    bot_move = ctrl.ControlSystemSimulation(bot_control)
    # Set input values for f_sens and humidity
    bot_move.input['f_sens'] = front_distance
    bot_move.input['atg'] = angle_goal_player
    # bot_move.input['r_sens'] = right_distance
    # bot_move.input['l_sens'] = left_distance
    # Compute the output
    bot_move.compute()
    # Print the result
    print(f"Speed: {bot_move.output['bot_speed']}")
    print(f"turn: {bot_move.output['bot_turn']}")
    return bot_move.output['bot_speed'], bot_move.output['bot_turn']

bot_speed(10, 66)
