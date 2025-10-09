import sys

import rclpy
from rclpy.node import Node

from perception_interfaces.srv import GetCubePoses


class CubePosesClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(GetCubePoses, 'cube_poses')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetCubePoses.Request()

    def send_request(self):
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    minimal_client = CubePosesClientAsync()
    future = minimal_client.send_request()
    rclpy.spin_until_future_complete(minimal_client, future)
    response = future.result()
    print(response)

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()