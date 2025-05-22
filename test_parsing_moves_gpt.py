import pytest
from gptchess.parsing_moves_gpt import extract_move_deepseek

def test_extract_move_deepseek_withGPT4():
    def run_test_case(resp_str, expected_result):
        result = extract_move_deepseek_withGPT4(resp_str)
        assert result == expected_result, f"Expected '{expected_result}', but got '{result}'"

    # Test cases
    run_test_case(
        resp_str="Got it! You played **1...d6**, which can lead into the Pirc Defense or Philidor's Defense. I'll continue with **2. d4**, expanding in the center. Your turn! 🏰",
        expected_result="d4"
    )

    # New test case
    run_test_case(
        resp_str="1. e4\n\nYour move! Let's see how the game unfolds. Are you responding with 1...e5, 1...c5 (Sicilian), or something else? 😊",
        expected_result="e4"
    )

def test_extract_move_deepseek():
    def run_test_case(resp_str, expected_result):
        result = extract_move_deepseek(resp_str)
        assert result == expected_result, f"Expected '{expected_result}', but got '{result}'"
    
    run_test_case(
        resp_str="<played_move>5. Qg4</played_move>",
        expected_result="Qg4"
    )

test_extract_move_deepseek()
# To run the tests, use the command: pytest test_parsing_moves_gpt.py 
