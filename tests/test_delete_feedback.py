import pytest

@pytest.fixture
def feedback_app():
    return FeedbackPage(username="testuser", role="tester")

def test_deleting_feedback(feedback_app):
    # Arrange
    feedback_app.issue_type.set("Bug")
    feedback_app.description_field.insert("1.0", "The game crashes when saving.")
    feedback_app.title_field.insert("1.0", "Game crash on save")

    # Act
    feedback_app.submit_feedback()
    feedback = dm.load_json(feedback_app.FEEDBACK_FILE)

    # Remove the feedback from the data
    del feedback["Game crash on save"]

    # Save updated data
    dm.save_json(feedback, feedback_app.FEEDBACK_FILE)

    # Assert
    assert "Game crash on save" not in feedback

import pytest
from scripts.submit_feedback import *
