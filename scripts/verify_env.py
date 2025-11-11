#!/usr/bin/env python3
"""Verify environment variables for IBDM project.

This script checks that all required API keys are available
in the environment for LLM integrations via LiteLLM.
"""

import os
import sys


def verify_environment():
    """Verify required environment variables are present."""
    required_vars = {
        "GEMINI_API_KEY": "Google/Gemini API key for LLM access",
        "OPENAI_API_KEY": "OpenAI API key for LLM access",
    }

    missing = []
    present = []

    print("Checking environment variables...\n")

    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show first 20 characters of key for verification
            masked_value = f"{value[:20]}..." if len(value) > 20 else value
            present.append((var, masked_value, description))
            print(f"✓ {var}")
            print(f"  {description}")
            print(f"  Value: {masked_value}")
            print()
        else:
            missing.append((var, description))
            print(f"✗ {var}")
            print(f"  {description}")
            print(f"  Status: NOT FOUND")
            print()

    # Summary
    print("-" * 60)
    print(f"Found: {len(present)}/{len(required_vars)} required variables")

    if missing:
        print("\nMissing variables:")
        for var, desc in missing:
            print(f"  - {var}: {desc}")
        print("\nPlease ensure API keys are set in the environment.")
        return False
    else:
        print("\n✓ All required environment variables are present!")
        print("\nLiteLLM will automatically use these keys:")
        print("  - GEMINI_API_KEY for gemini/* models")
        print("  - OPENAI_API_KEY for gpt-* models")
        return True


if __name__ == "__main__":
    success = verify_environment()
    sys.exit(0 if success else 1)
