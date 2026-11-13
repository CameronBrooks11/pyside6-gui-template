"""What the widgets on the example pages do.

This is the part to replace with your own application: each method here
answers one of the buttons, boxes or fields on the Bug, Cloud and Android
pages. The window itself (title bar, menu, switching pages) is in
main_window.py.
"""

from PySide6.QtCore import QTimer

from .about import ABOUT_HOME


class ExamplePages:
    def __init__(self, window):
        self.window = window
        self.ui = ui = window.ui

        # Home
        ui.lab_home_main_hed.setText("Profile")
        ui.lab_home_stat_hed.setText("Stat")

        # About > Home. A scroll bar placed in Qt Designer replaces the text
        # edit's own. Make this call once per bar: the text edit takes
        # ownership of it and deletes the one it had before.
        ui.text_about_home.setVerticalScrollBar(ui.vsb_about_home)
        ui.text_about_home.setText(ABOUT_HOME)

        # Bug
        self.progress_timer = QTimer(window)
        self.progress_timer.timeout.connect(self._advance_progress)
        ui.bn_bug_start.clicked.connect(lambda: self.start_progress(ui.comboBox_bug.currentText()))

        # Cloud
        ui.bn_cloud_connect.clicked.connect(self.connect_cloud)
        ui.bn_cloud_clear.clicked.connect(self.clear_cloud)

        # Android > Contact
        self.contact_fields = (
            ui.line_android_name,
            ui.line_android_adress,
            ui.line_android_org,
            ui.line_android_email,
            ui.line_android_ph,
        )
        ui.bn_android_contact_edit.clicked.connect(self.edit_contact)
        ui.bn_android_contact_save.clicked.connect(self.save_contact)
        ui.bn_android_contact_delete.clicked.connect(self.delete_contact)

        # Android > GamePad
        ui.textEdit_gamepad.setVerticalScrollBar(ui.vsb_gamepad)
        ui.textEdit_gamepad.setText("Type Here Something, or paste something here")

        # Android > Clean. `toggled` says whether the box became checked;
        # stateChanged would fire on unchecking too.
        ui.horizontalSlider_2.valueChanged.connect(
            lambda value: print("Slider: Horizontal: ", value)
        )
        ui.checkBox.toggled.connect(
            lambda checked: (
                checked
                and window.error_box.show_error(
                    "Happy to Know you liked the UI", ":/icons/smile.png", "Ok"
                )
            )
        )
        ui.checkBox_2.toggled.connect(
            lambda checked: (
                checked
                and window.error_box.show_error(
                    "Even More Happy to hear this", ":/icons/grin.png", "Ok"
                )
            )
        )

    # ---- Bug: a progress bar driven by a timer ----

    def start_progress(self, number):
        """Fill the progress bar, more slowly the bigger `number` is: 1 ms
        per percent for each million, and never less than 1 ms.

        A timer moves the bar one percent at a time, so the window stays
        responsive while it runs. A loop here would block the window until it
        finished. The one timer is kept and restarted, so a second call does
        not leave a first one running.
        """
        self.ui.bn_bug_start.setEnabled(False)
        self.ui.progressBar_bug.setValue(0)
        self.progress_timer.start(max(1, int(number) // 1000000))

    def _advance_progress(self):
        progress = self.ui.progressBar_bug.value() + 1
        self.ui.progressBar_bug.setValue(progress)
        if progress >= 100:
            self.progress_timer.stop()
            self.ui.bn_bug_start.setEnabled(True)

    # ---- Cloud: three fields and an error box ----

    def connect_cloud(self):
        """Pretend to connect: one hard-coded pair of values succeeds, and
        anything else raises the error box."""
        if self.ui.line_cloud_id.text() == "asd" and self.ui.line_cloud_adress.text() == "1234":
            self.ui.line_cloud_adress.setText("")
            self.ui.line_cloud_id.setText("")
            self.ui.line_cloud_proxy.setText("Connection established")
        else:
            self.window.error_box.show_error(
                "Incorrect Credentials", ":/icons/warning.png", "Retry"
            )

    def clear_cloud(self):
        self.ui.line_cloud_proxy.setText("")
        self.ui.line_cloud_adress.setText("")
        self.ui.line_cloud_id.setText("")

    # ---- Android > Contact: fields that are locked until Edit ----

    def edit_contact(self):
        self._set_contact_editable(True)

    def save_contact(self):
        self._set_contact_editable(False)

    def _set_contact_editable(self, editable):
        for field in self.contact_fields:
            field.setEnabled(editable)
        self.ui.bn_android_contact_save.setEnabled(editable)
        self.ui.bn_android_contact_edit.setEnabled(not editable)
        self.ui.bn_android_contact_share.setEnabled(not editable)
        self.ui.bn_android_contact_delete.setEnabled(not editable)

    def delete_contact(self):
        """Ask first: DialogBox.ask returns True when the right-hand button,
        here Yes, was pressed."""
        if self.window.dialog.ask(
            "Warning",
            "The contact information will be deleted. Do you want to continue?",
            ":/icons/warning.png",
            "Cancel",
            "Yes",
        ):
            for field in self.contact_fields:
                field.setText("")
