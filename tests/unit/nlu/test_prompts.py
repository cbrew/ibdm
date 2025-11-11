"""Tests for prompt template system."""

import json

import pytest

from ibdm.nlu.prompts import (
    Example,
    PromptTemplate,
    create_answer_parsing_template,
    create_dialogue_act_template,
    create_entity_extraction_template,
    create_question_understanding_template,
    create_reference_resolution_template,
    create_semantic_parsing_template,
    get_template,
    list_templates,
)


def test_example_format_without_reasoning():
    """Test formatting example without reasoning."""
    example = Example(input="test input", output="test output")

    formatted = example.format(include_reasoning=False)

    assert "Input: test input" in formatted
    assert "Output: test output" in formatted
    assert "Reasoning:" not in formatted


def test_example_format_with_reasoning():
    """Test formatting example with reasoning."""
    example = Example(input="test input", output="test output", reasoning="because of X")

    formatted = example.format(include_reasoning=True)

    assert "Input: test input" in formatted
    assert "Reasoning: because of X" in formatted
    assert "Output: test output" in formatted


def test_example_format_with_reasoning_disabled():
    """Test that reasoning is not shown when disabled."""
    example = Example(input="test input", output="test output", reasoning="because of X")

    formatted = example.format(include_reasoning=False)

    assert "Reasoning:" not in formatted


def test_prompt_template_basic():
    """Test basic prompt template creation and formatting."""
    template = PromptTemplate(
        name="test",
        system_prompt="You are a test assistant.",
        task_description="Test task description.",
        output_format='JSON: {"result": "value"}',
    )

    system, user = template.format("test input")

    assert system == "You are a test assistant."
    assert "Test task description" in user
    assert "## Output Format" in user
    assert '{"result": "value"}' in user
    assert "test input" in user


def test_prompt_template_with_variables():
    """Test template with variable interpolation."""
    template = PromptTemplate(
        name="test",
        system_prompt="You are a {role} assistant.",
        task_description="Perform {task_type} on the input.",
        output_format="Format: {format_type}",
    )

    system, user = template.format(
        "test input",
        variables={"role": "helpful", "task_type": "analysis", "format_type": "JSON"},
    )

    assert "helpful assistant" in system
    assert "Perform analysis" in user
    assert "Format: JSON" in user


def test_prompt_template_add_example():
    """Test adding examples to template."""
    template = PromptTemplate(
        name="test",
        system_prompt="Test",
        task_description="Task",
        output_format="Output",
    )

    assert len(template.examples) == 0

    template.add_example("input 1", "output 1")
    assert len(template.examples) == 1

    template.add_example("input 2", "output 2", reasoning="reason 2")
    assert len(template.examples) == 2
    assert template.examples[1].reasoning == "reason 2"


def test_prompt_template_format_with_examples():
    """Test template formatting with examples."""
    template = PromptTemplate(
        name="test",
        system_prompt="Test",
        task_description="Task",
        output_format="Output",
    )

    template.add_example("example input", "example output")

    system, user = template.format("actual input", include_examples=True)

    assert "## Examples" in user
    assert "Example 1" in user
    assert "example input" in user
    assert "example output" in user
    assert "actual input" in user


def test_prompt_template_format_without_examples():
    """Test template formatting without examples."""
    template = PromptTemplate(
        name="test",
        system_prompt="Test",
        task_description="Task",
        output_format="Output",
    )

    template.add_example("example input", "example output")

    system, user = template.format("actual input", include_examples=False)

    assert "## Examples" not in user
    assert "example input" not in user
    assert "actual input" in user


def test_dialogue_act_template():
    """Test dialogue act classification template."""
    template = create_dialogue_act_template()

    assert template.name == "dialogue_act_classification"
    assert len(template.examples) > 0
    assert not template.include_reasoning

    system, user = template.format("Hello, how are you?")

    assert "dialogue" in system.lower()
    assert "question" in user
    assert "answer" in user
    assert "command" in user


def test_question_understanding_template():
    """Test question understanding template."""
    template = create_question_understanding_template()

    assert template.name == "question_understanding"
    assert len(template.examples) > 0
    assert template.include_reasoning

    system, user = template.format("What time is it?")

    assert "question" in system.lower()
    assert "type" in user
    assert "focus" in user
    assert "presuppositions" in user


def test_entity_extraction_template():
    """Test entity extraction template."""
    template = create_entity_extraction_template()

    assert template.name == "entity_extraction"
    assert len(template.examples) > 0

    system, user = template.format("Bob lives in Paris.")

    assert "entity" in system.lower() or "entity" in user.lower()
    assert "PERSON" in user
    assert "LOC" in user


def test_semantic_parsing_template():
    """Test semantic parsing template."""
    template = create_semantic_parsing_template()

    assert template.name == "semantic_parsing"
    assert len(template.examples) > 0
    assert template.include_reasoning

    system, user = template.format("John runs quickly.")

    assert "semantic" in system.lower()
    assert "predicate" in user
    assert "arguments" in user


def test_answer_parsing_template():
    """Test answer parsing template."""
    template = create_answer_parsing_template()

    assert template.name == "answer_parsing"
    assert len(template.examples) > 0
    assert template.include_reasoning

    system, user = template.format('Q: "What?" A: "Something"')

    assert "answer" in system.lower()
    assert "addresses_question" in user
    assert "answer_type" in user


def test_reference_resolution_template():
    """Test reference resolution template."""
    template = create_reference_resolution_template()

    assert template.name == "reference_resolution"
    assert len(template.examples) > 0
    assert template.include_reasoning

    system, user = template.format("Context: John left. Current: He returned.")

    assert "reference" in system.lower() or "anaphora" in system.lower()
    assert "expression" in user
    assert "antecedent" in user


def test_get_template_success():
    """Test retrieving template from registry."""
    template = get_template("dialogue_act")

    assert isinstance(template, PromptTemplate)
    assert template.name == "dialogue_act_classification"


def test_get_template_not_found():
    """Test error when template not found."""
    with pytest.raises(KeyError, match="not found"):
        get_template("nonexistent_template")


def test_list_templates():
    """Test listing all available templates."""
    templates = list_templates()

    assert isinstance(templates, list)
    assert len(templates) > 0
    assert "dialogue_act" in templates
    assert "question_understanding" in templates
    assert "entity_extraction" in templates


def test_template_examples_are_valid_json():
    """Test that all template examples produce valid JSON outputs."""
    templates_to_test = [
        "dialogue_act",
        "question_understanding",
        "entity_extraction",
        "semantic_parsing",
        "answer_parsing",
        "reference_resolution",
    ]

    for template_name in templates_to_test:
        template = get_template(template_name)

        for example in template.examples:
            # Try to parse the output as JSON
            try:
                json.loads(example.output)
            except json.JSONDecodeError:
                pytest.fail(
                    f"Template '{template_name}' has example with invalid JSON output: "
                    f"{example.output}"
                )


def test_template_output_formats_mention_json():
    """Test that templates requiring JSON mention it in output format."""
    templates_to_test = [
        "dialogue_act",
        "question_understanding",
        "entity_extraction",
        "semantic_parsing",
        "answer_parsing",
        "reference_resolution",
    ]

    for template_name in templates_to_test:
        template = get_template(template_name)
        assert "json" in template.output_format.lower(), (
            f"Template '{template_name}' should mention JSON in output format"
        )
