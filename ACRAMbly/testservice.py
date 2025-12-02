import geometry_msgs.msg
import rclpy
from example_interfaces.srv import Trigger
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped

from perception_interfaces.srv import GetCubePoses
from perception_interfaces.msg import CubePoses


class GetCubePosesService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(GetCubePoses, 'cube_poses', self.callback)

    def callback(self, request, response):
        response.poses = CubePoses()
        response.poses.cube_1_pose = PoseStamped()
        response.poses.cube_2_pose = PoseStamped()
        response.poses.cube_3_pose = PoseStamped()
        return response

class TestService(Node):

    def __init__(self):
        super().__init__("test_service")
        self.srv = self.create_service(Trigger, "save_camera_frames", self.callback)
        self.publisher0 = self.create_publisher(PoseStamped, "/Current_OBJ_position_0", 10)
        self.publisher1 = self.create_publisher(PoseStamped, "/Current_OBJ_position_1", 10)
        self.publisher2 = self.create_publisher(PoseStamped, "/Current_OBJ_position_2", 10)

    def callback(self, request, response):
        pose = PoseStamped()
        self.publisher0.publish(pose)
        self.publisher1.publish(pose)
        self.publisher2.publish(pose)
        response.success = True
        return response



def main():
    rclpy.init()

    minimal_service = TestService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()