import rclpy
from rclpy.node import Node
from perception_interfaces.msg import CubePoses

from pycram.datastructures.pose import PoseStamped


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('testpublisher')
        self.publisher = self.create_publisher(CubePoses, 'Cube_Poses', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = CubePoses()
        self.publisher.publish(msg)


def main():
    rclpy.init()

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()