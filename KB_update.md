# 4ZE Racing Driverless System Knowledge Base

Version: 2.0

Date: June 2026

---

# Project Overview

## Objective

Develop a Formula Student Driverless autonomous system capable of navigating a cone-defined race track without human intervention.

Target milestones:

* Simulated closed-loop autonomy by July 2026
* Real perception stack by August 2026
* Jetson deployment by September 2026
* Real vehicle integration by October 2026
* Autonomous testing and validation by November 2026

---

# Vehicle Manufacturing Status

Current Stage:

Vehicle under development.

Completed:

* Vehicle architecture definition
* EV system design
* Autonomous system architecture
* Initial ROS2 software stack
* Hardware selection studies

In Progress:

* EV subsystem development
* Autonomous software development

Not Yet Started:

* Full vehicle manufacturing
* Autonomous hardware integration
* Vehicle-level autonomous validation

---

# Development Philosophy

## Core Principle

Build the autonomy stack independently from any simulator or hardware platform.

Benefits:

* Easier testing
* Easier deployment
* Better maintainability
* Reduced vendor lock-in

---

# Simulator Strategy

## Rejected

Formula Student Driverless Simulator (FSDS)

Reasons:

* No major updates in several years
* ROS2 compatibility issues
* Unreal Engine dependency problems
* High maintenance effort

## Selected

Gazebo

Reasons:

* Native ROS2 integration
* Existing physics engine
* Existing sensor plugins
* Active ecosystem

---

# Software Stack

Development:

* Windows 11
* WSL2 Ubuntu
* VSCode
* ROS2 Humble
* GitHub

Future:

* Docker
* Jetson Orin Nano Super

---

# High-Level Autonomous Pipeline

Camera + LiDAR + IMU

↓

Perception

↓

Localization

↓

Mapping

↓

Planning

↓

Control

↓

Vehicle Interface

↓

Vehicle

---

# Formula Bharat Safety Layer

The following systems supervise the autonomous pipeline:

* Mission Manager
* State Machine Manager
* Safety Supervisor
* EBS
* RES
* ASSI
* AMI
* ASMS
* SCS Monitoring

These systems do not replace the autonomous pipeline.

They supervise and protect it.

---

# Complete Autonomous Architecture

Mission Selector (AMI)

↓

State Machine Manager

↓

Safety Supervisor

↓

Perception

↓

Localization

↓

Mapping

↓

Planning

↓

Control

↓

Vehicle Interface

↓

Steering / Brake / Propulsion

Parallel Systems:

* RES
* ASSI Controller
* EBS
* ASMS
* SCS Monitor

---

# Current Development Status

Completed:

* Custom ROS interfaces
* Perception node (mock)
* Mapping node
* Planning node
* Control node
* Localization node

In Progress:

* Closed-loop feedback integration

Planned:

* RViz
* Bicycle model
* PID controller
* Gazebo integration
* YOLOv8
* Sensor fusion
* Jetson deployment

---

# Workspace Layout

av_ws/

├── av_interfaces

├── perception

├── localization

├── mapping

├── planning

└── control

---

# Message Definitions

## Cone.msg

Fields:

* x
* y
* color

Purpose:

Detected cone.

---

## ConeArray.msg

Purpose:

Collection of detected cones.

Publisher:

perception_node

Subscriber:

mapping_node

---

## Track.msg

Fields:

* left_cones
* right_cones

Purpose:

Track boundaries.

Publisher:

mapping_node

Subscriber:

planning_node

---

## Path.msg

Fields:

* geometry_msgs/Point[] points

Purpose:

Driveable path.

Publisher:

planning_node

Subscriber:

control_node

---

## Control.msg

Fields:

* steering
* throttle

Purpose:

Vehicle commands.

Publisher:

control_node

Subscriber:

vehicle_interface

---

## Pose2D.msg

Fields:

* x
* y
* yaw
* velocity

Purpose:

Vehicle state.

Publisher:

localization_node

Subscribers:

control_node

---

# Topic Graph

/perception/cones

↓

mapping_node

↓

/mapping/track

↓

planning_node

↓

/planning/path

↓

control_node

↓

/control/cmd

↓

vehicle_interface

↑

/localization/pose

↑

localization_node

---

# Node Documentation

## Perception Node

Current:

Mock cone detections.

Future:

YOLOv8 cone detection.

---

## Localization Node

Current:

Simple motion integration.

Future:

Bicycle model
EKF
Sensor fusion

---

## Mapping Node

Current:

Color separation and sorting.

Future:

Track memory
Cone association

---

## Planning Node

Current:

Midpoint planner.

Future:

Spline planner

---

## Control Node

Current:

Pure Pursuit

Future:

PID speed control

---

## Vehicle Interface Node

Purpose:

Bridge ROS2 stack and vehicle hardware.

Inputs:

* Steering command
* Throttle command

Outputs:

* CAN commands
* Steering actuator
* Brake actuator

---

# Formula Bharat State Machine

## AS Off

Conditions:

* ASMS OFF

ASSI:

* OFF

---

## AS Ready

Conditions:

* Mission selected
* EBS healthy
* Sensors healthy
* ASMS ON

ASSI:

* Yellow Solid

Requirement:

Remain in this state for at least 5 seconds before entering AS Driving.

---

## AS Driving

Conditions:

* RES GO command received

ASSI:

* Yellow Flashing

Requirement:

Remain in this state for at least 3 seconds before vehicle motion.

---

## AS Emergency

Entered when:

* RES stop command
* EBS trigger
* Critical fault
* Safety supervisor request

ASSI:

* Blue Flashing

Actions:

* Disable propulsion
* Activate emergency braking

---

## AS Finished

Mission complete.

ASSI:

* Blue Solid

Vehicle stationary.

---

# Mission Manager

Supported Missions:

* Manual Driving
* Inspection
* EBS Test
* Acceleration
* Skidpad
* Autocross
* Trackdrive

---

# Autonomous Mission Indicator (AMI)

Purpose:

Display selected mission.

Possible Hardware:

* Rotary switch
* ESP32
* OLED display

Displayed:

* Manual
* Inspection
* EBS Test
* Acceleration
* Skidpad
* Autocross
* Trackdrive

---

# Autonomous System Status Indicator (ASSI)

Required:

Three indicators.

Locations:

* Left side
* Right side
* Rear

Status Table:

AS Off = Off

AS Ready = Yellow Solid

AS Driving = Yellow Flashing

AS Emergency = Blue Flashing

AS Finished = Blue Solid

Recommended Controller:

Dedicated ESP32

---

# Autonomous System Master Switch (ASMS)

Purpose:

Enable autonomous actuation.

When OFF:

* Steering disabled
* Brake actuation disabled
* Autonomous propulsion disabled

Allowed:

* Sensors active
* Jetson active
* ROS network active

Manual driving must remain possible.

---

# Remote Emergency System (RES)

Functions:

* GO command
* Emergency stop

GO:

AS Ready → AS Driving

Emergency Stop:

Any State → AS Emergency

---

# Safety Supervisor

Responsibilities:

* Monitor perception health
* Monitor localization health
* Monitor CAN communication
* Monitor sensor timeouts
* Monitor state machine validity
* Monitor Jetson health

Outputs:

Healthy:

* System OK

Fault:

* Emergency Stop Request

---

# System Critical Signals (SCS)

Each critical signal must define:

* Signal name
* Source
* Destination
* Failure detection
* Safe state

Examples:

* Steering encoder
* Localization pose
* Brake pressure
* CAN commands
* Mission selector
* ASSI state
* EBS status

---

# Emergency Brake System (EBS)

Purpose:

Safely stop the vehicle after faults.

Trigger Conditions:

* RES stop
* Power failure
* Localization failure
* Perception failure
* CAN failure
* Jetson failure
* State machine failure

Sequence:

Fault

↓

Safety Supervisor

↓

AS Emergency

↓

Torque Disabled

↓

EBS Activated

↓

Vehicle Stops

---

# Hardware Decisions

## Compute

Selected:

Jetson Orin Nano Super

Minimum:

8GB RAM

Reason:

Best performance-to-cost ratio for embedded AI.

---

## Development Platform

Selected:

Windows + WSL2 + Docker

---

## Camera

Candidates:

* ZED 2i
* OAK-D
* Intel RealSense

Status:

Not finalized

---

## LiDAR

Status:

Not finalized

Purpose:

Cone detection and localization

---

## GNSS

Candidate:

u-blox ZED-F9P RTK

Purpose:

Global positioning

---

## IMU

Requirements:

* ROS2 support
* High update rate

Preferred:

Industrial CAN-enabled IMU

---

## Networking

Vehicle CAN Bus

Architecture:

ROS2 ↔ Vehicle Interface ↔ CAN Network

---

# Development Roadmap

## June 2026

Goals:

* Localization node
* Pose feedback
* RViz
* Bicycle model
* PID fundamentals

Deliverable:

Closed-loop autonomy stack

---

## July 2026

Goals:

* Gazebo setup
* Vehicle model
* Cone world
* Simulated sensors

Deliverable:

Autonomous operation in simulation

---

## August 2026

Goals:

* Camera pipeline
* YOLOv8
* LiDAR processing
* Sensor fusion

Deliverable:

Perception-based autonomy

---

## September 2026

Goals:

* Jetson deployment
* Docker
* TensorRT
* Runtime optimization

Deliverable:

Embedded deployment

---

## October 2026

Goals:

* Vehicle integration
* CAN interface
* Calibration
* Initial autonomous testing

Deliverable:

First autonomous vehicle operation

---

## November 2026

Goals:

* Reliability
* Validation
* Performance tuning

Deliverable:

Competition-ready driverless system

---

# Learning Notes

## ROS2

Topics:

* Nodes
* Publishers
* Subscribers
* Interfaces
* Services

---

## tf2

Learn:

* map
* base_link
* sensor frames

---

## Pure Pursuit

Inputs:

* Vehicle pose
* Path

Output:

* Steering angle

---

## PID

Purpose:

Speed control

Terms:

* P
* I
* D

---

## Bicycle Model

Learn:

* Wheelbase
* Steering angle
* Yaw rate

Purpose:

Vehicle dynamics

---

## Gazebo

Purpose:

Simulation and testing

---

## YOLOv8

Pipeline:

Camera

↓

YOLO

↓

ConeArray

---

## Sensor Fusion

Combine:

* Camera
* LiDAR
* IMU
* RTK GNSS

Goal:

Reliable localization and perception

# Additional System Engineering Documentation

---

# Autonomous Hardware Block Diagram

```text
                    Jetson Orin Nano
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
      Camera             LiDAR               RTK GNSS
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                           IMU
                            │
                            ▼
                      ROS2 Network
                            │
                            ▼
                     Vehicle Interface
                            │
                         CAN Bus
                            │
        ┌───────────┬───────────┬───────────┬───────────┐
        ▼           ▼           ▼           ▼
      VCU      Steering     Brake       ASSI/AMI
                ECU          ECU       Controller
```

---

# Vehicle CAN Architecture

## Purpose

Provide deterministic communication between autonomous subsystems and vehicle hardware.

---

## CAN Nodes

### Jetson Orin Nano

Responsibilities:

* Perception
* Localization
* Mapping
* Planning
* Control

---

### Vehicle Control Unit (VCU)

Responsibilities:

* CAN gateway
* Safety supervision
* Vehicle interface

---

### Steering Controller

Responsibilities:

* Steering motor control
* Steering feedback

---

### Brake Controller

Responsibilities:

* Brake actuator control
* Brake pressure monitoring

---

### ASSI Controller

Responsibilities:

* State indication

---

### AMI Controller

Responsibilities:

* Mission indication

---

# Planned CAN Messages

## CMD_STEERING

Purpose:

Steering command.

Rate:

50 Hz

Source:

Control Node

Destination:

Steering Controller

---

## CMD_TORQUE

Purpose:

Torque request.

Rate:

50 Hz

Source:

Control Node

Destination:

VCU

---

## BRAKE_REQUEST

Purpose:

Brake actuation request.

Rate:

50 Hz

Source:

Safety Supervisor

Destination:

Brake Controller

---

## VEHICLE_STATE

Purpose:

Vehicle telemetry.

Rate:

100 Hz

Source:

VCU

Destination:

Jetson

---

## EBS_STATUS

Purpose:

Emergency brake status.

Rate:

20 Hz

Source:

Brake Controller

Destination:

Safety Supervisor

---

# Coordinate Frames

## map

Global track reference frame.

Purpose:

Global localization.

---

## odom

Continuous local frame.

Purpose:

Vehicle motion estimation.

---

## base_link

Vehicle center reference frame.

Purpose:

Vehicle control calculations.

---

## camera_link

Camera coordinate frame.

Purpose:

Cone detection.

---

## lidar_link

LiDAR coordinate frame.

Purpose:

Point cloud processing.

---

## imu_link

IMU coordinate frame.

Purpose:

Orientation estimation.

---

# State Transition Table

| Current State | Event            | Next State   |
| ------------- | ---------------- | ------------ |
| AS Off        | ASMS ON          | AS Ready     |
| AS Ready      | Mission Selected | AS Ready     |
| AS Ready      | RES GO           | AS Driving   |
| AS Driving    | Mission Complete | AS Finished  |
| AS Driving    | Fault Detected   | AS Emergency |
| AS Ready      | Fault Detected   | AS Emergency |
| AS Finished   | Reset            | AS Off       |
| Any State     | RES E-Stop       | AS Emergency |
| Any State     | EBS Trigger      | AS Emergency |

---

# Fault Management

## Camera Failure

Detection:

* Camera timeout
* Invalid image stream

Action:

* Enter AS Emergency

---

## LiDAR Failure

Detection:

* Point cloud timeout

Action:

* Enter AS Emergency

---

## GNSS Failure

Detection:

* Invalid RTK solution

Action:

* Continue if localization remains valid

Otherwise:

* Enter AS Emergency

---

## IMU Failure

Detection:

* Missing messages
* Invalid orientation

Action:

* Enter AS Emergency

---

## Localization Failure

Detection:

* Pose timeout
* Invalid position estimate

Action:

* Enter AS Emergency

---

## CAN Timeout

Detection:

* Missing CAN messages

Action:

* Torque request set to zero

---

## Jetson Failure

Detection:

* Watchdog timeout

Action:

* Trigger EBS

---

## Steering Failure

Detection:

* Position mismatch
* Encoder fault

Action:

* Enter AS Emergency

---

## Brake Failure

Detection:

* Pressure mismatch

Action:

* Enter AS Emergency

---

# Steering System Concept

Current Status:

Conceptual design.

---

## Preferred Architecture

Actuator:

* BLDC Motor

Drive Method:

* Chain Drive

Reason:

* Common Formula Student solution
* Easy mechanical packaging
* Allows manual steering

---

## Feedback

Primary Sensor:

* AS5600 Magnetic Encoder

Future Alternative:

* Industrial Absolute Encoder

---

## Controller

ESP32

---

## Communication

CAN Bus

---

## Steering Control Loop

Target Steering Angle

↓

Steering Controller

↓

Motor Driver

↓

Steering Motor

↓

Steering Rack

↓

Steering Encoder

↓

Controller Feedback

---

# Brake System Concept

Current Status:

Conceptual design.

---

## Purpose

Provide autonomous braking capability.

Provide emergency braking capability.

---

## Architecture

Autonomous Brake System (ASB)

contains

Emergency Brake System (EBS)

---

## Planned Actuator

Type:

Linear Actuator

Status:

To be finalized

---

## Energy Storage

Spring-based mechanical energy storage

Reason:

Compliance with EBS requirements

---

## Trigger Methods

* RES Emergency Stop
* EBS Fault
* Power Loss
* Safety Supervisor Request

---

## Manual Override

Required.

Manual braking must remain possible.

---

# ASF Preparation Map

## Chapter 1

System Overview

Sources:

* Hardware Architecture
* Software Architecture

---

## Chapter 2

Autonomous System Implementation

Sources:

* State Machine
* Mission Manager
* Safety Supervisor

---

## Chapter 3

Emergency Brake System

Sources:

* EBS Section
* Fault Management

---

## Chapter 4

Service Brake

Sources:

* Brake System Concept

---

## Chapter 5

Steering System

Sources:

* Steering System Concept

---

## Chapter 6

ASSI Implementation

Sources:

* ASSI Controller
* State Machine

---

## Chapter 7

Additional Autonomous Parts

Sources:

* AMI
* Sensors
* Compute Hardware

---

# Node Specifications

## Perception Node

Inputs:

* Camera
* LiDAR

Outputs:

* ConeArray

Rate:

20 Hz

Failure Modes:

* No detections
* Sensor timeout

Dependencies:

* Camera
* LiDAR

---

## Localization Node

Inputs:

* IMU
* GNSS
* Vehicle State

Outputs:

* Pose2D

Rate:

100 Hz

Failure Modes:

* Pose timeout
* Invalid estimate

Dependencies:

* Sensor Fusion

---

## Mapping Node

Inputs:

* ConeArray

Outputs:

* Track

Rate:

20 Hz

Failure Modes:

* Invalid track generation

Dependencies:

* Perception

---

## Planning Node

Inputs:

* Track

Outputs:

* Path

Rate:

20 Hz

Failure Modes:

* Path generation failure

Dependencies:

* Mapping

---

## Control Node

Inputs:

* Path
* Pose2D

Outputs:

* Control Commands

Rate:

50 Hz

Failure Modes:

* Control divergence

Dependencies:

* Localization
* Planning

---

## Safety Supervisor

Inputs:

* Node health
* Sensor health
* CAN status
* State machine status

Outputs:

* Emergency stop request

Rate:

100 Hz

Failure Modes:

* Watchdog timeout

Dependencies:

* Entire system

---

# Engineering Decision Log

## June 2026

Decision:

ROS2 Humble

Reason:

Stable ecosystem and documentation.

---

Decision:

Gazebo

Rejected:

FSDS

Reason:

FSDS outdated and difficult to maintain.

---

Decision:

Windows + WSL2

Rejected:

Arch Linux Dual Boot

Reason:

Lower maintenance burden.

---

Decision:

Mock Pipeline Before Perception

Reason:

Validate architecture before hardware integration.

---

Decision:

Jetson Orin Nano Super

Reason:

Best balance between performance and cost.

---

Decision:

Chain Drive Steering Actuator

Reason:

Maintains manual steering capability and simplifies integration.

---

Decision:

Dedicated ASSI Controller

Reason:

State indication remains functional even if Jetson crashes.

---

Decision:

Safety-First Architecture

Reason:

Formula Bharat technical inspection focuses heavily on ASMS, ASSI, AMI, RES, EBS, and fault handling before vehicle performance.
