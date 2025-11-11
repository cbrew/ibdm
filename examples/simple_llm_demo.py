#!/usr/bin/env python3
"""Demonstration of using Gemini 2.5 models through LiteLLM.

This script shows how to use LiteLLM to interact with Google's Gemini models
using the IBDM project's LLM configuration standards.

Model Usage:
- gemini-2.5-pro: Large-scale generation, complex reasoning, extended responses
- gemini-2.5-flash: Control flow, analytics, classification, structured data
"""

import os

from litellm import completion


def verify_api_keys():
    """Verify that required API keys are present."""
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in environment")

    print("✓ Gemini API key verified")
    return True


def call_gemini(model: str, prompt: str, temperature: float = 0.7, max_tokens: int = 8000) -> str:
    """Call a Gemini model using LiteLLM.

    Args:
        model: The model to use (gemini-2.5-pro or gemini-2.5-flash)
        prompt: The user prompt/question
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        max_tokens: Maximum tokens in response

    Returns:
        The model's response text
    """
    model_name = model.split("/")[-1] if "/" in model else model
    print(f"\n{'=' * 70}")
    print(f"Calling {model_name}...")
    print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"{'=' * 70}\n")

    # Call Gemini through LiteLLM
    # LiteLLM automatically uses GEMINI_API_KEY from environment
    response = completion(
        model=f"gemini/{model_name}" if "/" not in model else model,
        messages=[{"role": "user", "content": prompt}],
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
    print("LiteLLM + Gemini 2.5 Models Demo")
    print("=" * 70)
    print(
        "\nThis demo showcases both Gemini 2.5 Pro and Flash models with appropriate use cases.\n"
    )

    # Verify environment
    verify_api_keys()

    print("\n" + "=" * 70)
    print("PART 1: Gemini 2.5 Pro - Large-scale Generation")
    print("=" * 70)

    # Example 1: Complex explanation (Pro)
    call_gemini(
        "gemini-2.5-pro",
        """Explain what an issue-based dialogue management system is, covering:
        1. Its theoretical foundations
        2. How it differs from traditional dialogue systems
        3. Key advantages and challenges
        Provide a comprehensive response.""",
        temperature=0.7,
        max_tokens=2000,
    )

    # Example 2: Creative writing (Pro)
    call_gemini(
        "gemini-2.5-pro",
        """Write a short story (3-4 paragraphs) about an AI system learning to
        understand human dialogue through issue-based reasoning.""",
        temperature=0.9,
        max_tokens=1500,
    )

    print("\n" + "=" * 70)
    print("PART 2: Gemini 2.5 Flash - Control & Analytics")
    print("=" * 70)

    # Example 3: Classification task (Flash)
    call_gemini(
        "gemini-2.5-flash",
        """Classify the following dialogue act: "What's the weather like tomorrow?"

        Choose one: question, statement, command, acknowledgment
        Respond with just the category and a brief reason.""",
        temperature=0.3,
        max_tokens=200,
    )

    # Example 4: Structured extraction (Flash)
    call_gemini(
        "gemini-2.5-flash",
        """Extract key information from this text in JSON format:
        "The meeting is scheduled for next Tuesday at 2 PM in room 305.
        Please bring your laptop and the quarterly report."

        Return: {"day": ..., "time": ..., "location": ..., "items": [...]}""",
        temperature=0.2,
        max_tokens=300,
    )

    # Example 5: Quick QA (Flash)
    call_gemini(
        "gemini-2.5-flash",
        "List 3 key components of a dialogue system. Be concise.",
        temperature=0.5,
        max_tokens=200,
    )

    print("\n" + "=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)
    print("\nModel Selection Summary:")
    print("- Use gemini-2.5-pro for: detailed generation, creative tasks, complex reasoning")
    print("- Use gemini-2.5-flash for: classification, extraction, quick answers, control flow")
    print("=" * 70)


if __name__ == "__main__":
    main()
