from pynput.mouse import Button, Controller as mouseController;
from pynput.keyboard import Key, Controller as keyBoardController;
import json;
import time;

mouse = mouseController();
keyboard = keyBoardController();

# PyUserInput 键盘事件不全  鼠标双击在mac不生效
# pyautogui 每两次移动鼠标之间有最短0.1s的duration  鼠标双击在mac不生效
# 这里选用pynput

def mouse_move(dis_axis):
    mouse.move(dis_axis['disX'] * 3, dis_axis['disY'] * 3);

def user_tap():
    mouse.click(Button.left, 1);

def user_long_press():
    mouse.click(Button.right, 1);

def user_double_tap():
    mouse.click(Button.left, 2);

def keyboard_press(clickKey):
    keyboard.press(Key[clickKey]);

def hot_key_press(hot_key):
    keys = hot_key.split('+');
    with keyboard.pressed(Key[keys[0]]):
        keyboard.press(keys[1]);
        keyboard.release(keys[1]);

def user_input(message):
    keyboard.type(message);

operation_map = {
    'tap': user_tap,
    'doubleTap': user_double_tap,
    'longPress': user_long_press,
    'move': mouse_move,
    'keyboard_press': keyboard_press,
    'hot_key_press': hot_key_press,
    'input': user_input
}

def user_target(target):
    target_dict = json.loads(target);
    if target_dict['operation'] == 'move':
        operation_map['move'](target_dict['axis']);
    elif target_dict['operation'] == 'input':
        operation_map['input'](target_dict['message']);
    elif target_dict['operation'] == 'keyboard_press':
        operation_map['keyboard_press'](target_dict['key']);
    elif target_dict['operation'] == 'hot_key_press':
        operation_map['hot_key_press'](target_dict['key']);
    else:
        operation_map[target_dict['operation']]();
