"""Tests for terminal inference."""
import pytest
from src.utils import infer_terminal


def test_lhr_gate_a_terminal_2():
    terminal, reasoning = infer_terminal("LHR", "A12")
    assert terminal == "T2"
    assert "A12" in reasoning


def test_lhr_gate_b_terminal_3():
    terminal, reasoning = infer_terminal("LHR", "B22")
    assert terminal == "T3"


def test_unknown_airport_returns_none():
    terminal, reasoning = infer_terminal("XYZ", "A1")
    assert terminal is None


def test_no_gate_returns_none():
    terminal, reasoning = infer_terminal("LHR", None)
    assert terminal is None
    assert "No gate" in reasoning


def test_cdg_terminal_inference():
    terminal, reasoning = infer_terminal("CDG", "B5")
    assert terminal == "T2A"
