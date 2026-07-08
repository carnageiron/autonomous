# 4ZE Racing Driverless Engineering State

Version: 1.0

Last Updated: 2026-07-04

---

# Purpose

This file is the running engineering memory for the current codebase.

It should be updated whenever:

- a design decision is made
- an earlier assumption is disproven
- the implementation phase changes
- a new subsystem is added
- safety or rule-compliance conclusions change
- important codebase changes are made

This file is intended to stay shorter and more operational than the broader knowledge-base documents.

Primary references for larger context remain:

- `LLM_CONTEXT.md`
- `KB_update.md`
- `av_sys.md`
- `FB2027_Rules_V1.2_02072026.md`

---

# Current High-Confidence Conclusions

## Project Position

The repository is currently in a working mock autonomy phase, not a competition-ready driverless phase.

The software stack has moved beyond planning-only documentation and now contains a runnable end-to-end ROS2 pipeline with:

- mock perception
- mapping
- planning
- control
- localization
- custom interfaces

However, the Formula Bharat driverless safety/compliance layer described in the documentation does not yet exist in code as a proper implementation.

---

## Current Development Phase Assessment

### Completed or Mostly Completed

1. Architecture definition
2. Custom ROS2 interface definition
3. Mock pipeline validation
4. Basic closed-loop autonomy in software-only form

### Not Yet Completed

1. Formula Bharat safety-state-machine implementation
2. Safety supervisor implementation
3. Mission manager / AMI logic in code
4. ASSI / ASMS / RES / EBS integration in code
5. Vehicle interface package
6. Gazebo-based vehicle simulation
7. Real perception stack
8. Embedded deployment
9. Real vehicle integration
10. Competition-oriented system validation

---

# Current Codebase Reality

## Confirmed ROS2 Packages Present

- `av_interfaces`
- `perception`
- `mapping`
- `planning`
- `control`
- `localization`

## Confirmed Missing Package Areas

The following are described in documentation but do not currently exist as real packages/modules in `src/`:

- safety supervisor package
- state machine package
- mission manager package
- vehicle interface package
- launch package
- simulation package
- dedicated diagnostics package

---

## Confirmed Implemented Pipeline

Current implemented topic flow:

`/perception/cones`

-> `/mapping/track`

-> `/planning/path`

-> `/control/cmd`

-> `/localization/pose`

This is a mock/prototype flow, not a hardware or competition control architecture.

---

## Node Behavior Summary

### Perception

- publishes fake blue and yellow cones
- no camera input
- no LiDAR input
- no real detection logic

### Mapping

- transforms local cones into global coordinates using current pose
- separates cones by color
- sorts cones by x-coordinate
- publishes RViz markers

### Planning

- forms a midpoint path between left and right cones
- publishes a simple path
- publishes RViz path visualization

### Control

- uses Pure Pursuit for steering
- uses PID-style speed control for throttle
- publishes `Control` messages

### Localization

- uses a kinematic bicycle model
- updates pose from commanded control
- publishes `Pose2D`
- broadcasts `odom -> base_link`

---

# Verification Already Performed

## Workspace Inspection

The actual workspace contents were inspected and compared against:

- `KB_update.md`
- `av_sys.md`
- `FB2027_Rules_V1.2_02072026.md`

## Runtime Verification

`run_system_tests.py` was executed successfully on 2026-07-04 with `ROS_LOG_DIR` redirected into the workspace due home-directory logging restrictions in the environment.

Observed result:

- unit tests passed
- integration test passed
- end-to-end ROS2 mock stack ran successfully
- vehicle displacement during test was about `14.26 m`

Conclusion:

The mock closed-loop software stack is runnable and not merely aspirational documentation.

---

# Most Important Current Gap

The biggest gap between documentation and implementation is the absence of the safety/compliance layer required for Formula Bharat Driverless operation.

This includes the lack of implemented:

- AS state machine
- autonomous mission selection logic
- safety supervisor
- watchdog/fault management layer
- ASSI behavior
- ASMS gating logic
- RES integration logic
- EBS/ASB control path
- SCS monitoring architecture

This means the codebase currently demonstrates autonomy-pipeline behavior, but not driverless competition architecture.

---

# Current Recommendation

The next major implementation step should be:

## Build the Formula Bharat safety/compliance skeleton before deeper perception work

Recommended order:

1. Define ROS interfaces for autonomous state, mission selection, health, and emergency stop
2. Implement a state machine package
3. Implement a safety supervisor package
4. Gate the existing control pipeline through the safety layer
5. Make the mock pipeline run under explicit autonomous states
6. Then move into Gazebo-based simulation

Reason:

The current autonomy stack proves software flow, but Formula Bharat driverless success depends first on safe state handling, autonomous start/stop behavior, and inspectable system logic.

---

# Known Technical Issues

## Package Metadata

Several packages still contain placeholder metadata:

- `TODO` descriptions
- `TODO` license fields

## Dependency Declarations

Some package manifests do not yet declare all runtime dependencies implied by the source code.

This should be cleaned up before the stack grows further.

## Interface Simplicity

Current message set is sufficient for the mock pipeline but too small for the eventual safety and vehicle architecture.

Examples of likely future interface needs:

- autonomous state message
- mission selection message
- health/heartbeat message
- emergency stop message
- brake request message
- vehicle state / actuator feedback messages

---

# Decisions Confirmed So Far

## Confirmed Architectural Decisions

- ROS2 Humble is the current middleware baseline
- custom interfaces are being used for the core mock autonomy chain
- Gazebo is the intended simulator direction, not FSDS
- the current pipeline should remain modular
- business logic should remain separate from hardware details
- Formula Bharat compliance must drive the safety architecture

## Confirmed Practical Decision

The repository's real implementation state must always be checked against code, not assumed from design documents alone.

This has already proven important because the docs describe a larger intended system than what is currently implemented.

---

# Open Questions

These items are still unresolved from actual implementation perspective:

- exact package breakdown for state machine and safety supervisor
- final AMI/ASSI controller architecture
- real vehicle interface package boundaries
- actual CAN message definitions
- real EBS actuation and release strategy in code
- final sensor set and drivers
- Gazebo world and vehicle model structure

---

# Update Log

## 2026-07-04

- Created this file as the running engineering state record
- Confirmed current codebase is a working mock closed-loop ROS2 stack
- Confirmed safety/compliance architecture exists in docs but not yet in implementation
- Confirmed next major implementation priority should be state machine + safety supervisor + safety-gated control flow

---

# Update Rule

Whenever a meaningful code or architecture change is made, append a dated note to `Update Log` and revise any affected sections above instead of only adding a new note.
