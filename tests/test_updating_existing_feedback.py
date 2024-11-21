import pytest
from scripts.feedback_overview import *

@pytest.fixture
def reset_feedback_file():
    """Fixture to reset feedback.json before each test"""
    # Create a clean feedback dictionary
    initial_feedback = {
        "Test Feedback 1": {
            "issue_type": "Bug",
            "priority": "Low",
            "description": "Initial test description",
            "status": "New",
            "assignee": "Unassigned",
            "submitted_by": "testuser"
        }
    }
    dm.save_json(initial_feedback, "feedback.json")

@pytest.mark.parametrize("role,expected_can_edit_priority", [
    ('manager', True),
    ('qa-tester', True),
    ('developer', False),
])
def test_priority_edit_permissions(role, expected_can_edit_priority, reset_feedback_file):
    """Test priority editing permissions for different roles"""
    app = FeedbackOverview(role=role)
    app.load_feedback()

    # Get the first feedback card (first title in the dictionary)
    first_title = list(dm.load_json("feedback.json").keys())[0]
    feedback_data = dm.load_json("feedback.json")[first_title]

    # Attempt to edit priority
    new_priority = "High"
    priority_var = tk.StringVar(value=new_priority)

    # Simulate saving changes
    app.save_changes(
        first_title,
        priority_var,
        tk.StringVar(value=feedback_data['status']),
        tk.StringVar(value=feedback_data['issue_type']),
        tk.StringVar(value=feedback_data['assignee']),
        tk.Text(app)
    )

    # Reload feedback and verify changes
    updated_feedback = dm.load_json("feedback.json")[first_title]

    if expected_can_edit_priority:
        assert updated_feedback['priority'] == new_priority
    else:
        assert updated_feedback['priority'] == feedback_data['priority']

@pytest.mark.parametrize("role,expected_can_edit_status", [
    ('manager', True),
    ('developer', True),
    ('qa-tester', False),
])
def test_status_edit_permissions(role, expected_can_edit_status, reset_feedback_file):
    """Test status editing permissions for different roles"""
    app = FeedbackOverview(role=role)
    app.load_feedback()

    # Get the first feedback card (first title in the dictionary)
    first_title = list(dm.load_json("feedback.json").keys())[0]
    feedback_data = dm.load_json("feedback.json")[first_title]

    # Attempt to edit status
    new_status = "Resolved"
    status_var = tk.StringVar(value=new_status)

    # Simulate saving changes
    app.save_changes(
        first_title,
        tk.StringVar(value=feedback_data['priority']),
        status_var,
        tk.StringVar(value=feedback_data['issue_type']),
        tk.StringVar(value=feedback_data['assignee']),
        tk.Text(app)
    )

    # Reload feedback and verify changes
    updated_feedback = dm.load_json("feedback.json")[first_title]

    if expected_can_edit_status:
        assert updated_feedback['status'] == new_status
    else:
        assert updated_feedback['status'] == feedback_data['status']


@pytest.mark.parametrize("role,expected_can_edit_assignee", [
    ('manager', True),
    ('developer', True),
    ('qa-tester', False),
])
def test_assignee_edit_permissions(role, expected_can_edit_assignee, reset_feedback_file):
    """Test assignee editing permissions for different roles"""
    app = FeedbackOverview(role=role)
    app.load_feedback()

    # Get the first feedback card (first title in the dictionary)
    first_title = list(dm.load_json("feedback.json").keys())[0]
    feedback_data = dm.load_json("feedback.json")[first_title]

    # Attempt to edit assignee
    new_assignee = "Jari"
    assignee_var = tk.StringVar(value=new_assignee)

    # Simulate saving changes
    app.save_changes(
        first_title,
        tk.StringVar(value=feedback_data['priority']),
        tk.StringVar(value=feedback_data['status']),
        tk.StringVar(value=feedback_data['issue_type']),
        assignee_var,
        tk.Text(app)
    )

    # Reload feedback and verify changes
    updated_feedback = dm.load_json("feedback.json")[first_title]

    if expected_can_edit_assignee:
        assert updated_feedback['assignee'] == new_assignee
    else:
        assert updated_feedback['assignee'] == feedback_data['assignee']

def test_sorting_functionality(reset_feedback_file):
    """Test sorting functionality of feedback overview"""
    # Prepare test data with different priorities
    test_feedback = {
        "Low Priority Feedback": {"priority": "Low"},
        "Critical Priority Feedback": {"priority": "Critical"},
        "High Priority Feedback": {"priority": "High"},
        "Medium Priority Feedback": {"priority": "Medium"}
    }
    dm.save_json(test_feedback, "feedback.json")

    # Test ascending sort
    app_ascending = FeedbackOverview(role='manager')
    app_ascending.sort_ascending.set(True)
    sorted_feedback_ascending = app_ascending.sort_feedback_by_priority(test_feedback)
    ascending_order = list(sorted_feedback_ascending.keys())
    assert ascending_order == [
        "Critical Priority Feedback",
        "High Priority Feedback",
        "Medium Priority Feedback",
        "Low Priority Feedback"
    ]

    # Test descending sort
    app_descending = FeedbackOverview(role='manager')
    app_descending.sort_ascending.set(False)
    sorted_feedback_descending = app_descending.sort_feedback_by_priority(test_feedback)
    descending_order = list(sorted_feedback_descending.keys())
    assert descending_order == [
        "Low Priority Feedback",
        "Medium Priority Feedback",
        "High Priority Feedback",
        "Critical Priority Feedback"
    ]