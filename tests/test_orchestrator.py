"""Orchestrator module tests"""

import pytest
from orchestrator.context import extract_context
from orchestrator.tools import pick_tool_from_intent
from orchestrator.params import extract_tool_params

def test_context_extraction():
    """Test context analysis"""
    # This will use the fallback since we don't have real API key in tests
    result = extract_context("I need help with math")
    
    assert "intent" in result
    assert "topic" in result
    assert "emotional_state" in result

def test_tool_selection():
    """Test tool selection logic"""
    assert pick_tool_from_intent("I need practice problems") == "quiz_generator"
    assert pick_tool_from_intent("Explain this concept") == "concept_explainer"
    assert pick_tool_from_intent("Make notes") == "note_maker"

def test_parameter_extraction():
    """Test parameter extraction"""
    tool, params = extract_tool_params("practice", "math", "frustrated")
    
    assert tool == "quiz_generator"
    assert params["difficulty"] == "easy"  # Frustrated emotion should make it easy
    assert params["topic"] == "math"
