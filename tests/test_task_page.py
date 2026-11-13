import time

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
    assert not page.ui.steps_spin.isEnabled()
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
    assert not page.ui.cancel_button.isEnabled()

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
    time.sleep(0.1)  # the first task makes progress that is not yet delivered
    page.stop()
    page.step_seconds = 0.5
    page.ui.steps_spin.setValue(2)  # short, so a failure here does not hang
    page.start()
    qtbot.wait(100)  # long enough for the first task's reports to arrive
    assert page.is_running()
    assert page.ui.progress_bar.value() == 0


def test_a_late_report_does_not_relabel_a_stopped_task(page, qtbot):
    page.step_seconds = 0
    page.ui.steps_spin.setValue(3)
    page.start()
    time.sleep(0.2)  # the task ends, and its report waits for the event loop
    page.stop()
    qtbot.wait(50)
    assert page.ui.status_label.text() == "Cancelled"


def test_start_does_nothing_while_a_task_is_running(page, qtbot):
    page.step_seconds = 0.01
    page.ui.steps_spin.setValue(1000)
    page.start()
    qtbot.waitUntil(lambda: page.ui.progress_bar.value() > 0)
    page.start()
    assert page.ui.progress_bar.value() > 0


def test_closing_the_window_stops_a_running_task(window, qtbot):
    page = window.task_page
    page.step_seconds = 0.01
    page.ui.steps_spin.setValue(1000)
    page.ui.start_button.click()
    qtbot.waitUntil(lambda: page.ui.progress_bar.value() > 0)
    started = time.monotonic()
    window.close()
    assert time.monotonic() - started < 2  # stopped, not waited out: that takes 10 s
    assert not page.is_running()
    assert not window.isVisible()
