import pytest
from unittest.mock import MagicMock, patch

from metaflow.plugins.cards.card_server import cards_for_run

@patch('metaflow.plugins.cards.card_server.cards_for_task')
def test_cards_for_run_stopiteration(mock_cards_for_task):
    """
    Test that cards_for_run gracefully returns instead of raising StopIteration
    when max_cards is reached, preventing PEP 479 RuntimeErrors.
    """
    def mock_generator(*args, **kwargs):
        for i in range(5):
            yield f"dummy_card_{i}"
            
    mock_cards_for_task.return_value = mock_generator()

    mock_task = MagicMock()
    mock_task.finished = True
    mock_task.pathspec = "mock/pathspec"
    
    mock_step = MagicMock()
    mock_step.tasks.return_value = [mock_task]
    
    mock_run = MagicMock()
    mock_run.steps.return_value = [mock_step]

    result_generator = cards_for_run(
        flow_datastore=None,
        run_object=mock_run,
        only_running=False,
        max_cards=2
    )

    results = list(result_generator)
    
    assert len(results) == 2
    assert results[0][1] == "dummy_card_0"
    assert results[1][1] == "dummy_card_1"