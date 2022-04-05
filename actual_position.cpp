#include "ros/ros.h"
#include "std_msgs/MultiArrayLayout.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/Float64MultiArray.h"
#include <vector>


float vel[4];
void vel_callback(const std_msgs::Float64MultiArray::ConstPtr& vel_data);

int main(int argc, char **argv)
{
    ros::init(argc, argv, "actual_position");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("vel_data", 1, vel_callback);
    ros::Publisher pub = nh.advertise<std_msgs::Float64MultiArray>("odom_data",1);
    ros::Rate rate(1000);

    float a=28;//mm
    float b=30;//mm
    float vel_last[4]={0,0,0,0};
    float vel_delta[4]={0,0,0,0};
    float position_x=0,position_y=0,position_w=0;
    float vel_linear_x,vel_linear_y,vel_linear_w;
    float vel_linear_delta_x,vel_linear_delta_y,vel_linear_delta_w;

    while(ros::ok())
    {
        for(int i=0;i<4;i++)
            vel_last[i] = vel[i];
        ros::spinOnce();
        for(int i=0;i<4;i++)
            vel_delta[i] = vel[i]-vel_last[i];
        
        vel_linear_x = 0.25*(-vel[0]+vel[1]-vel[2]+vel[3]);
        vel_linear_y = 0.25*(vel[0]+vel[1]+vel[2]+vel[3]);
        vel_linear_w = (1/(4*(a+b)))*(vel[0]-vel[1]-vel[2]+vel[3]);

        vel_linear_delta_x = 0.25*(-vel_delta[0]+vel_delta[1]-vel_delta[2]+vel_delta[3]);
        vel_linear_delta_y = 0.25*(vel_delta[0]+vel_delta[1]+vel_delta[2]+vel_delta[3]);
        vel_linear_delta_w = (1/(4*(a+b)))*(vel_delta[0]-vel_delta[1]-vel_delta[2]+vel_delta[3]);

        position_x = position_x + vel_linear_delta_x*0.001;
        position_y = position_y + vel_linear_delta_y*0.001;
        position_w = position_w + vel_linear_delta_w*0.001;

        std_msgs::Float64MultiArray odom_array_msg;
        odom_array_msg.data.resize(6);
        
        odom_array_msg.data.push_back(position_x);
        odom_array_msg.data.push_back(position_y);
        odom_array_msg.data.push_back(position_w);
        odom_array_msg.data.push_back(vel_linear_x);
        odom_array_msg.data.push_back(vel_linear_y);
        odom_array_msg.data.push_back(vel_linear_w);

        pub.publish(odom_array_msg);
        ROS_INFO("%f %f %f",position_x,position_y,position_w);

        rate.sleep();
    }

}

void vel_callback(const std_msgs::Float64MultiArray::ConstPtr& vel_data)
{
    vel[0] = vel_data->data[0];
    vel[1] = vel_data->data[1];
    vel[2] = vel_data->data[2];
    vel[3] = vel_data->data[3];
}
