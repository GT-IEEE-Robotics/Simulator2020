import time
import multiprocessing
from simulator.game import Game

# Constants
SRRESET = 0
SREND = 1
SRSTEP = 2
SRTIME = 3
SRIMAGE = 4
SRPOSE = 5
SRWHEELS = 6
SRENABLED = 7

class SimConfig:
    def __init__(self, bin_configuration_yaml):
        self.bin_configuration_yaml = bin_configuration_yaml

        self.use_interactive = True
        self.is_interactive_realtime = True
        self.hide_ui = True
        self.topdown_viewport = False

        # self.use_headless = False # used to implement parallization
        # self.num_headless = 0     # see: https://github.com/bulletphysics/bullet3/issues/1925#issuecomment-428355937
        
        self.starting_state_fname = None
        self.starting_robot_pose = None
        self.starting_time = 0.0
        self.auto_enable_timer = 0.0
        self.skew = 0.0

        self.log_dir = None
        self.log_bullet_states = False
        self.log_mp4 = False

    def validate(self):
        """Validate the current configurations for
        any inconsistencies.
        """
        # TODO implement
        pass
        

# ----------- Sim Server Side -----------

def _sim_server(q, s, sim_config):
    g = Game(use_interactive=sim_config.use_interactive,
             is_interactive_realtime=sim_config.is_interactive_realtime,
             hide_ui=sim_config.hide_ui,
             topdown_viewport=sim_config.topdown_viewport,
             log_dir=sim_config.log_dir,
             log_bullet_states=sim_config.log_bullet_states,
             log_mp4=sim_config.log_mp4,
             robot_skew=sim_config.skew)
    g.setup(bin_configuration_yaml=sim_config.bin_configuration_yaml,
            starting_state_fname=sim_config.starting_state_fname,
            starting_robot_pose=sim_config.starting_robot_pose,
            starting_time=sim_config.starting_time,
            auto_enable_timer=sim_config.auto_enable_timer)

    uncompleted_steps = 0
    while True:
        if sim_config.is_interactive_realtime or uncompleted_steps > 0:
            g.step()
            uncompleted_steps -= 1 if uncompleted_steps > 0 else 0
        if q.empty(): continue

        req_token = q.get()
        if type(req_token) is tuple:
            if req_token[0] == SRSTEP:
                uncompleted_steps = req_token[1]
                s.put(True)
            elif req_token[0] == SRTIME:
                g.time = req_token[1]
                s.put(g.time)
            elif req_token[0] == SRPOSE:
                s.put(g.mobile_agent.set_pose(req_token[1]))
            elif req_token[0] == SRWHEELS:
                s.put(g.mobile_agent.command_wheel_velocities(req_token[1], req_token[2]))
            elif req_token[0] == SRENABLED:
                g.mobile_agent.enabled = req_token[1]
                s.put(g.mobile_agent.enabled)
        elif req_token == SRRESET:
            s.put(g.reset())
        elif req_token == SREND:
            s.put(True)
            break
        elif req_token == SRTIME:
            s.put(g.time)
        elif req_token == SRIMAGE:
            s.put(g.mobile_agent.capture_image())
        elif req_token == SRPOSE:
            s.put(g.mobile_agent.get_pose())
        elif req_token == SRWHEELS:
            s.put(g.mobile_agent.read_wheel_velocities())
        elif req_token == SRENABLED:
            s.put(g.mobile_agent.enabled)
        else:
            print("simserver, something new came: ", req_token)

# ------------- Client Side -------------
req_queue = multiprocessing.Queue()
res_queue = multiprocessing.Queue()

def request(value):
    while not req_queue.empty(): pass
    while not res_queue.empty(): pass
    req_queue.put(value)
    while res_queue.empty(): pass
    return res_queue.get()

def start(config):
    p = multiprocessing.Process(target=_sim_server, args=(req_queue, res_queue, config))
    p.start()

def restart():
    return request(SRRESET)

def end():
    return request(SREND)

def step(num_steps=1):
    return request((SRSTEP, num_steps))

def get_time():
    return request(SRTIME)

def set_time(time):
    return request((SRTIME, time))

def read_robot_cam():
    return request(SRIMAGE)

def get_robot_pose():
    return request(SRPOSE)

def set_robot_pose(pose):
    return request((SRPOSE, pose))

def read_robot_vels():
    return request(SRWHEELS)

def command_robot_vels(lwheel_vel, rwheel_vel):
    return request((SRWHEELS, lwheel_vel, rwheel_vel))

def get_enabled():
    return request(SRENABLED)

def set_enabled(enabled):
    return request((SRENABLED, enabled))

'''
function list
-----
CONCEPTS:
 - simulations
   - time, position of objects, and world
   - realtime / iteration steps
   - debug visualizer
 
   - game
     - time left in the game
     - points the agent won

   - environment
     - position of objects in the world

   - agents
     - keep track of their images
     - stepper position

 - configuration
   - parameters regarding the simulation and game

   - interactive
     - either realtime or iterations
   - headless (n)
     - iterations
   - start state
   - logging?
     - saveWorld, saveState, restoreState, saveBullet
   - set debug camera position (p.configureDebugVisualizer(p.COV_ENABLE_GUI,0))

-----

    start(config)
    restart()
    end()

    step(num_steps=1)

    get_time()
    set_time()

    get_pose()
    set_pose()

    capture_image()

    command_wheels(left_omega, right_omega)
    read_wheels()

command_stepper(position)
read_stepper()

get_score()
get_time_remaining()
is_failed()

visualize_curve()
'''
