import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FlaskSubscriber(Node):
    def __init__(self):
        super().__init__('flask_subscriber')
        self.subscription = self.create_subscription(
            String,
            'flask_msg',
            self.listener_callback,
            10)
        self.subscription
    
    def listener_callback(self, msg):
        self.get_logger().info('I heard: %s' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    flask_subscriber = FlaskSubscriber()
    rclpy.spin(flask_subscriber)

    flask_subscriber.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()