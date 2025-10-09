import geometry_msgs.msg
import rclpy
from example_interfaces.srv import Trigger

from pycram.datastructures.pose import PoseStamped
from pycram.datastructures.world import World
from pycram.ros import create_subscriber, node

from perception_interfaces.msg import CubePoses
from perception_interfaces.srv import GetCubePoses

world : World = None

def update_object_poses(poses):
    for pose in poses:
        obj_name = pose[0]
        obj_pose = PoseStamped.from_ros_message(pose[1])
        if world is not None:
            for obj in world.objects:
                if obj.name == obj_name:
                    obj.set_pose(obj_pose)

class PerceptionClient:
    def __init__(self):
        self.client = node.create_client(Trigger, "save_camera_frames")
        create_subscriber("/Current_OBJ_position_0", geometry_msgs.msg.PoseStamped, self.callback0, 10)
        create_subscriber("/Current_OBJ_position_1", geometry_msgs.msg.PoseStamped, self.callback1, 10)
        create_subscriber("/Current_OBJ_position_2", geometry_msgs.msg.PoseStamped, self.callback2, 10)
        self.cube1_pose = PoseStamped()
        self.cube2_pose = PoseStamped()
        self.cube3_pose = PoseStamped()
        self.req = Trigger.Request()

    def callback0(self, msg):
        self.cube1_pose = msg
        print("received cube1 pose")

    def callback1(self, msg):
        self.cube2_pose = msg
        print("received cube2 pose")

    def callback2(self, msg):
        self.cube3_pose =msg
        print("received cube3 pose")

    def request(self):
        future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(node, future)
        response = future.result()
        print(response)
        poses = [("Cube_1", self.cube1_pose), ("Cube_2", self.cube2_pose), ("Cube_3", self.cube3_pose)]
        print(poses)
        update_object_poses(poses)

class PerceptionClientNew:
    def __init__(self):
        self.client = node.create_client(GetCubePoses, "save_camera_frames")
        self.req = GetCubePoses.Request()

    def request(self):
        future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(node, future)
        response = future.result()
        poses = [("Cube_1", response.cube_1_pose), ("Cube_2", response.cube_2_pose), ("Cube_3", response.cube_3_pose)]
        update_object_poses(poses)
