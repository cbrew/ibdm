#!/usr/bin/env python3
"""Demonstration of using OpenAI GPT-4 models through LiteLLM.

This script shows how to use LiteLLM to interact with OpenAI's GPT-4 models
using the IBDM project's LLM configuration standards.

Model Usage:
- gpt-4o: Large-scale generation, complex reasoning, extended responses
- gpt-4o-mini: Control flow, analytics, classification, structured data
"""

import os

from litellm import completion


def verify_api_keys():
    """Verify that required API keys are present."""
    openai_key = os.getenv("OPENAI_API_KEY")

    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in environment")

    print("✓ OpenAI API key verified")
    return True


def call_openai(model: str, prompt: str, temperature: float = 0.7, max_tokens: int = 8000) -> str:
    """Call an OpenAI model using LiteLLM.

    Args:
        model: The model to use (gpt-4o or gpt-4o-mini)
        prompt: The user prompt/question
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        max_tokens: Maximum tokens in response

    Returns:
        The model's response text
    """
    print(f"\n{'=' * 70}")
    print(f"Calling {model}...")
    print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"{'=' * 70}\n")

    # Call OpenAI through LiteLLM
    # LiteLLM automatically uses OPENAI_API_KEY from environment
    response = completion(
        model=model,
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
    print("LiteLLM + OpenAI GPT-4 Models Demo")
    print("=" * 70)
    print(
        "\nThis demo showcases both GPT-4o and GPT-4o-mini models with appropriate use cases.\n"
    )

    # Verify environment
    verify_api_keys()

    print("\n" + "=" * 70)
    print("PART 1: GPT-4o - Large-scale Generation")
    print("=" * 70)

    # Example 1: Complex explanation (4o)
    call_openai(
        "gpt-4o",
        """Explain what an issue-based dialogue management system is, covering:
        1. Its theoretical foundations
        2. How it differs from traditional dialogue systems
        3. Key advantages and challenges
        Provide a comprehensive response.""",
        temperature=0.7,
        max_tokens=2000,
    )

    # Example 2: Creative writing (4o)
    call_openai(
        "gpt-4o",
        """Write a short story (3-4 paragraphs) about an AI system learning to
        understand human dialogue through issue-based reasoning.""",
        temperature=0.9,
        max_tokens=1500,
    )

    print("\n" + "=" * 70)
    print("PART 2: GPT-4o-mini - Control & Analytics")
    print("=" * 70)

    # Example 3: Classification task (mini)
    call_openai(
        "gpt-4o-mini",
        """Classify the following dialogue act: "What's the weather like tomorrow?"

        Choose one: question, statement, command, acknowledgment
        Respond with just the category and a brief reason.""",
        temperature=0.3,
        max_tokens=200,
    )

    # Example 4: Structured extraction (mini)
    call_openai(
        "gpt-4o-mini",
        """Extract key information from this text in JSON format:
        "The meeting is scheduled for next Tuesday at 2 PM in room 305.
        Please bring your laptop and the quarterly report."

        Return: {"day": ..., "time": ..., "location": ..., "items": [...]}""",
        temperature=0.2,
        max_tokens=300,
    )

    # Example 5: Quick QA (mini)
    call_openai(
        "gpt-4o-mini",
        "List 3 key components of a dialogue system. Be concise.",
        temperature=0.5,
        max_tokens=200,
    )

    print("\n" + "=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)
    print("\nModel Selection Summary:")
    print("- Use gpt-4o for: detailed generation, creative tasks, complex reasoning")
    print("- Use gpt-4o-mini for: classification, extraction, quick answers, control flow")
    print("=" * 70)


if __name__ == "__main__":
    main()
