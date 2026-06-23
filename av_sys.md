# 4ZE Racing Driverless System Architecture Explained

Version: 1.0

Date: June 2026

---

# Purpose of this Document

This document explains the reasoning behind the autonomous system architecture used by 4ZE Racing.

Unlike the main knowledge base, which stores facts, hardware selections, and software structure, this document focuses on:

* Why each subsystem exists
* How subsystems interact
* Formula Bharat Driverless requirements
* Safety philosophy
* Future development direction

---

# System Philosophy

The autonomous system is designed around three principles:

1. Safety
2. Modularity
3. Competition Compliance

The objective is not simply to drive a vehicle autonomously.

The objective is to build a Formula Bharat compliant autonomous vehicle that can pass technical inspection and safely complete dynamic events.

---

# High Level System View

The autonomous vehicle can be divided into two major layers.

Layer 1:

Autonomous Intelligence

Layer 2:

Safety and Compliance

---

# Layer 1 - Autonomous Intelligence

This layer is responsible for understanding the environment and controlling the vehicle.

Pipeline:

Sensors

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

Vehicle

---

# Sensors

Purpose:

Observe the environment and provide data to the software stack.

Planned Sensors:

* Camera
* LiDAR
* IMU
* RTK GNSS

The sensors themselves do not make decisions.

They only provide information.

---

# Perception

Purpose:

Understand what exists around the vehicle.

Inputs:

* Camera images
* LiDAR data

Outputs:

* Cone positions
* Cone colors

Current State:

Mock cone generation.

Future State:

YOLOv8 cone detection.

---

# Localization

Purpose:

Determine where the vehicle currently is.

Inputs:

* IMU
* GNSS
* Vehicle motion

Outputs:

* Vehicle position
* Vehicle orientation
* Vehicle velocity

Localization answers:

"Where am I?"

---

# Mapping

Purpose:

Convert individual cone detections into a usable track representation.

Inputs:

* Cone detections

Outputs:

* Track boundaries

Mapping answers:

"What does the track look like?"

---

# Planning

Purpose:

Generate a path through the track.

Inputs:

* Track boundaries

Outputs:

* Target trajectory

Planning answers:

"Where should I go?"

---

# Control

Purpose:

Follow the planned trajectory.

Inputs:

* Vehicle pose
* Planned path

Outputs:

* Steering commands
* Torque requests

Control answers:

"How should I move?"

---

# Vehicle Interface

Purpose:

Convert software commands into real vehicle actions.

Inputs:

* Steering request
* Torque request

Outputs:

* CAN messages
* Steering actuator commands
* Brake actuator commands

The vehicle interface separates software from hardware.

This allows the software stack to remain unchanged even if vehicle hardware changes.

---

# Layer 2 - Safety and Compliance

Formula Bharat Driverless is primarily a safety challenge.

The following systems exist specifically to satisfy competition requirements.

* State Machine
* EBS
* RES
* ASSI
* AMI
* ASMS
* Safety Supervisor

---

# State Machine

Purpose:

Control all operating modes of the autonomous vehicle.

The state machine is the highest authority in the system.

No subsystem is allowed to bypass it.

States:

* AS Off
* AS Ready
* AS Driving
* AS Emergency
* AS Finished

All autonomous operation occurs through these states.

---

# AS Off

Vehicle not operating autonomously.

Characteristics:

* Autonomous actuation disabled
* Manual driving allowed
* ASSI off

---

# AS Ready

Vehicle prepared for autonomous operation.

Requirements:

* Mission selected
* Sensors healthy
* EBS healthy
* Safety checks passed

ASSI:

Yellow solid

The vehicle must remain in this state for at least five seconds before autonomous driving can begin.

---

# AS Driving

Autonomous mission active.

ASSI:

Yellow flashing

The vehicle may only begin moving after remaining in this state for three seconds.

---

# AS Emergency

Safety state.

Entered when:

* Critical fault occurs
* EBS activates
* RES emergency stop activated
* Safety supervisor requests stop

ASSI:

Blue flashing

Actions:

* Remove propulsion
* Activate emergency braking

---

# AS Finished

Mission completed successfully.

ASSI:

Blue solid

Vehicle remains stationary.

---

# Emergency Brake System (EBS)

Purpose:

Guarantee vehicle stopping even during severe failures.

The EBS is the final safety mechanism.

It exists independently of normal vehicle control.

The EBS must stop the vehicle when:

* Compute fails
* Sensors fail
* Communications fail
* Power fails

The EBS is considered more important than perception, planning, or control.

Without a compliant EBS the vehicle cannot compete.

---

# Remote Emergency System (RES)

Purpose:

Allow officials to start and stop autonomous operation remotely.

Functions:

* GO
* Emergency Stop

GO:

Transitions vehicle into autonomous operation.

Emergency Stop:

Forces transition into AS Emergency.

---

# Autonomous System Master Switch (ASMS)

Purpose:

Enable or disable autonomous actuation.

When OFF:

* Steering actuation disabled
* Brake actuation disabled
* Autonomous propulsion disabled

Sensors and computing may remain active.

Manual driving must always remain possible.

---

# Autonomous System Status Indicator (ASSI)

Purpose:

Communicate autonomous status to officials.

States:

Off

Yellow Solid

Yellow Flashing

Blue Flashing

Blue Solid

The ASSI provides visual confirmation of the current autonomous state.

---

# Autonomous Mission Indicator (AMI)

Purpose:

Display the selected autonomous mission.

Supported Missions:

* Manual Driving
* Inspection
* EBS Test
* Acceleration
* Skidpad
* Autocross
* Trackdrive

The AMI allows officials to verify the active mission before operation.

---

# Safety Supervisor

Purpose:

Monitor overall system health.

Responsibilities:

* Sensor monitoring
* Node monitoring
* CAN monitoring
* State machine monitoring
* Fault detection

If a critical failure occurs:

Safety Supervisor

↓

AS Emergency

↓

EBS

↓

Vehicle Stop

---

# System Critical Signals

Formula Bharat requires monitoring of critical signals.

Examples:

* Steering encoder
* Brake pressure
* Localization output
* CAN communication
* Mission selection

Each signal must define:

* Source
* Destination
* Failure detection method
* Safe state

---

# Steering System Concept

Current Preferred Design:

Chain driven steering actuator.

Reasoning:

* Common Formula Student solution
* Compact packaging
* Easier manual steering compliance

Feedback Sensor:

AS5600 magnetic encoder.

Controller:

ESP32.

Communication:

CAN Bus.

---

# Brake System Concept

Purpose:

Provide autonomous braking and emergency braking.

Current Concept:

Spring-assisted EBS with actuator controlled release.

Requirements:

* Manual braking always possible
* Autonomous braking possible
* Emergency braking possible

---

# Why ROS2 Was Selected

Reasons:

* Industry standard robotics middleware
* Excellent modularity
* Large ecosystem
* Native support for distributed systems

ROS2 allows every subsystem to be developed independently.

---

# Why Gazebo Was Selected

FSDS was evaluated and rejected.

Reasons:

* Outdated ecosystem
* Maintenance concerns
* ROS2 difficulties

Gazebo was selected because:

* Active development
* ROS2 integration
* Existing sensor models
* Easier long-term maintenance

---

# Why Jetson Orin Nano Was Selected

Requirements:

* Embedded deployment
* AI acceleration
* CUDA support

The Jetson Orin Nano provides sufficient performance for:

* YOLOv8
* Sensor fusion
* Planning
* Control

while remaining affordable.

---

# Future Evolution

Current Stage:

Architecture validation.

Next Stage:

Simulation validation.

Then:

Sensor integration.

Then:

Vehicle integration.

Finally:

Competition preparation.

The architecture is intentionally modular so that future sensors, controllers, and algorithms can be replaced without redesigning the entire system.

---

# Key Takeaway

The autonomous vehicle is not a single program.

It is a collection of interacting subsystems.

The driving stack:

Perception

↓

Localization

↓

Mapping

↓

Planning

↓

Control

creates vehicle motion.

The safety stack:

State Machine

↓

Safety Supervisor

↓

EBS

prevents unsafe vehicle behavior.

Both systems are equally important for a successful Formula Bharat Driverless vehicle.
