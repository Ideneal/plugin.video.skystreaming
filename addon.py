import sys
import os

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, 'resources', 'lib'))
import plugin

if __name__ == '__main__':
    plugin.start()