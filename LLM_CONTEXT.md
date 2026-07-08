# LLM_CONTEXT.md

> **Version:** 2.0
>
> **Project:** 4ZE Racing Driverless Vehicle
>
> **Purpose:** Entry point for AI assistants working on the Formula Student Driverless codebase.
>
> Read this document before reading any other project documentation.

---

# Purpose

This repository is designed for AI-assisted development of a Formula Student Driverless racecar.

This document serves as the primary entry point for any AI assistant working on the project.

Supported assistants include:

- ChatGPT
- Codex CLI
- Claude Code
- Gemini CLI
- Cursor
- Cline
- Roo Code
- Continue
- Windsurf
- Aider
- Local LLMs

Every AI assistant should read this document before making any modifications.

---

# Project Overview

This repository belongs to **4ZE Racing**.

The project converts an existing Formula Student Electric vehicle into a fully autonomous racecar compliant with modern Formula Student Driverless competitions.

The manual EV platform is assumed to be complete.

Current work focuses exclusively on autonomous systems.

---

# Project Goals

The primary objectives are:

- Pass all Driverless technical inspections
- Complete autonomous dynamic events
- Build a safe and reliable software stack
- Build a maintainable codebase for future team members
- Produce complete technical documentation
- Maintain Formula Student rule compliance

---

# Engineering Priorities

Always prioritize, in order:

1. Safety
2. Rule Compliance
3. Reliability
4. Determinism
5. Maintainability
6. Simplicity
7. Performance

Performance should never compromise safety.

---

# Primary References

When making engineering decisions, use the following priority:

1. Formula Student Rules
2. Formula Bharat Rules
3. Formula Student East ASF
4. Datasheets
5. ROS2 Documentation
6. Linux Documentation
7. Existing Project Documentation

If documentation conflicts, ask before making assumptions.

---

# Documentation Hierarchy

Read documentation in the following order.

---

## Level 1 — Project Context

Always read these first.

```
LLM_CONTEXT.md

README.md

PROJECT_CONTEXT.md

AI_INSTRUCTIONS.md

CHANGELOG_AI.md
```

---

## Level 2 — Technical Documentation

Read only documentation relevant to the task.

```
docs/

architecture.md

software_architecture.md

hardware_architecture.md

ros2.md

can.md

vehicle_interface.md

perception.md

mapping.md

planning.md

control.md

localization.md

simulation.md

safety.md

ebs.md

steering.md

sensors.md

testing.md

deployment.md

coding_standards.md

development_workflow.md

rule_compliance.md

roadmap.md
```

---

## Level 3 — Source Code

Understand the implementation before making changes.

```
src/

firmware/

hardware/

simulation/

launch/

config/

scripts/

tests/
```

Never assume implementation details.

Read the code first.

---

# Repository Structure

```
README.md

LICENSE

LLM_CONTEXT.md

PROJECT_CONTEXT.md

AI_INSTRUCTIONS.md

CHANGELOG_AI.md

docs/

src/

firmware/

hardware/

simulation/

launch/

config/

scripts/

tests/

tools/

assets/
```

---

# Autonomous System Overview

High-level pipeline:

```
Sensors

↓

Sensor Drivers

↓

Sensor Fusion

↓

Perception

↓

Mapping

↓

Localization

↓

Planning

↓

Trajectory Generation

↓

Controller

↓

Vehicle Interface

↓

CAN

↓

Actuators
```

---

# Expected ROS2 Architecture

Major systems should exist as independent ROS2 nodes.

Typical nodes include:

- camera drivers
- lidar drivers
- imu driver
- gps driver
- perception
- localization
- mapping
- planning
- trajectory generation
- controller
- vehicle interface
- diagnostics
- logging
- visualization

Communication should occur only through ROS interfaces.

Avoid direct coupling.

---

# CAN Philosophy

All actuator commands ultimately become CAN messages.

Never bypass the CAN abstraction layer.

CAN IDs should:

- be centralized
- be documented
- never duplicated
- never hardcoded throughout the project

---

# State Machine

All vehicle behavior must follow an explicit state machine.

Typical states:

```
OFF

↓

READY

↓

DRIVING

↓

FINISHED

↓

EMERGENCY

↓

FAULT
```

Every transition must be documented.

---

# Functional Safety

Safety-critical software must:

- validate every input
- detect stale data
- detect communication timeout
- validate sensor ranges
- detect impossible values
- detect watchdog failures
- transition to a safe state on failure

Never assume incoming data is valid.

---

# Before Every Task

Always perform the following.

1. Read LLM_CONTEXT.md.
2. Read project documentation.
3. Read relevant technical documentation.
4. Inspect existing implementation.
5. Explain your understanding.
6. State assumptions.
7. Identify risks.
8. Create an implementation plan.
9. Implement incrementally.
10. Verify functionality.
11. Update documentation if required.
12. Update CHANGELOG_AI.md.

---

# Planning Before Coding

Before implementation, always explain:

- Understanding of the task
- Assumptions
- Safety implications
- Formula Student rule implications
- Files that will change
- Verification strategy

Do not immediately begin coding.

---

# Engineering Philosophy

Prefer:

- incremental improvements
- modular architecture
- deterministic execution
- readable code
- reusable components
- hardware abstraction
- explicit state machines
- composition over inheritance
- strongly typed interfaces

Avoid:

- large rewrites
- premature optimization
- duplicated logic
- unnecessary abstractions
- deeply nested code
- global mutable state
- hidden side effects
- clever code

---

# Code Modification Rules

Only modify files required for the requested task.

Do not:

- reformat unrelated files
- rename unrelated symbols
- refactor unrelated modules
- delete unrelated code
- modify CAN IDs without explanation
- modify ROS interfaces without explanation
- modify safety-critical logic without documenting why

Every changed line should directly relate to the requested task.

---

# Coding Standards

Prefer:

- descriptive names
- small functions
- const correctness
- RAII (C++)
- strong typing
- explicit interfaces
- dependency injection where appropriate

Avoid:

- magic numbers
- duplicated code
- hidden dependencies
- overly complex templates
- unnecessary macros

---

# Error Handling

Every subsystem should:

- detect failures
- report failures
- degrade safely
- avoid silent failure

Critical failures should transition the vehicle into a safe state.

---

# Timing

Control loops should be deterministic.

Avoid:

```
sleep()
```

Prefer:

- ROS timers
- steady clocks
- fixed-rate execution

---

# Logging

Every subsystem should log:

- startup
- shutdown
- warnings
- errors
- state transitions
- watchdog failures
- emergency events
- actuator commands (when appropriate)

---

# Diagnostics

Every subsystem should expose:

- heartbeat
- health
- software version
- diagnostics
- status
- runtime statistics

---

# Hardware Abstraction

Business logic should never directly access hardware.

Always use abstraction layers for:

- CAN
- GPIO
- Sensors
- Actuators
- Vehicle Interface

---

# Testing Philosophy

Every feature should have:

- Unit Tests
- Integration Tests
- Simulation Tests
- Hardware Tests
- Vehicle Tests

Regression testing should be performed before deployment.

---

# Verification

Every completed task should verify:

- existing functionality preserved
- build succeeds
- tests pass
- documentation updated
- no duplicated logic introduced
- coding standards followed
- rule compliance maintained
- safety preserved

---

# Simulation

Simulation changes should support:

- Gazebo
- FSDS (if applicable)
- ROS bag playback
- Recorded sensor datasets

Simulation should remain as close as possible to real vehicle behavior.

---

# Documentation

Every module should document:

- Purpose
- Inputs
- Outputs
- Dependencies
- Failure Modes
- Safety Considerations
- Formula Student Rule References (if applicable)

---

# Formula Student Context

Assume the following systems are already complete:

- Chassis
- Suspension
- Powertrain
- High Voltage System
- Low Voltage System
- Battery Pack
- BMS
- Manual Steering
- Manual Braking
- Manual Vehicle Controls

Current development concerns autonomous systems only.

---

# ASF Integration

Every autonomous subsystem should eventually map to the Autonomous System Form.

Relevant ASF sections include:

- System Overview
- Autonomous Architecture
- State Machine
- Emergency Brake System
- Steering System
- ASSI
- Wiring Diagrams
- Functional Safety
- Critical Signals
- Hardwired Logic
- Safety Analysis
- Appendices

Design documentation should be written so it can later be inserted directly into the ASF.

---

# Working With Tasks

Before implementation:

- Understand the request.
- Inspect existing implementation.
- Identify dependencies.
- Identify affected ROS nodes.
- Identify affected CAN interfaces.
- Identify affected hardware.
- Explain implementation approach.

After implementation:

- Verify functionality.
- Verify safety.
- Verify rule compliance.
- Update documentation.
- Update CHANGELOG_AI.md.

---

# Working With Issues

If requirements are ambiguous:

Ask.

Do not guess.

If multiple solutions exist:

Explain trade-offs.

Choose the simplest maintainable solution.

---

# AI Guidelines

Think before coding.

Do not invent:

- hardware specifications
- CAN IDs
- ROS topics
- message definitions
- wiring diagrams
- electrical interfaces
- Formula Student rules
- safety mechanisms

If required information is missing:

Stop and ask.

Prefer explicit code over clever code.

Avoid overengineering.

---

# Expected Response Format

When implementing changes:

1. Summarize your understanding.
2. State assumptions.
3. Explain the implementation plan.
4. Implement incrementally.
5. Explain verification.
6. Mention safety implications.
7. Suggest improvements if appropriate.

---

# Git Workflow

Prefer:

- feature branches
- small commits
- descriptive commit messages
- pull requests
- code review before merging

---

# Definition of Done

A task is complete only when:

- implementation finished
- build succeeds
- tests pass
- existing functionality preserved
- documentation updated
- CHANGELOG_AI.md updated
- coding standards followed
- rule compliance maintained
- safety preserved

---

# Final Principle

The objective is not simply to write code.

The objective is to build a reliable, deterministic, safe, maintainable, and competition-ready Formula Student Driverless platform.

Every change should leave the project in a better state while preserving safety, rule compliance, readability, maintainability, and long-term scalability.