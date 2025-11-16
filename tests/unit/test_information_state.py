"""Unit tests for Information State classes."""

from ibdm.core import (
    Answer,
    ControlIS,
    DialogueMove,
    InformationState,
    Plan,
    PrivateIS,
    SharedIS,
    WhQuestion,
    YNQuestion,
)


class TestPrivateIS:
    """Tests for PrivateIS class."""

    def test_creation(self):
        """Test creating a PrivateIS."""
        private = PrivateIS()
        assert private.plan == []
        assert private.agenda == []
        assert private.beliefs == {}
        assert private.last_utterance is None
        assert private.issues == []  # IBiS3

    def test_creation_with_plans(self):
        """Test creating a PrivateIS with plans."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        plan = Plan(plan_type="findout", content=q)
        private = PrivateIS(plan=[plan])
        assert len(private.plan) == 1
        assert private.plan[0] == plan

    def test_creation_with_agenda(self):
        """Test creating a PrivateIS with agenda."""
        move = DialogueMove(move_type="greet", content="hello", speaker="system")
        private = PrivateIS(agenda=[move])
        assert len(private.agenda) == 1
        assert private.agenda[0] == move

    def test_creation_with_beliefs(self):
        """Test creating a PrivateIS with beliefs."""
        beliefs = {"weather": "sunny", "temperature": 20}
        private = PrivateIS(beliefs=beliefs)
        assert private.beliefs == beliefs

    def test_creation_with_issues(self):
        """Test creating a PrivateIS with issues (IBiS3)."""
        q1 = WhQuestion(variable="x", predicate="parties(x)")
        q2 = WhQuestion(variable="y", predicate="effective_date(y)")
        private = PrivateIS(issues=[q1, q2])
        assert len(private.issues) == 2
        assert private.issues[0] == q1
        assert private.issues[1] == q2

    def test_str_representation(self):
        """Test string representation."""
        private = PrivateIS()
        s = str(private)
        assert "PrivateIS" in s

    def test_str_representation_with_issues(self):
        """Test string representation with issues (IBiS3)."""
        q = WhQuestion(variable="x", predicate="parties(x)")
        private = PrivateIS(issues=[q])
        s = str(private)
        assert "PrivateIS" in s
        assert "issues=1" in s

    def test_serialization_with_issues(self):
        """Test serialization and deserialization of PrivateIS with issues (IBiS3)."""
        q1 = WhQuestion(variable="x", predicate="parties(x)")
        q2 = YNQuestion(proposition="is_nda")
        private = PrivateIS(issues=[q1, q2], beliefs={"test": "value"})

        # Serialize
        data = private.to_dict()
        assert "issues" in data
        assert len(data["issues"]) == 2

        # Deserialize
        reconstructed = PrivateIS.from_dict(data)
        assert len(reconstructed.issues) == 2
        assert reconstructed.beliefs == {"test": "value"}
        # Questions should be reconstructed correctly
        assert isinstance(reconstructed.issues[0], WhQuestion)
        assert isinstance(reconstructed.issues[1], YNQuestion)


class TestSharedIS:
    """Tests for SharedIS class."""

    def test_creation(self):
        """Test creating a SharedIS."""
        shared = SharedIS()
        assert shared.qud == []
        assert shared.commitments == set()
        assert shared.last_moves == []
        assert shared.moves == []  # IBiS2
        assert shared.next_moves == []  # IBiS2

    def test_push_qud(self):
        """Test pushing a question onto QUD stack."""
        shared = SharedIS()
        q = WhQuestion(variable="x", predicate="weather(x)")
        shared.push_qud(q)
        assert len(shared.qud) == 1
        assert shared.qud[0] == q

    def test_push_multiple_qud(self):
        """Test pushing multiple questions onto QUD stack."""
        shared = SharedIS()
        q1 = WhQuestion(variable="x", predicate="weather(x)")
        q2 = YNQuestion(proposition="raining")
        shared.push_qud(q1)
        shared.push_qud(q2)
        assert len(shared.qud) == 2
        assert shared.qud[0] == q1
        assert shared.qud[1] == q2

    def test_pop_qud(self):
        """Test popping a question from QUD stack."""
        shared = SharedIS()
        q = WhQuestion(variable="x", predicate="weather(x)")
        shared.push_qud(q)
        popped = shared.pop_qud()
        assert popped == q
        assert len(shared.qud) == 0

    def test_pop_qud_empty(self):
        """Test popping from empty QUD stack."""
        shared = SharedIS()
        popped = shared.pop_qud()
        assert popped is None

    def test_top_qud(self):
        """Test getting top of QUD stack without removing."""
        shared = SharedIS()
        q1 = WhQuestion(variable="x", predicate="weather(x)")
        q2 = YNQuestion(proposition="raining")
        shared.push_qud(q1)
        shared.push_qud(q2)
        top = shared.top_qud()
        assert top == q2
        assert len(shared.qud) == 2  # Stack unchanged

    def test_top_qud_empty(self):
        """Test getting top of empty QUD stack."""
        shared = SharedIS()
        top = shared.top_qud()
        assert top is None

    def test_commitments(self):
        """Test shared commitments."""
        shared = SharedIS()
        shared.commitments.add("weather(sunny)")
        shared.commitments.add("temperature(20)")
        assert len(shared.commitments) == 2
        assert "weather(sunny)" in shared.commitments

    def test_str_representation(self):
        """Test string representation."""
        shared = SharedIS()
        s = str(shared)
        assert "SharedIS" in s

    def test_str_representation_with_qud(self):
        """Test string representation with QUD."""
        shared = SharedIS()
        q = WhQuestion(variable="x", predicate="weather(x)")
        shared.push_qud(q)
        s = str(shared)
        assert "SharedIS" in s
        assert "qud=1" in s

    def test_creation_with_moves(self):
        """Test creating a SharedIS with moves (IBiS2)."""
        move1 = DialogueMove(move_type="ask", content="What is the weather?", speaker="user")
        move2 = DialogueMove(move_type="answer", content="Sunny", speaker="system")
        shared = SharedIS(moves=[move1, move2])
        assert len(shared.moves) == 2
        assert shared.moves[0] == move1
        assert shared.moves[1] == move2

    def test_creation_with_next_moves(self):
        """Test creating a SharedIS with next_moves (IBiS2)."""
        move1 = DialogueMove(move_type="ask", content="What is your name?", speaker="system")
        move2 = DialogueMove(move_type="icm", content="confirmation", speaker="system")
        shared = SharedIS(next_moves=[move1, move2])
        assert len(shared.next_moves) == 2
        assert shared.next_moves[0] == move1
        assert shared.next_moves[1] == move2

    def test_serialization_with_grounding_fields(self):
        """Test serialization of SharedIS with IBiS2 grounding fields."""
        # Create moves
        q = WhQuestion(variable="x", predicate="weather(x)")
        move1 = DialogueMove(move_type="ask", content=q, speaker="system")
        move2 = DialogueMove(move_type="answer", content="sunny", speaker="user")

        # Create SharedIS with grounding fields
        shared = SharedIS(moves=[move1, move2], next_moves=[move1], commitments={"weather(sunny)"})

        # Serialize
        data = shared.to_dict()
        assert "moves" in data
        assert "next_moves" in data
        assert len(data["moves"]) == 2
        assert len(data["next_moves"]) == 1

    def test_deserialization_with_grounding_fields(self):
        """Test deserialization of SharedIS with IBiS2 grounding fields."""
        # Create moves with complex content
        q = WhQuestion(variable="x", predicate="parties(x)")
        a = Answer(content="Acme Corp", question_ref=q)
        move1 = DialogueMove(move_type="ask", content=q, speaker="system")
        move2 = DialogueMove(move_type="answer", content=a, speaker="user")

        # Create SharedIS
        shared = SharedIS(
            moves=[move1, move2], next_moves=[move1], commitments={"parties(acme_corp)"}
        )

        # Serialize and deserialize
        data = shared.to_dict()
        reconstructed = SharedIS.from_dict(data)

        # Verify reconstruction
        assert len(reconstructed.moves) == 2
        assert len(reconstructed.next_moves) == 1
        assert reconstructed.commitments == {"parties(acme_corp)"}

        # Verify moves are properly reconstructed
        assert isinstance(reconstructed.moves[0], DialogueMove)
        assert isinstance(reconstructed.moves[1], DialogueMove)
        assert reconstructed.moves[0].move_type == "ask"
        assert reconstructed.moves[1].move_type == "answer"

    def test_grounding_move_history_tracking(self):
        """Test tracking complete move history for grounding (IBiS2)."""
        shared = SharedIS()

        # Simulate dialogue with move tracking
        q1 = WhQuestion(variable="x", predicate="destination(x)")
        move1 = DialogueMove(move_type="ask", content=q1, speaker="system")
        shared.moves.append(move1)

        a1 = Answer(content="Paris", question_ref=q1)
        move2 = DialogueMove(move_type="answer", content=a1, speaker="user")
        shared.moves.append(move2)

        # Verify history
        assert len(shared.moves) == 2
        assert shared.moves[0].speaker == "system"
        assert shared.moves[1].speaker == "user"

    def test_next_moves_queue(self):
        """Test pending system moves queue (IBiS2)."""
        shared = SharedIS()

        # System prepares multiple moves
        q1 = WhQuestion(variable="x", predicate="name(x)")
        move1 = DialogueMove(move_type="ask", content=q1, speaker="system")

        q2 = WhQuestion(variable="y", predicate="age(y)")
        move2 = DialogueMove(move_type="ask", content=q2, speaker="system")

        # Add to next_moves queue
        shared.next_moves.append(move1)
        shared.next_moves.append(move2)

        assert len(shared.next_moves) == 2

        # Pop first move
        next_move = shared.next_moves.pop(0)
        assert next_move == move1
        assert len(shared.next_moves) == 1


class TestControlIS:
    """Tests for ControlIS class."""

    def test_creation(self):
        """Test creating a ControlIS."""
        control = ControlIS()
        assert control.speaker == "user"
        assert control.next_speaker == "system"
        assert control.initiative == "mixed"
        assert control.dialogue_state == "active"

    def test_custom_speaker(self):
        """Test creating a ControlIS with custom speaker."""
        control = ControlIS(speaker="system", next_speaker="user")
        assert control.speaker == "system"
        assert control.next_speaker == "user"

    def test_user_initiative(self):
        """Test setting user initiative."""
        control = ControlIS(initiative="user")
        assert control.initiative == "user"

    def test_system_initiative(self):
        """Test setting system initiative."""
        control = ControlIS(initiative="system")
        assert control.initiative == "system"

    def test_dialogue_states(self):
        """Test different dialogue states."""
        control_active = ControlIS(dialogue_state="active")
        control_paused = ControlIS(dialogue_state="paused")
        control_ended = ControlIS(dialogue_state="ended")
        assert control_active.dialogue_state == "active"
        assert control_paused.dialogue_state == "paused"
        assert control_ended.dialogue_state == "ended"

    def test_str_representation(self):
        """Test string representation."""
        control = ControlIS()
        s = str(control)
        assert "ControlIS" in s
        assert "user" in s
        assert "system" in s


class TestInformationState:
    """Tests for InformationState class."""

    def test_creation(self):
        """Test creating an InformationState."""
        state = InformationState()
        assert isinstance(state.private, PrivateIS)
        assert isinstance(state.shared, SharedIS)
        assert isinstance(state.control, ControlIS)
        assert state.agent_id == "system"

    def test_custom_agent_id(self):
        """Test creating an InformationState with custom agent ID."""
        state = InformationState(agent_id="agent_007")
        assert state.agent_id == "agent_007"

    def test_custom_components(self):
        """Test creating an InformationState with custom components."""
        private = PrivateIS(beliefs={"test": "value"})
        shared = SharedIS()
        control = ControlIS(speaker="agent1")
        state = InformationState(private=private, shared=shared, control=control, agent_id="agent1")
        assert state.private == private
        assert state.shared == shared
        assert state.control == control
        assert state.agent_id == "agent1"

    def test_clone(self):
        """Test cloning an InformationState."""
        state = InformationState()
        q = WhQuestion(variable="x", predicate="weather(x)")
        state.shared.push_qud(q)
        state.private.beliefs["weather"] = "sunny"

        cloned = state.clone()
        assert cloned is not state
        assert cloned.shared is not state.shared
        assert cloned.private is not state.private
        assert cloned.control is not state.control

    def test_clone_independence(self):
        """Test that cloned state is independent."""
        state = InformationState()
        q = WhQuestion(variable="x", predicate="weather(x)")
        state.shared.push_qud(q)

        cloned = state.clone()
        # Modify original
        q2 = YNQuestion(proposition="raining")
        state.shared.push_qud(q2)

        # Cloned should be unchanged
        assert len(state.shared.qud) == 2
        assert len(cloned.shared.qud) == 1

    def test_str_representation(self):
        """Test string representation."""
        state = InformationState(agent_id="test_agent")
        s = str(state)
        assert "InformationState" in s
        assert "test_agent" in s

    def test_complete_dialogue_flow(self):
        """Test a complete dialogue flow with InformationState."""
        # Create information state for system agent
        state = InformationState(agent_id="system")

        # User asks a question
        q = WhQuestion(variable="x", predicate="weather(stockholm, x)")
        state.shared.push_qud(q)
        assert state.shared.top_qud() == q

        # System creates plan to respond
        plan = Plan(plan_type="respond", content=q)
        state.private.plan.append(plan)
        assert len(state.private.plan) == 1

        # System prepares answer move
        answer = Answer(content="sunny", question_ref=q)
        move = DialogueMove(move_type="answer", content=answer, speaker="system")
        state.private.agenda.append(move)
        assert len(state.private.agenda) == 1

        # Answer resolves question
        assert q.resolves_with(answer)

        # Pop QUD after answering
        resolved_q = state.shared.pop_qud()
        assert resolved_q == q
        assert len(state.shared.qud) == 0

        # Add to commitments
        state.shared.commitments.add("weather(stockholm, sunny)")
        assert "weather(stockholm, sunny)" in state.shared.commitments
