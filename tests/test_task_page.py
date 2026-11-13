import pytest

from app.pages.task import TaskPage


@pytest.fixture
def page(qtbot):
    page = TaskPage()
    qtbot.addWidget(page)
    yield page
    page.stop()


def test_a_task_runs_to_the_end(page, qtbot):
    page.step_seconds = 0
    page.ui.steps_spin.setValue(20)
    page.ui.start_button.click()
    assert page.is_running()
    assert not page.ui.start_button.isEnabled()
    assert page.ui.cancel_button.isEnabled()

    qtbot.waitUntil(lambda: not page.is_running())
    assert page.ui.status_label.text() == "Finished"
    assert page.ui.progress_bar.value() == page.ui.progress_bar.maximum() == 20
    assert page.ui.start_button.isEnabled()
    assert not page.ui.cancel_button.isEnabled()


def test_cancel_stops_a_task_part_way(page, qtbot):
    page.step_seconds = 0.01
    page.ui.steps_spin.setValue(1000)
    page.ui.start_button.click()
    qtbot.waitUntil(lambda: page.ui.progress_bar.value() > 0)
    page.ui.cancel_button.click()

    qtbot.waitUntil(lambda: not page.is_running())
    assert page.ui.status_label.text() == "Cancelled"
    assert page.ui.progress_bar.value() < 1000
    assert page.ui.start_button.isEnabled()


def test_a_task_can_be_run_again(page, qtbot):
    page.step_seconds = 0
    page.ui.steps_spin.setValue(5)
    for _ in range(2):
        page.ui.start_button.click()
        qtbot.waitUntil(lambda: not page.is_running())
        assert page.ui.progress_bar.value() == 5


def test_a_stopped_task_does_not_end_the_next_one(page, qtbot):
    page.step_seconds = 0.01
    page.ui.steps_spin.setValue(1000)
    page.start()
    page.stop()
    page.start()
    qtbot.wait(100)  # long enough for the first task's report to arrive
    assert page.is_running()


def test_closing_the_window_stops_a_running_task(window, qtbot):
    page = window.task_page
    page.step_seconds = 0.01
    page.ui.steps_spin.setValue(1000)
    page.ui.start_button.click()
    qtbot.waitUntil(lambda: page.ui.progress_bar.value() > 0)
    window.close()
    assert not page.is_running()
    assert not window.isVisible()
