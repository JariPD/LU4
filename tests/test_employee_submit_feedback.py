import pytest
from scripts.submit_feedback import *

@pytest.fixture
def feedback_app():
    return FeedbackPage(username="testuser", role="qa-tester")

def test_employee_submit_feedback(feedback_app):
    # Arrange
    feedback_app.issue_type.set("Bug")
    feedback_app.priority.set("High")
    feedback_app.description_field.insert("1.0", "The game crashes when saving.")
    feedback_app.title_field.insert("1.0", "Game crash on save")

    # Act
    feedback_app.submit_feedback()

    # Assert
    feedback = dm.load_json(feedback_app.FEEDBACK_FILE)
    assert "Game crash on save" in feedback
    assert feedback["Game crash on save"] == {
        "issue_type": "Bug",
        "priority": "High",
        "description": "The game crashes when saving.",
        "status": "New",
        "assignee": "Unassigned",
        "submitted_by": "testuser"
    }

    # Clean up
    del feedback["Game crash on save"]
    dm.save_json(feedback, feedback_app.FEEDBACK_FILE)