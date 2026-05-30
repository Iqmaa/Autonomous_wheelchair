#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
from geometry_msgs.msg import Twist

class ObstacleAvoidanceChair(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_chair')
        
        self.publisher = self.create_publisher(Twist, '/wheel_controller/cmd_vel_unstamped', 10)
        self.subscription = self.create_subscription(PointCloud2, '/scan/points', self.pointcloud_callback, 10)
        
        self.timer = self.create_timer(0.1, self.control_loop)
        self.cmd_vel = Twist()

        # State Tracking Flags
        self.obstacle_ahead = False
        self.obstacle_behind = False
        self.min_distance_found = 12.0

    def pointcloud_callback(self, msg):
        """ Processes 3D PointCloud matrix to track separate forward/backward hazard spaces """
        ahead_flag = False
        behind_flag = False
        closest_point = 12.0

        # Unpack raw byte stream into Cartesian spatial elements
        points = pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)

        for x, y, z in points:
            # 1. FIXED SELF-DETECTION ZONE
            # Protects a tight box around the central structural frame/seat/mast footprint
            if -0.3 < x < 0.3 and abs(y) < 0.55:
                continue

            # 2. SEPARATE DIRECTIONAL EVALUATION BALANCING
            # Width window: 80cm (abs(y) < 0.40) | Height window: 1.2m (abs(z) < 0.60)
            if abs(y) < 0.95 and abs(z) < 0.70:
                
                # Check Front Zone (0.28m out to 2.5m ahead)
                if 0.3 <= x < 1.4:
                    ahead_flag = True
                    if x < closest_point:
                        closest_point = x
                        
                # Check Rear Zone (-2.5m behind up to -0.28m)
                elif -2.5 < x <= -0.3:
                    behind_flag = True
                    if abs(x) < closest_point:
                        closest_point = abs(x)

        self.obstacle_ahead = ahead_flag
        self.obstacle_behind = behind_flag
        self.min_distance_found = closest_point
        
        self.get_logger().info(
            f"Front Haz: {self.obstacle_ahead} | Rear Haz: {self.obstacle_behind} | Closest: {self.min_distance_found:.2f}m"
        )

    def control_loop(self):
        # Reset velocities safely every iteration frame loop
        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0

        if self.obstacle_ahead:
            # Hazard is in front -> Back up smoothly and swing the chassis away
            self.cmd_vel.linear.x = 0.0 #-0.25 
            self.cmd_vel.angular.z = 0.6  
            self.get_logger().warn("⚠️ Obstacle ahead detected! Executing reverse escape...")
            
        elif self.obstacle_behind:
            # Hazard is behind -> Move forward away from it cleanly
            self.cmd_vel.linear.x = 0.35    
            self.cmd_vel.angular.z = 0.6    
            self.get_logger().warn("⚠️ Obstacle behind detected! Driving forward away...")
            
        else:
            # Path completely clear -> Cruise straight ahead normal speed
            self.cmd_vel.linear.x = 0.40    
            self.cmd_vel.angular.z = 0.0    

        # Output to real-time diff-drive engine controller lanes
        self.publisher.publish(self.cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    chair = ObstacleAvoidanceChair()
    rclpy.spin(chair)
    rclpy.shutdown()

if __name__ == '__main__':
    main()