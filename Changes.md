# Changes Log

This file tracks changes made to the contents of the `src/` repository.

## 2026-07-09

### Added

- Established `Changes.md` as the running change log for all future edits within `src/`.
- Created `temp.md` containing detailed design and Python implementation steps for the ROS2 state machine package (`state_machine`).

### Modified

- Added new custom message definitions to `av_interfaces/msg/`: `AutonomousState.msg`, `Mission.msg`, `Heartbeat.msg` (using correct `uint8` types), and `EmergencyStop.msg`.
- Updated `av_interfaces/CMakeLists.txt` and `av_interfaces/package.xml` to include and link `std_msgs` as a dependency for the new message headers.

### Logged Baseline

- Baseline documentation commit recorded at `3dff3aa` with:
- `ENGINEERING_STATE.md`
- `FB2027_Rules_V1.2_02072026.md`
- `LLM_CONTEXT.md`

### Process

- Future modifications to files or folders inside `src/` should be logged here as they are made.
