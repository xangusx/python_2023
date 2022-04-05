#include "ros/ros.h"
#include <geometry_msgs/Twist.h>
#include "std_msgs/MultiArrayLayout.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/Float64MultiArray.h"
#include <iostream>
#include <math.h>
#include <vector>

typedef struct position position;
struct position{
    float x;
    float y;
};

float distance(float a,float b);
void position_callback(const std_msgs::Float64MultiArray::ConstPtr& odom_data);

float position_x=0.0;
float position_y=0.0;
float position_w=0.0;
float vel_linear_x=0.0;
float vel_linear_y=0.0;
float vel_linear_w=0.0;

int main(int argc,char **argv)
{
    ros::init(argc, argv, "chassis_controll");
    ros::NodeHandle nh;
    ros::Publisher pub = nh.advertise<std_msgs::Float64MultiArray>("vel_array",1);
    ros::Subscriber sub = nh.subscribe("odom_data", 1, position_callback);
    geometry_msgs::Twist vel;
    float a;//mm
    float b;//mm
    float p;
    float vel_rpm[4];
    int index=0;
    int x[2]={0,100};
    int y[2]={100,0};
    while(ros::ok())
    {
        ros::spinOnce();
        position initial = {
        .x = position_x ,
        .y = position_y
        };
        position target = {
                .x = x[index]-initial.x ,
                .y = y[index]-initial.y
            };
        float d = distance(target.x,target.y);
        if(d<10)
            index++;
        else
            p = d/0.05;
        vel.linear.x = target.x/p;
        vel.linear.y = target.y/p;
        vel.angular.z = 0;

        std_msgs::Float64MultiArray vel_array_msg;
        vel_array_msg.data.resize(4);

        vel_rpm[0] = vel.linear.y - vel.linear.x + vel.angular.z*(a+b);
        vel_rpm[1] = vel.linear.y + vel.linear.x - vel.angular.z*(a+b);
        vel_rpm[2] = vel.linear.y - vel.linear.x - vel.angular.z*(a+b);
        vel_rpm[3] = vel.linear.y + vel.linear.x + vel.angular.z*(a+b);

        for(int i=0;i<4;i++)
            vel_array_msg.data.push_back(vel_rpm[i]);   
        
        pub.publish(vel_array_msg);
        ROS_INFO("I published something![%d]",index);
    }
    
}

float distance(float a,float b)
{
    float distance = sqrt(a*a+b*b);
        return distance;
}

void position_callback(const std_msgs::Float64MultiArray::ConstPtr& odom_data)
{
    /*std::vector<float>::const_iterator it = odom_data->data.begin();
    position_x = *it;
    position_y = *(it+1);
    position_w = *(it+2);
    vel_linear_x = *(it+3);
    vel_linear_y = *(it+4);
    vel_linear_w = *(it+5);*/
    position_x = odom_data->data[0];
    position_y = odom_data->data[1];
    position_w = odom_data->data[2];
    vel_linear_x = odom_data->data[3];
    vel_linear_y = odom_data->data[4];
    vel_linear_w = odom_data->data[5];
}