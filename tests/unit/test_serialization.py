"""Unit tests for serialization and deserialization."""

import json
import tempfile
from pathlib import Path

from ibdm.core import (
    AltQuestion,
    Answer,
    DialogueMove,
    InformationState,
    Plan,
    WhQuestion,
    YNQuestion,
)
from ibdm.persistence import (
    answer_to_dict,
    dialogue_move_to_dict,
    dict_to_answer,
    dict_to_dialogue_move,
    dict_to_information_state,
    dict_to_plan,
    dict_to_question,
    information_state_to_dict,
    information_state_to_json,
    json_to_information_state,
    load_information_state,
    plan_to_dict,
    question_to_dict,
    save_information_state,
)


class TestQuestionSerialization:
    """Tests for Question serialization."""

    def test_wh_question_to_dict(self):
        """Test converting WhQuestion to dict."""
        q = WhQuestion(variable="x", predicate="weather(x)", constraints={"location": "Stockholm"})
        d = question_to_dict(q)

        assert d["type"] == "WhQuestion"
        assert d["variable"] == "x"
        assert d["predicate"] == "weather(x)"
        assert d["constraints"] == {"location": "Stockholm"}

    def test_yn_question_to_dict(self):
        """Test converting YNQuestion to dict."""
        q = YNQuestion(proposition="raining", parameters={"location": "Stockholm"})
        d = question_to_dict(q)

        assert d["type"] == "YNQuestion"
        assert d["proposition"] == "raining"
        assert d["parameters"] == {"location": "Stockholm"}

    def test_alt_question_to_dict(self):
        """Test converting AltQuestion to dict."""
        q = AltQuestion(alternatives=["tea", "coffee", "water"])
        d = question_to_dict(q)

        assert d["type"] == "AltQuestion"
        assert d["alternatives"] == ["tea", "coffee", "water"]

    def test_dict_to_wh_question(self):
        """Test converting dict to WhQuestion."""
        d = {
            "type": "WhQuestion",
            "variable": "x",
            "predicate": "weather(x)",
            "constraints": {"location": "Stockholm"},
        }
        q = dict_to_question(d)

        assert isinstance(q, WhQuestion)
        assert q.variable == "x"
        assert q.predicate == "weather(x)"
        assert q.constraints == {"location": "Stockholm"}

    def test_dict_to_yn_question(self):
        """Test converting dict to YNQuestion."""
        d = {
            "type": "YNQuestion",
            "proposition": "raining",
            "parameters": {"location": "Stockholm"},
        }
        q = dict_to_question(d)

        assert isinstance(q, YNQuestion)
        assert q.proposition == "raining"
        assert q.parameters == {"location": "Stockholm"}

    def test_dict_to_alt_question(self):
        """Test converting dict to AltQuestion."""
        d = {"type": "AltQuestion", "alternatives": ["tea", "coffee"]}
        q = dict_to_question(d)

        assert isinstance(q, AltQuestion)
        assert q.alternatives == ["tea", "coffee"]

    def test_question_roundtrip(self):
        """Test question serialization roundtrip."""
        original = WhQuestion(variable="x", predicate="test(x)")
        d = question_to_dict(original)
        restored = dict_to_question(d)

        assert isinstance(restored, WhQuestion)
        assert restored.variable == original.variable
        assert restored.predicate == original.predicate


class TestAnswerSerialization:
    """Tests for Answer serialization."""

    def test_answer_to_dict(self):
        """Test converting Answer to dict."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        a = Answer(content="sunny", question_ref=q, certainty=0.9)
        d = answer_to_dict(a)

        assert d["content"] == "sunny"
        assert d["certainty"] == 0.9
        assert d["question_ref"]["type"] == "WhQuestion"

    def test_answer_to_dict_no_question_ref(self):
        """Test converting Answer without question_ref to dict."""
        a = Answer(content="sunny")
        d = answer_to_dict(a)

        assert d["content"] == "sunny"
        assert d["question_ref"] is None
        assert d["certainty"] == 1.0

    def test_dict_to_answer(self):
        """Test converting dict to Answer."""
        d = {
            "content": "sunny",
            "question_ref": {
                "type": "WhQuestion",
                "variable": "x",
                "predicate": "weather(x)",
                "constraints": {},
            },
            "certainty": 0.9,
        }
        a = dict_to_answer(d)

        assert a.content == "sunny"
        assert a.certainty == 0.9
        assert isinstance(a.question_ref, WhQuestion)

    def test_answer_roundtrip(self):
        """Test answer serialization roundtrip."""
        original = Answer(content="test_value", certainty=0.8)
        d = answer_to_dict(original)
        restored = dict_to_answer(d)

        assert restored.content == original.content
        assert restored.certainty == original.certainty


class TestDialogueMoveSerialization:
    """Tests for DialogueMove serialization."""

    def test_dialogue_move_to_dict_simple(self):
        """Test converting DialogueMove with simple content to dict."""
        m = DialogueMove(move_type="greet", content="Hello", speaker="user", timestamp=123.45)
        d = dialogue_move_to_dict(m)

        assert d["move_type"] == "greet"
        assert d["content"] == "Hello"
        assert d["speaker"] == "user"
        assert d["timestamp"] == 123.45

    def test_dialogue_move_to_dict_with_question(self):
        """Test converting DialogueMove with Question content to dict."""
        q = WhQuestion(variable="x", predicate="test(x)")
        m = DialogueMove(move_type="ask", content=q, speaker="user", timestamp=123.45)
        d = dialogue_move_to_dict(m)

        assert d["move_type"] == "ask"
        assert isinstance(d["content"], dict)
        assert d["content"]["type"] == "WhQuestion"

    def test_dialogue_move_to_dict_with_answer(self):
        """Test converting DialogueMove with Answer content to dict."""
        a = Answer(content="sunny")
        m = DialogueMove(move_type="answer", content=a, speaker="system", timestamp=123.45)
        d = dialogue_move_to_dict(m)

        assert d["move_type"] == "answer"
        assert isinstance(d["content"], dict)
        assert d["content"]["content"] == "sunny"

    def test_dict_to_dialogue_move(self):
        """Test converting dict to DialogueMove."""
        d = {
            "move_type": "greet",
            "content": "Hello",
            "speaker": "user",
            "timestamp": 123.45,
        }
        m = dict_to_dialogue_move(d)

        assert m.move_type == "greet"
        assert m.content == "Hello"
        assert m.speaker == "user"
        assert m.timestamp == 123.45

    def test_dialogue_move_roundtrip(self):
        """Test dialogue move serialization roundtrip."""
        q = WhQuestion(variable="x", predicate="test(x)")
        original = DialogueMove(move_type="ask", content=q, speaker="user", timestamp=123.45)
        d = dialogue_move_to_dict(original)
        restored = dict_to_dialogue_move(d)

        assert restored.move_type == original.move_type
        assert restored.speaker == original.speaker
        assert restored.timestamp == original.timestamp
        assert isinstance(restored.content, WhQuestion)


class TestPlanSerialization:
    """Tests for Plan serialization."""

    def test_plan_to_dict(self):
        """Test converting Plan to dict."""
        q = WhQuestion(variable="x", predicate="test(x)")
        p = Plan(plan_type="findout", content=q, status="active")
        d = plan_to_dict(p)

        assert d["plan_type"] == "findout"
        assert d["status"] == "active"
        assert isinstance(d["content"], dict)
        assert d["content"]["type"] == "WhQuestion"
        assert d["subplans"] == []

    def test_plan_to_dict_with_subplans(self):
        """Test converting Plan with subplans to dict."""
        q1 = WhQuestion(variable="x", predicate="test(x)")
        q2 = WhQuestion(variable="y", predicate="check(y)")
        subplan = Plan(plan_type="findout", content=q2)
        p = Plan(plan_type="raise", content=q1, subplans=[subplan])
        d = plan_to_dict(p)

        assert len(d["subplans"]) == 1
        assert d["subplans"][0]["plan_type"] == "findout"

    def test_dict_to_plan(self):
        """Test converting dict to Plan."""
        d = {
            "plan_type": "findout",
            "content": {
                "type": "WhQuestion",
                "variable": "x",
                "predicate": "test(x)",
                "constraints": {},
            },
            "status": "active",
            "subplans": [],
        }
        p = dict_to_plan(d)

        assert p.plan_type == "findout"
        assert p.status == "active"
        assert isinstance(p.content, WhQuestion)
        assert p.subplans == []

    def test_plan_roundtrip(self):
        """Test plan serialization roundtrip."""
        q = WhQuestion(variable="x", predicate="test(x)")
        original = Plan(plan_type="findout", content=q)
        d = plan_to_dict(original)
        restored = dict_to_plan(d)

        assert restored.plan_type == original.plan_type
        assert restored.status == original.status
        assert isinstance(restored.content, WhQuestion)


class TestInformationStateSerialization:
    """Tests for InformationState serialization."""

    def test_information_state_to_dict_empty(self):
        """Test converting empty InformationState to dict."""
        state = InformationState(agent_id="test_agent")
        d = information_state_to_dict(state)

        assert d["agent_id"] == "test_agent"
        assert d["private"]["plan"] == []
        assert d["private"]["agenda"] == []
        assert d["private"]["beliefs"] == {}
        assert d["shared"]["qud"] == []
        assert d["shared"]["commitments"] == []
        assert d["control"]["speaker"] == "user"

    def test_information_state_to_dict_with_data(self):
        """Test converting InformationState with data to dict."""
        state = InformationState(agent_id="test_agent")
        q = WhQuestion(variable="x", predicate="test(x)")
        state.shared.push_qud(q)
        state.private.beliefs["key"] = "value"
        state.shared.commitments.add("test_commitment")

        d = information_state_to_dict(state)

        assert len(d["shared"]["qud"]) == 1
        assert d["shared"]["qud"][0]["type"] == "WhQuestion"
        assert d["private"]["beliefs"]["key"] == "value"
        assert "test_commitment" in d["shared"]["commitments"]

    def test_dict_to_information_state(self):
        """Test converting dict to InformationState."""
        d = {
            "agent_id": "test_agent",
            "private": {"plan": [], "agenda": [], "beliefs": {}, "last_utterance": None},
            "shared": {"qud": [], "commitments": [], "last_moves": []},
            "control": {
                "speaker": "user",
                "next_speaker": "system",
                "initiative": "mixed",
                "dialogue_state": "active",
            },
        }
        state = dict_to_information_state(d)

        assert state.agent_id == "test_agent"
        assert len(state.shared.qud) == 0
        assert len(state.private.plan) == 0
        assert state.control.speaker == "user"

    def test_information_state_roundtrip(self):
        """Test information state serialization roundtrip."""
        original = InformationState(agent_id="test_agent")
        q = WhQuestion(variable="x", predicate="weather(x)")
        original.shared.push_qud(q)
        original.private.beliefs["test"] = "value"

        d = information_state_to_dict(original)
        restored = dict_to_information_state(d)

        assert restored.agent_id == original.agent_id
        assert len(restored.shared.qud) == 1
        assert isinstance(restored.shared.qud[0], WhQuestion)
        assert restored.private.beliefs["test"] == "value"

    def test_information_state_to_json(self):
        """Test converting InformationState to JSON."""
        state = InformationState(agent_id="test_agent")
        json_str = information_state_to_json(state)

        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data["agent_id"] == "test_agent"

    def test_json_to_information_state(self):
        """Test converting JSON to InformationState."""
        json_str = """
        {
            "agent_id": "test_agent",
            "private": {
                "plan": [],
                "agenda": [],
                "beliefs": {},
                "last_utterance": null
            },
            "shared": {
                "qud": [],
                "commitments": [],
                "last_moves": []
            },
            "control": {
                "speaker": "user",
                "next_speaker": "system",
                "initiative": "mixed",
                "dialogue_state": "active"
            }
        }
        """
        state = json_to_information_state(json_str)

        assert state.agent_id == "test_agent"
        assert len(state.shared.qud) == 0

    def test_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        original = InformationState(agent_id="test_agent")
        q = YNQuestion(proposition="test")
        original.shared.push_qud(q)

        json_str = information_state_to_json(original)
        restored = json_to_information_state(json_str)

        assert restored.agent_id == original.agent_id
        assert len(restored.shared.qud) == 1
        assert isinstance(restored.shared.qud[0], YNQuestion)


class TestFilePersistence:
    """Tests for file-based persistence."""

    def test_save_and_load_information_state(self):
        """Test saving and loading InformationState to/from file."""
        original = InformationState(agent_id="test_agent")
        q = WhQuestion(variable="x", predicate="test(x)")
        original.shared.push_qud(q)
        original.private.beliefs["key"] = "value"

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "state.json"
            save_information_state(original, str(filepath))

            assert filepath.exists()

            restored = load_information_state(str(filepath))

            assert restored.agent_id == original.agent_id
            assert len(restored.shared.qud) == 1
            assert isinstance(restored.shared.qud[0], WhQuestion)
            assert restored.private.beliefs["key"] == "value"

    def test_save_complex_state(self):
        """Test saving a complex InformationState."""
        state = InformationState(agent_id="complex_agent")

        # Add questions
        q1 = WhQuestion(variable="x", predicate="weather(x)")
        q2 = YNQuestion(proposition="raining")
        state.shared.push_qud(q1)
        state.shared.push_qud(q2)

        # Add plans
        plan = Plan(plan_type="findout", content=q1)
        state.private.plan.append(plan)

        # Add moves
        move = DialogueMove(move_type="ask", content=q1, speaker="user", timestamp=123.45)
        state.shared.last_moves.append(move)

        # Add beliefs
        state.private.beliefs["weather_data"] = {"temp": 20, "condition": "sunny"}

        # Add commitments
        state.shared.commitments.add("weather(sunny)")

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "complex_state.json"
            save_information_state(state, str(filepath))

            restored = load_information_state(str(filepath))

            assert len(restored.shared.qud) == 2
            assert len(restored.private.plan) == 1
            assert len(restored.shared.last_moves) == 1
            assert "weather_data" in restored.private.beliefs
            assert "weather(sunny)" in restored.shared.commitments
