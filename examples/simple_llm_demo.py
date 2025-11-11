#!/usr/bin/env python3
"""Simple demonstration of using Gemini 2.5 Pro through LiteLLM.

This script shows how to use LiteLLM to interact with Google's Gemini models
using the IBDM project's LLM configuration standards.
"""

import os

from litellm import completion


def verify_api_keys():
    """Verify that required API keys are present."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in environment")

    print("✓ API keys verified")
    return True


def call_gemini_pro(prompt: str, temperature: float = 0.7, max_tokens: int = 8000):
    """Call Gemini 2.5 Pro using LiteLLM.

    Args:
        prompt: The user prompt/question
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        max_tokens: Maximum tokens in response

    Returns:
        The model's response text
    """
    print(f"\n{'=' * 60}")
    print("Calling Gemini 2.5 Pro...")
    print(f"Prompt: {prompt}")
    print(f"{'=' * 60}\n")

    try:
        # Call Gemini through LiteLLM
        # LiteLLM automatically uses GEMINI_API_KEY from environment
        response = completion(
            model="gemini/gemini-2.5-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Extract response text
        response_text = response.choices[0].message.content

        # Print usage statistics
        usage = response.usage
        print("Response received!")
        print(
            f"Tokens used: {usage.total_tokens} "
            f"(prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})"
        )
        print(f"\n{'=' * 60}")
        print("Response:")
        print(f"{'=' * 60}\n")
        print(response_text)
        print(f"\n{'=' * 60}\n")

        return response_text

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        print("\nTrying fallback to OpenAI GPT-4o-mini...")

        # Fallback to OpenAI
        try:
            response = completion(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            response_text = response.choices[0].message.content
            print("✓ Fallback successful!")
            return response_text
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            raise


def main():
    """Run the demo."""
    print("LiteLLM + Gemini 2.5 Pro Demo")
    print("=" * 60)

    # Verify environment
    verify_api_keys()

    # Example 1: Simple question
    call_gemini_pro(
        "Explain what a dialogue management system is in 2-3 sentences.", temperature=0.7
    )

    # Example 2: More structured request
    call_gemini_pro(
        """List 3 key components of an issue-based dialogue management system.
        Format your response as a numbered list.""",
        temperature=0.5,
    )

    # Example 3: Creative task
    call_gemini_pro("Write a haiku about natural language understanding.", temperature=0.9)

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
