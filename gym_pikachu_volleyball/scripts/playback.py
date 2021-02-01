import cv2
import gym
import pyglet
import argparse
import numpy as np

env = gym.make('gym_pikachu_volleyball:pikachu-volleyball-v0', isPlayer1Computer=True, isPlayer2Computer=False)

parser = argparse.ArgumentParser()
parser.add_argument('--game_id', type=int, required=True)
parser.add_argument('--path', default='output.avi')
args = parser.parse_args()

with open('actions.txt', 'r') as f:
    line = f.readlines()[args.game_id]

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args.path,fourcc, 30.0, (1728,1216))

    seed, actions, _ = line.split(',')
    actions = actions.strip('\n')

    env.seed(int(seed))
    env.reset()
    env.render()
    env.viewer.window.set_visible(False)

    for action in actions:
        action = ord(action) - 65
        env.step((0, action))
        env.render()
        
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        image_data = buffer.get_image_data()
        arr = np.frombuffer(image_data.get_data(), dtype=np.uint8)
        arr = arr.reshape(buffer.height, buffer.width, 4)
        arr = arr[::-1,:,0:3]
        arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        out.write(arr)

out.release()

