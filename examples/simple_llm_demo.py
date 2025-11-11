#!/usr/bin/env python3
"""Demonstration of using Anthropic Claude 4.5 models through LiteLLM.

This script shows how to use LiteLLM to interact with Anthropic's Claude 4.5 models
using the IBDM project's LLM configuration standards.

Model Usage:
- claude-sonnet-4-5-20250929: Large-scale generation, complex reasoning, extended responses
- claude-haiku-4-5-20251001: Control flow, analytics, classification, structured data
"""

import os

from litellm import completion


def verify_api_keys():
    """Verify that required API keys are present."""
    ibdm_key = os.getenv("IBDM_API_KEY")

    if not ibdm_key:
        raise ValueError("IBDM_API_KEY not found in environment")

    print("✓ IBDM API key verified")
    return True


def call_claude(model: str, prompt: str, temperature: float = 0.7, max_tokens: int = 8000) -> str:
    """Call a Claude model using LiteLLM.

    Args:
        model: The model to use (claude-sonnet-4-5-20250929 or claude-haiku-4-5-20251001)
        prompt: The user prompt/question
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        max_tokens: Maximum tokens in response

    Returns:
        The model's response text
    """
    # Get API key from environment
    api_key = os.getenv("IBDM_API_KEY")

    # Extract short model name for display
    model_display = "Sonnet 4.5" if "sonnet" in model else "Haiku 4.5"

    print(f"\n{'=' * 70}")
    print(f"Calling Claude {model_display}...")
    print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"{'=' * 70}\n")

    # Call Claude through LiteLLM with explicit API key
    response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_key=api_key,  # Explicitly pass API key to avoid conflicts
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Extract response text
    response_text = response.choices[0].message.content

    # Print usage statistics
    usage = response.usage
    print("✓ Response received!")
    print(
        f"Tokens used: {usage.total_tokens} "
        f"(prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})"
    )
    print(f"\n{'=' * 70}")
    print("Response:")
    print(f"{'=' * 70}\n")
    print(response_text)
    print(f"\n{'=' * 70}\n")

    return response_text


def main():
    """Run the demo."""
    print("=" * 70)
    print("LiteLLM + Claude 4.5 Models Demo")
    print("=" * 70)
    print(
        "\nThis demo showcases both Claude Sonnet 4.5 and Haiku 4.5 with appropriate use cases.\n"
    )

    # Verify environment
    verify_api_keys()

    print("\n" + "=" * 70)
    print("PART 1: Claude Sonnet 4.5 - Large-scale Generation")
    print("=" * 70)

    # Example 1: Complex explanation (Sonnet)
    call_claude(
        "claude-sonnet-4-5-20250929",
        """Explain what an issue-based dialogue management system is, covering:
        1. Its theoretical foundations
        2. How it differs from traditional dialogue systems
        3. Key advantages and challenges
        Provide a comprehensive response.""",
        temperature=0.7,
        max_tokens=2000,
    )

    # Example 2: Creative writing (Sonnet)
    call_claude(
        "claude-sonnet-4-5-20250929",
        """Write a short story (3-4 paragraphs) about an AI system learning to
        understand human dialogue through issue-based reasoning.""",
        temperature=0.9,
        max_tokens=1500,
    )

    print("\n" + "=" * 70)
    print("PART 2: Claude Haiku 4.5 - Control & Analytics")
    print("=" * 70)

    # Example 3: Classification task (Haiku)
    call_claude(
        "claude-haiku-4-5-20251001",
        """Classify the following dialogue act: "What's the weather like tomorrow?"

        Choose one: question, statement, command, acknowledgment
        Respond with just the category and a brief reason.""",
        temperature=0.3,
        max_tokens=200,
    )

    # Example 4: Structured extraction (Haiku)
    call_claude(
        "claude-haiku-4-5-20251001",
        """Extract key information from this text in JSON format:
        "The meeting is scheduled for next Tuesday at 2 PM in room 305.
        Please bring your laptop and the quarterly report."

        Return: {"day": ..., "time": ..., "location": ..., "items": [...]}""",
        temperature=0.2,
        max_tokens=300,
    )

    # Example 5: Quick QA (Haiku)
    call_claude(
        "claude-haiku-4-5-20251001",
        "List 3 key components of a dialogue system. Be concise.",
        temperature=0.5,
        max_tokens=200,
    )

    print("\n" + "=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)
    print("\nModel Selection Summary:")
    print("- Use Sonnet 4.5 for: detailed generation, creative tasks, complex reasoning")
    print("- Use Haiku 4.5 for: classification, extraction, quick answers, control flow")
    print("=" * 70)


if __name__ == "__main__":
    main()
