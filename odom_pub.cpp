#include "ros/ros.h"
#include <tf/transform_broadcaster.h>
#include<geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include "std_msgs/MultiArrayLayout.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/Float64MultiArray.h"
#include <vector>

void position_callback(const std_msgs::Float64MultiArray::ConstPtr& odom_data);
void publish_odomtery(float position_x,float position_y,float oriention,
                    float vel_linear_x,float vel_linear_y,float vel_linear_w);

float position_x;
float position_y;
float position_w;
float vel_linear_x;
float vel_linear_y;
float vel_linear_w;
nav_msgs::Odometry odom;

int main(int argc, char **argv)
{
    ros::init(argc, argv, "odom_pub");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("odom_data", 1, position_callback);
    ros::Publisher odom_pub = nh.advertise<nav_msgs::Odometry>("odom",1);
    ros::Rate rate(20);
    while(ros::ok())
    {
        ros::spinOnce();
        publish_odomtery(position_x,position_y,position_w,vel_linear_x,vel_linear_y,vel_linear_w);
        odom_pub.publish(odom);
        rate.sleep();
    }

}

void position_callback(const std_msgs::Float64MultiArray::ConstPtr& odom_data)
{
    position_x = odom_data->data[0];
    position_y = odom_data->data[1];
    position_w = odom_data->data[2];
    vel_linear_x = odom_data->data[3];
    vel_linear_y = odom_data->data[4];
    vel_linear_w = odom_data->data[5];
}

void publish_odomtery(float position_x,float position_y,float oriention,float vel_linear_x,float vel_linear_y,float vel_linear_w)
{
    static tf::TransformBroadcaster odom_broadcaster;
    geometry_msgs::TransformStamped odom_trans;
    geometry_msgs::Quaternion odom_quat;

    odom_quat = tf::createQuaternionMsgFromYaw(oriention);

    odom_trans.header.stamp = ros::Time::now();
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "base_link";

    odom_trans.transform.translation.x = position_x;
    odom_trans.transform.translation.y = position_y;
    odom_trans.transform.translation.z = 0.0;
    odom_trans.transform.rotation = odom_quat;

    odom_broadcaster.sendTransform(odom_trans);

    odom.header.stamp = ros::Time::now();
    odom.header.frame_id = "odom";
    odom.child_frame_id = "base_link";

    odom.pose.pose.position.x = position_x;
    odom.pose.pose.position.y = position_y;
    odom.pose.pose.position.z = 0.0;
    odom.pose.pose.orientation = odom_quat;

    odom.twist.twist.linear.x = vel_linear_x;
    odom.twist.twist.linear.y = vel_linear_y;
    odom.twist.twist.angular.z = vel_linear_w;
}