"""Prompt template system for IBDM natural language understanding tasks.

This module provides composable prompt templates for various NLU tasks including:
- Semantic parsing
- Dialogue act classification
- Entity extraction
- Question understanding
- Answer parsing
- Reference resolution

Templates support:
- Variable interpolation
- Few-shot examples
- Chain-of-thought reasoning
- Structured output formatting
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Example:
    """A single few-shot example.

    Attributes:
        input: The example input text
        output: The expected output
        reasoning: Optional chain-of-thought reasoning steps
    """

    input: str
    output: str
    reasoning: str | None = None

    def format(self, include_reasoning: bool = True) -> str:
        """Format the example for inclusion in a prompt.

        Args:
            include_reasoning: Whether to include reasoning steps

        Returns:
            Formatted example string
        """
        parts = [f"Input: {self.input}"]

        if include_reasoning and self.reasoning:
            parts.append(f"Reasoning: {self.reasoning}")

        parts.append(f"Output: {self.output}")

        return "\n".join(parts)


def _example_list_factory() -> list[Example]:
    """Factory function for creating empty example lists."""
    return []


@dataclass
class PromptTemplate:
    """A composable prompt template for NLU tasks.

    Templates consist of:
    - System prompt: Instructions for the model
    - Task description: What the model should do
    - Few-shot examples: Example inputs and outputs
    - Output format: Specification of expected output structure
    - User prompt: The actual task input

    Attributes:
        name: Template name/identifier
        system_prompt: General instructions for the model
        task_description: Specific task description
        output_format: Description of expected output format
        examples: Few-shot examples
        include_reasoning: Whether to include chain-of-thought reasoning
    """

    name: str
    system_prompt: str
    task_description: str
    output_format: str
    examples: list[Example] = field(default_factory=_example_list_factory)
    include_reasoning: bool = True

    def format(
        self,
        input_text: str,
        variables: dict[str, Any] | None = None,
        include_examples: bool = True,
    ) -> tuple[str, str]:
        """Format the template with the given input and variables.

        Args:
            input_text: The input text to process
            variables: Optional variables to interpolate into template
            include_examples: Whether to include few-shot examples

        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        vars_dict = variables or {}

        # Format system prompt
        system = self.system_prompt.format(**vars_dict)

        # Build user prompt
        user_parts = [self.task_description.format(**vars_dict)]

        # Add output format
        user_parts.append("\n## Output Format")
        # Only format if there are variables, otherwise use as-is to avoid JSON brace issues
        if vars_dict:
            user_parts.append(self.output_format.format(**vars_dict))
        else:
            user_parts.append(self.output_format)

        # Add examples if requested
        if include_examples and self.examples:
            user_parts.append("\n## Examples")
            for i, example in enumerate(self.examples, 1):
                user_parts.append(f"\n### Example {i}")
                user_parts.append(example.format(self.include_reasoning))

        # Add the actual input
        user_parts.append("\n## Your Task")
        user_parts.append(f"Input: {input_text}")
        user_parts.append("Output:")

        return system, "\n".join(user_parts)

    def add_example(self, input: str, output: str, reasoning: str | None = None) -> None:
        """Add a few-shot example to the template.

        Args:
            input: Example input text
            output: Expected output
            reasoning: Optional reasoning steps
        """
        self.examples.append(Example(input=input, output=output, reasoning=reasoning))


# Predefined templates for common NLU tasks


def create_dialogue_act_template() -> PromptTemplate:
    """Create a template for dialogue act classification.

    Returns:
        PromptTemplate configured for dialogue act classification
    """
    template = PromptTemplate(
        name="dialogue_act_classification",
        system_prompt="You are an expert in dialogue analysis and pragmatics. "
        "Your task is to classify utterances into dialogue acts based on their "
        "communicative function.",
        task_description="Classify the following utterance into one of these dialogue acts:\n"
        "- question: Requesting information\n"
        "- answer: Providing information in response to a question\n"
        "- assertion: Making a statement or claim (NOT requests or needs)\n"
        "- command: Giving an instruction or request for action "
        "(includes 'I need to...', 'I want to...', imperatives)\n"
        "- acknowledgment: Confirming understanding or receipt of information\n"
        "- clarification: Requesting or providing clarification\n"
        "- greeting: Opening or closing a conversation\n"
        "- other: Other dialogue functions",
        output_format='Respond with JSON: {{"act": "<dialogue_act>", "confidence": <0-1>}}',
        include_reasoning=False,
    )

    # Add examples
    template.add_example(
        input="What's the weather like tomorrow?",
        output='{"act": "question", "confidence": 0.95}',
    )

    template.add_example(
        input="It will be sunny with a high of 75 degrees.",
        output='{"act": "answer", "confidence": 0.9}',
    )

    template.add_example(
        input="Please close the door.",
        output='{"act": "command", "confidence": 0.95}',
    )

    template.add_example(
        input="I need to draft an NDA.",
        output='{"act": "command", "confidence": 0.85}',
    )

    template.add_example(
        input="I want to schedule a meeting for tomorrow.",
        output='{"act": "command", "confidence": 0.85}',
    )

    template.add_example(
        input="I understand, I'll take care of it.",
        output='{"act": "acknowledgment", "confidence": 0.9}',
    )

    return template


def create_question_understanding_template() -> PromptTemplate:
    """Create a template for deep question understanding.

    Returns:
        PromptTemplate configured for question analysis
    """
    template = PromptTemplate(
        name="question_understanding",
        system_prompt="You are an expert in question semantics and pragmatics. "
        "Your task is to analyze questions and extract their semantic structure, "
        "including type, focus, presuppositions, and implicit constraints.",
        task_description="Analyze the following question and extract:\n"
        "- Question type: wh (who/what/where/when/why/how), yes-no, alternative, or rhetorical\n"
        "- Focus: What the question is asking about (the wh-word referent or decision point)\n"
        "- Presuppositions: What the question assumes to be true\n"
        "- Constraints: Any implicit constraints or preferences",
        output_format="Respond with JSON:\n"
        "{\n"
        '  "type": "wh|yes-no|alternative|rhetorical",\n'
        '  "focus": "<what the question asks about>",\n'
        '  "presuppositions": ["<assumption 1>", "<assumption 2>", ...],\n'
        '  "constraints": ["<constraint 1>", "<constraint 2>", ...]\n'
        "}",
        include_reasoning=True,
    )

    # Add examples
    template.add_example(
        input="What's the best Italian restaurant in downtown?",
        output='{"type": "wh", "focus": "Italian restaurant", '
        '"presuppositions": ["There are Italian restaurants in downtown", '
        '"Some are better than others"], '
        '"constraints": ["Location: downtown", "Cuisine: Italian", "Quality: best"]}',
        reasoning="This is a wh-question (what) asking about restaurants. "
        "It presupposes restaurants exist and can be ranked. "
        "Constraints include location (downtown), cuisine (Italian), and quality (best).",
    )

    template.add_example(
        input="Is the museum open on Sundays?",
        output='{"type": "yes-no", "focus": "museum opening status", '
        '"presuppositions": ["A museum exists", "Museums have opening hours"], '
        '"constraints": ["Day: Sunday"]}',
        reasoning="This is a yes-no question about the museum's status. "
        "It presupposes the museum exists and has variable hours. "
        "The constraint is the specific day (Sunday).",
    )

    template.add_example(
        input="Should we meet at 2pm or 3pm?",
        output='{"type": "alternative", "focus": "meeting time", '
        '"presuppositions": ["A meeting is planned", "Time needs to be decided"], '
        '"constraints": ["Options: 2pm or 3pm"]}',
        reasoning="This is an alternative question presenting two time options. "
        "It presupposes a meeting is happening and needs a time. "
        "The constraints are the two specific time options.",
    )

    return template


def create_entity_extraction_template() -> PromptTemplate:
    """Create a template for entity extraction.

    Returns:
        PromptTemplate configured for entity extraction
    """
    template = PromptTemplate(
        name="entity_extraction",
        system_prompt="You are an expert in named entity recognition and information extraction. "
        "Your task is to identify and extract entities from text, including persons, "
        "organizations, locations, dates, times, and domain-specific entities.",
        task_description="Extract all entities from the following text and classify them:\n"
        "- PERSON: People, including fictional characters\n"
        "- ORG: Organizations, companies, agencies, institutions\n"
        "- LOC: Locations, including GPE (countries, cities) and physical locations\n"
        "- DATE: Absolute or relative dates\n"
        "- TIME: Times of day\n"
        "- QUANTITY: Measurements, amounts, numbers\n"
        "- OTHER: Domain-specific entities",
        output_format="Respond with JSON:\n"
        "{\n"
        '  "entities": [\n'
        '    {"text": "<entity text>", "type": "<entity type>", '
        '"start": <char offset>, "end": <char offset>},\n'
        "    ...\n"
        "  ]\n"
        "}",
        include_reasoning=False,
    )

    # Add examples
    template.add_example(
        input="John Smith will visit the New York office next Tuesday at 2pm.",
        output='{"entities": ['
        '{"text": "John Smith", "type": "PERSON", "start": 0, "end": 10}, '
        '{"text": "New York", "type": "LOC", "start": 27, "end": 35}, '
        '{"text": "next Tuesday", "type": "DATE", "start": 43, "end": 55}, '
        '{"text": "2pm", "type": "TIME", "start": 59, "end": 62}'
        "]}",
    )

    template.add_example(
        input="Apple Inc. announced revenue of $90 billion in Q4 2024.",
        output='{"entities": ['
        '{"text": "Apple Inc.", "type": "ORG", "start": 0, "end": 10}, '
        '{"text": "$90 billion", "type": "QUANTITY", "start": 32, "end": 43}, '
        '{"text": "Q4 2024", "type": "DATE", "start": 47, "end": 54}'
        "]}",
    )

    return template


def create_semantic_parsing_template() -> PromptTemplate:
    """Create a template for semantic parsing of utterances.

    Returns:
        PromptTemplate configured for semantic parsing
    """
    template = PromptTemplate(
        name="semantic_parsing",
        system_prompt=(
            "You are an expert in computational semantics and formal meaning "
            "representation. Your task is to parse natural language utterances into "
            "structured semantic representations. "
            "IMPORTANT: Respond with ONLY valid JSON, no explanations or markdown formatting."
        ),
        task_description=(
            "Parse the following utterance into a structured semantic representation:\n"
            "- Identify the main predicate (action, state, or relation)\n"
            "- Extract arguments and their semantic roles (agent, patient, theme, location, etc.)\n"
            "- Capture modifiers (time, manner, degree, etc.)\n"
            "- Note any modal or aspectual information"
        ),
        output_format="Respond with ONLY valid JSON (no markdown, no explanations):\n"
        "{\n"
        '  "predicate": "<main predicate>",\n'
        '  "arguments": [\n'
        '    {"role": "<semantic role>", "value": "<argument>"},\n'
        "    ...\n"
        "  ],\n"
        '  "modifiers": [\n'
        '    {"type": "<modifier type>", "value": "<modifier>"},\n'
        "    ...\n"
        "  ]\n"
        "}",
        include_reasoning=False,  # No reasoning to ensure pure JSON output
    )

    # Add examples (no reasoning to ensure pure JSON output)
    template.add_example(
        input="Alice quickly drove to the airport yesterday.",
        output='{"predicate": "drive", '
        '"arguments": ['
        '{"role": "agent", "value": "Alice"}, '
        '{"role": "goal", "value": "the airport"}'
        "], "
        '"modifiers": ['
        '{"type": "manner", "value": "quickly"}, '
        '{"type": "time", "value": "yesterday"}'
        "]}",
    )

    template.add_example(
        input="The cat is sleeping on the couch.",
        output='{"predicate": "sleep", '
        '"arguments": ['
        '{"role": "theme", "value": "the cat"}'
        "], "
        '"modifiers": ['
        '{"type": "location", "value": "on the couch"}'
        "]}",
        reasoning="The main predicate is 'sleep'. The cat is the theme (entity in a state). "
        "The location modifier specifies where the sleeping is happening.",
    )

    return template


def create_answer_parsing_template() -> PromptTemplate:
    """Create a template for parsing answers and matching them to questions.

    Returns:
        PromptTemplate configured for answer parsing
    """
    template = PromptTemplate(
        name="answer_parsing",
        system_prompt=(
            "You are an expert in dialogue coherence and question-answer relationships. "
            "Your task is to parse answers and determine how they relate to their "
            "corresponding questions."
        ),
        task_description="Given a question and an answer, analyze:\n"
        "- Whether the answer addresses the question\n"
        "- Answer type: direct, partial, over-informative, indirect, or non-answer\n"
        "- The propositional content provided\n"
        "- Any implied or additional information",
        output_format="Respond with JSON:\n"
        "{\n"
        '  "addresses_question": true|false,\n'
        '  "answer_type": "direct|partial|over-informative|indirect|non-answer",\n'
        '  "propositional_content": "<what information was provided>",\n'
        '  "implied_info": ["<implied 1>", "<implied 2>", ...]\n'
        "}",
        include_reasoning=True,
    )

    # Add examples
    template.add_example(
        input='Question: "What time does the store close?"\nAnswer: "It closes at 9pm."',
        output='{"addresses_question": true, "answer_type": "direct", '
        '"propositional_content": "store closes at 9pm", '
        '"implied_info": []}',
        reasoning="This is a direct answer that fully addresses the question by "
        "providing the requested closing time.",
    )

    template.add_example(
        input='Question: "Is the restaurant expensive?"\n'
        'Answer: "It\'s a Michelin star restaurant with entrees starting at $45."',
        output='{"addresses_question": true, "answer_type": "over-informative", '
        '"propositional_content": "restaurant has Michelin star, entrees start at $45", '
        '"implied_info": ["yes, it is expensive", "it is high quality"]}',
        reasoning="This answer provides more information than requested. It doesn't "
        'directly say "yes" but implies expensiveness through concrete details.',
    )

    template.add_example(
        input='Question: "When can we meet?"\nAnswer: "I\'m free next week."',
        output='{"addresses_question": true, "answer_type": "partial", '
        '"propositional_content": "speaker is available next week", '
        '"implied_info": ["specific time still needs to be determined"]}',
        reasoning="This partially addresses the question by narrowing down availability "
        "to next week, but doesn't specify an exact time.",
    )

    return template


def create_reference_resolution_template() -> PromptTemplate:
    """Create a template for resolving references (pronouns, definite descriptions).

    Returns:
        PromptTemplate configured for reference resolution
    """
    template = PromptTemplate(
        name="reference_resolution",
        system_prompt="You are an expert in discourse anaphora and reference resolution. "
        "Your task is to identify referential expressions and link them to their antecedents "
        "in the discourse context.",
        task_description="Given a discourse context and a current utterance:\n"
        "- Identify all referential expressions (pronouns, definite descriptions, demonstratives)\n"
        "- Determine their antecedents from the context\n"
        "- Handle ambiguous cases by providing multiple candidates with confidence scores",
        output_format="Respond with JSON:\n"
        "{\n"
        '  "references": [\n'
        "    {\n"
        '      "expression": "<referential expression>",\n'
        '      "type": "pronoun|definite|demonstrative",\n'
        '      "antecedent": "<most likely antecedent>",\n'
        '      "confidence": <0-1>,\n'
        '      "alternatives": [{"antecedent": "<alt>", "confidence": <0-1>}, ...]\n'
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}",
        include_reasoning=True,
    )

    # Add examples
    template.add_example(
        input='Context: "John went to the store. Mary called him."\nCurrent: "He bought milk."',
        output='{"references": ['
        '{"expression": "He", "type": "pronoun", '
        '"antecedent": "John", "confidence": 0.95, '
        '"alternatives": []}'
        "]}",
        reasoning='The pronoun "He" in the current utterance refers back to John, '
        "who is the male referent in the prior context and the subject of the store visit.",
    )

    template.add_example(
        input='Context: "We have two restaurants available. The Italian one is downtown."\n'
        'Current: "What about the other one?"',
        output='{"references": ['
        '{"expression": "the other one", "type": "definite", '
        '"antecedent": "the non-Italian restaurant", "confidence": 0.9, '
        '"alternatives": []}'
        "]}",
        reasoning='"The other one" refers to the second restaurant mentioned in context, '
        "implicitly the non-Italian one since one was already specified.",
    )

    return template


# Template registry
TEMPLATE_REGISTRY: dict[str, PromptTemplate] = {
    "dialogue_act": create_dialogue_act_template(),
    "question_understanding": create_question_understanding_template(),
    "entity_extraction": create_entity_extraction_template(),
    "semantic_parsing": create_semantic_parsing_template(),
    "answer_parsing": create_answer_parsing_template(),
    "reference_resolution": create_reference_resolution_template(),
}


def get_template(name: str) -> PromptTemplate:
    """Get a template by name from the registry.

    Args:
        name: Template name

    Returns:
        The requested template

    Raises:
        KeyError: If template name is not found
    """
    if name not in TEMPLATE_REGISTRY:
        raise KeyError(
            f"Template '{name}' not found. Available templates: {list(TEMPLATE_REGISTRY.keys())}"
        )

    return TEMPLATE_REGISTRY[name]


def list_templates() -> list[str]:
    """List all available template names.

    Returns:
        List of template names
    """
    return list(TEMPLATE_REGISTRY.keys())
