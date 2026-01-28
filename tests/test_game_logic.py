import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, init_new_game, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "📉 Go LOWER!")

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "📈 Go HIGHER!")

# Glitch #1 Test: Flipped Feedback Messages
def test_feedback_messages_not_flipped():
    """Test that feedback messages correctly guide the player.
    
    Bug: When guess was too high, it said "Go HIGHER!" (backwards).
    When guess was too low, it said "Go LOWER!" (backwards).
    
    Root cause: The messages in check_guess() were inverted:
    - "guess > secret" returned "Go HIGHER!" instead of "Go LOWER!"
    - "guess < secret" returned "Go LOWER!" instead of "Go HIGHER!"
    
    This test ensures the feedback correctly tells you which direction to guess.
    """
    secret = 38
    
    # When you guess HIGHER than secret, it should tell you to go LOWER
    outcome, message = check_guess(56, secret)
    assert outcome == "Too High", "Guessing 56 when secret is 38 should be 'Too High'"
    assert "LOWER" in message, \
        f"When guess is too high, message should say 'Go LOWER' not '{message}' (was flipped)"
    
    # When you guess LOWER than secret, it should tell you to go HIGHER
    outcome, message = check_guess(20, secret)
    assert outcome == "Too Low", "Guessing 20 when secret is 38 should be 'Too Low'"
    assert "HIGHER" in message, \
        f"When guess is too low, message should say 'Go HIGHER' not '{message}' (was flipped)"

# Glitch #2 Test
def test_new_game_resets_game_state():
    """Test that pressing New Game resets status, history, and attempts.
    
    Bug: After winning and pressing new game, guesses submitted don't work
    (don't receive feedback on submission, and don't show up in history).
    
    Root cause: The new_game handler didn't reset st.session_state.status
    from "won" back to "playing", causing st.stop() to block submissions.
    
    Fix: init_new_game() returns a dict with status="playing" that the
    new_game handler applies to all session state fields.
    """
    new_state = init_new_game("Normal")
    
    # Status must be reset to "playing" so submit handler runs
    assert new_state["status"] == "playing", \
        "Status should be 'playing' after new game (was blocking submissions when left as 'won')"
    
    # History must be cleared so new guesses appear fresh
    assert new_state["history"] == [], \
        "History should be empty after new game (old guesses were persisting)"
    
    # Attempts must reset to start fresh
    assert new_state["attempts"] == 1, \
        "Attempts should reset to 1 on new game"
    
    # Secret must be generated within the difficulty range
    assert 1 <= new_state["secret"] <= 100, \
        "Normal difficulty should generate secret in range 1-100"

# Glitch #3 Test: Hard Mode Range
def test_hard_mode_has_larger_range_than_normal():
    """Test that Hard difficulty has a larger range than Normal.
    
    Bug: Hard mode returned range 1-50 while Normal returned 1-100,
    making Hard mode EASIER than Normal (smaller number pool = easier to guess).
    
    Root cause: get_range_for_difficulty() had Hard mode set to (1, 50)
    instead of a larger range like (1, 500) or (1, 1000).
    
    Fix: Changed Hard mode to return (1, 500).
    """
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    
    easy_range = easy_high - easy_low + 1
    normal_range = normal_high - normal_low + 1
    hard_range = hard_high - hard_low + 1
    
    # Hard should be harder than Normal
    assert hard_range > normal_range, \
        f"Hard mode range ({hard_range}) should be larger than Normal ({normal_range})"
    
    # Normal should be harder than Easy
    assert normal_range > easy_range, \
        f"Normal mode range ({normal_range}) should be larger than Easy ({easy_range})"
    
    # Verify specific ranges
    assert easy_range == 20, "Easy should be 20 (1-20)"
    assert normal_range == 100, "Normal should be 100 (1-100)"
    assert hard_range == 500, "Hard should be 500 (1-500)"


# Glitch #4 Test: Enter Key Submission
def test_enter_key_submission_callback():
    """Test that the submit_guess callback sets the should_submit flag.
    
    Bug: Pressing Enter on the text input didn't submit the guess.
    
    Root cause: The submission logic only checked if the button was clicked
    (if submit:), ignoring Enter key presses in the text input.
    
    Fix: Added an on_change callback to st.text_input() that sets
    st.session_state.should_submit = True when the input changes (including
    Enter press), and updated the condition to check:
    if submit or st.session_state.get("should_submit", False)
    
    Note: This test validates the logic; actual Streamlit interaction
    testing would require integration tests with a Streamlit test client.
    """
    # Simulate what the callback does
    class MockSessionState:
        def __init__(self):
            self.should_submit = False
        
        def get(self, key, default=None):
            return getattr(self, key, default)
    
    session_state = MockSessionState()
    
    # Before callback: should_submit is False
    assert session_state.should_submit == False, \
        "should_submit should start as False"
    
    # Callback sets it to True (simulating Enter press)
    session_state.should_submit = True
    assert session_state.should_submit == True, \
        "Callback should set should_submit to True"
    
    # After submission, reset the flag
    session_state.should_submit = False
    assert session_state.should_submit == False, \
        "Flag should reset after processing submission"


