# Execution Controller Design

**Status**: ✅ CURRENT
**Task**: ibdm-150
**Created**: 2025-11-20

## Overview

The ExecutionController abstracts execution flow control for IBDM demos and scenarios. It provides a reusable component that supports different execution modes (step-by-step, automatic, replay) without duplicating logic across multiple demo types.

## Problem Statement

Currently, execution control is duplicated across demo implementations:

1. **BusinessDemo** (`scripts/run_business_demo.py`):
   - Has `auto_advance` parameter
   - Uses `time.sleep(2)` in auto mode
   - Uses `input("Press Enter...")` in manual mode
   - Hardcoded delays and prompts

2. **InteractiveDemo** (`src/ibdm/demo/interactive_demo.py`):
   - Always waits for user input
   - No playback or automatic mode
   - No replay support

**Issues**:
- Code duplication
- Inconsistent user experience
- Hard to add new execution modes (e.g., replay)
- Hard to configure (fixed delays, prompts)

## Solution

Create a reusable `ExecutionController` that:
- Abstracts execution timing and flow control
- Supports multiple execution modes
- Is configurable (delays, prompts, callbacks)
- Works with both scripted and interactive demos

## Design

### Execution Modes

1. **STEP** (Manual)
   - Wait for user input before each action
   - Prompt: `"Press Enter to continue..."`
   - Use case: Debugging, presentations, learning

2. **AUTO** (Automatic)
   - Automatic advancement with configurable delays
   - Default delay: 2 seconds
   - Use case: Demos, videos, testing

3. **REPLAY** (Playback)
   - Play back saved dialogue sessions
   - Supports step-through or auto-play of replay
   - Use case: Debugging, analysis, documentation

### Architecture

```python
from enum import Enum
from typing import Callable, Optional


class ExecutionMode(Enum):
    """Execution mode for dialogue scenarios."""
    STEP = "step"      # Manual: wait for user input
    AUTO = "auto"      # Automatic: timed delays
    REPLAY = "replay"  # Playback: from saved session


class ExecutionController:
    """Controls execution flow for dialogue scenarios.

    Provides consistent execution timing and flow control across
    different demo types (scripted scenarios, interactive sessions,
    replays).
    """

    def __init__(
        self,
        mode: ExecutionMode = ExecutionMode.STEP,
        auto_delay: float = 2.0,
        banner_delay: float = 3.0,
        prompt: str = "Press Enter to continue...",
        on_interrupt: Optional[Callable[[], None]] = None,
    ):
        """Initialize execution controller.

        Args:
            mode: Execution mode (step/auto/replay)
            auto_delay: Delay between turns in auto mode (seconds)
            banner_delay: Delay after showing banner in auto mode (seconds)
            prompt: Prompt message for step mode
            on_interrupt: Callback when user interrupts (Ctrl+C)
        """

    def wait_at_banner(self) -> None:
        """Wait after displaying banner/intro."""

    def wait_between_turns(self) -> None:
        """Wait between dialogue turns."""

    def wait_at_end(self) -> None:
        """Wait at end of scenario."""

    def pause(self) -> None:
        """Pause execution until user action."""

    def set_mode(self, mode: ExecutionMode) -> None:
        """Change execution mode dynamically."""

    def configure(self, **kwargs) -> None:
        """Update configuration dynamically."""
```

### Integration Points

#### BusinessDemo Integration

```python
class BusinessDemo:
    def __init__(
        self,
        scenario_path: Path,
        verbose: bool = True,
        execution_mode: ExecutionMode = ExecutionMode.STEP,
        nlg_mode: str = "off",
    ):
        self.controller = ExecutionController(
            mode=execution_mode,
            auto_delay=2.0,
            banner_delay=3.0,
        )

    def run_scenario(self) -> dict[str, Any]:
        self.print_banner()
        self.controller.wait_at_banner()

        for i, turn in enumerate(self.scenario["turns"]):
            self.print_turn(turn, i)

            if i < len(self.scenario["turns"]) - 1:
                self.controller.wait_between_turns()

        self.print_summary()
        return self.scenario.get("metrics", {})
```

#### InteractiveDemo Integration

```python
class InteractiveDemo:
    def __init__(
        self,
        agent_id: str = "system",
        execution_mode: ExecutionMode = ExecutionMode.STEP,
        # ... other params
    ):
        self.controller = ExecutionController(
            mode=execution_mode,
            prompt="",  # Interactive demo has its own prompts
        )

    def run(self) -> None:
        self.display_banner()

        while True:
            user_input = input("user> ")
            # ... process input ...

            # Optional pause between turns for demos
            if self.controller.mode == ExecutionMode.AUTO:
                self.controller.wait_between_turns()
```

### CLI Integration

Update CLI arguments to support execution modes:

```bash
# BusinessDemo
python scripts/run_business_demo.py --mode step    # Manual
python scripts/run_business_demo.py --mode auto    # Automatic
python scripts/run_business_demo.py --mode auto --delay 1.5  # Custom delay

# InteractiveDemo
python -m ibdm.demo.interactive_demo --mode step   # Default
python -m ibdm.demo.interactive_demo --mode auto   # Demo mode
```

### Configuration

Support configuration via:
1. Constructor parameters
2. Environment variables
3. Runtime updates

```python
# Environment variables
IBDM_EXECUTION_MODE=auto
IBDM_AUTO_DELAY=1.5
IBDM_BANNER_DELAY=3.0

# Runtime configuration
controller.configure(auto_delay=1.0)
controller.set_mode(ExecutionMode.AUTO)
```

## Benefits

1. **Code Reuse**: Single implementation for all demos
2. **Consistency**: Same UX across all execution contexts
3. **Flexibility**: Easy to add new modes (e.g., FAST, DEBUG)
4. **Configurability**: Adjust delays, prompts, callbacks
5. **Testability**: Easy to test scenarios with zero delays
6. **Interruptibility**: Centralized Ctrl+C handling

## Implementation Plan

1. Create `src/ibdm/demo/execution_controller.py`
   - Implement `ExecutionMode` enum
   - Implement `ExecutionController` class
   - Add docstrings and type hints

2. Add tests `tests/unit/test_execution_controller.py`
   - Test each execution mode
   - Test configuration updates
   - Test interrupt handling

3. Refactor BusinessDemo
   - Replace `auto_advance` with `ExecutionController`
   - Update CLI arguments
   - Remove hardcoded delays

4. Update InteractiveDemo (optional)
   - Add optional ExecutionController support
   - Preserve backward compatibility

5. Documentation
   - Update user guides
   - Add examples to docs

## Future Enhancements

1. **REPLAY Mode**: Full implementation with session loading
2. **FAST Mode**: Zero delays for testing
3. **DEBUG Mode**: Step-by-step with state inspection
4. **Callbacks**: Hooks for custom behavior at each wait point
5. **Progress Indicators**: Show progress in auto mode
6. **Video Recording**: Integration with asciinema/terminalizer

## Compatibility

- **Backward Compatible**: Existing demos continue to work
- **Migration Path**: Gradual adoption, not breaking changes
- **Optional**: Demos can opt-in to ExecutionController

## Testing Strategy

```python
def test_step_mode():
    """Test step mode waits for user input."""
    controller = ExecutionController(mode=ExecutionMode.STEP)
    # Mock input() and verify it's called

def test_auto_mode():
    """Test auto mode uses time.sleep()."""
    controller = ExecutionController(mode=ExecutionMode.AUTO, auto_delay=0.1)
    # Measure time and verify delay

def test_mode_switching():
    """Test dynamic mode changes."""
    controller = ExecutionController(mode=ExecutionMode.STEP)
    controller.set_mode(ExecutionMode.AUTO)
    # Verify behavior changes

def test_configuration():
    """Test runtime configuration updates."""
    controller = ExecutionController(auto_delay=2.0)
    controller.configure(auto_delay=1.0)
    # Verify new delay is used
```

## Success Criteria

1. ✅ ExecutionController class implemented
2. ✅ All execution modes work correctly
3. ✅ Tests pass with 100% coverage
4. ✅ BusinessDemo refactored to use controller
5. ✅ No regressions in existing demos
6. ✅ Documentation updated

## References

- Task: ibdm-150
- Current Implementation: `scripts/run_business_demo.py` (lines 299-314)
- Related: ibdm-100.7 (session persistence and replay)
