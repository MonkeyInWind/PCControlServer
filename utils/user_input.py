from pymouse import PyMouse;
from pykeyboard import PyKeyboard;
import json;
import time;

m = PyMouse();
k = PyKeyboard();

def mouse_move(disAxis):
    current_axis = m.position();
    # print(axis[0]);
    # print(disAxis);
    nextX = current_axis[0] + disAxis['disX'] * 3;
    nextY = current_axis[1] + disAxis['disY'] * 3;
    print(nextX, nextY);
    m.move(nextX, nextY);

def user_tap():
    position = m.position();
    m.click(position[0], position[1]);
    print('tap');

def user_long_press():
    position = m.position();
    m.click(position[0], position[1], 2);
    print('long press');

def user_double_tap():
    position = m.position();
    m.click(position[0], position[1], 1, 2);
    print('double tap');

operation_map = {
    'tap': user_tap,
    'doubleTap': user_double_tap,
    'longPress': user_long_press,
    'move': mouse_move
}

def user_target(target):
    target_dict = json.loads(target);
    if 'axis' in target_dict:
        operation_map[target_dict['operation']](target_dict['axis']);
    else:
        operation_map[target_dict['operation']]();
