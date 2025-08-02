import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QTime, QDateTime
from PyQt5.QtMultimedia import QSound
from PyQt5 import uic
import os


class AlarmClock(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('alarm_clock.ui', self)

        # Initialize variables
        self.alarm_time = None
        self.alarm_active = False
        self.alarm_sound = None

        # Setup timer for clock update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        # Connect buttons
        self.setAlarmButton.clicked.connect(self.set_alarm)
        self.stopAlarmButton.clicked.connect(self.stop_alarm)

        # Initial setup
        self.stopAlarmButton.setEnabled(False)
        self.update_time()

    def update_time(self):
        """Update the current time display"""
        current_time = QDateTime.currentDateTime()
        display_time = current_time.toString('hh:mm:ss')
        self.timeLabel.setText(display_time)

        # Check if alarm should trigger
        if self.alarm_active and self.alarm_time:
            current_qtime = QTime.currentTime()
            if (current_qtime.hour() == self.alarm_time.hour() and
                    current_qtime.minute() == self.alarm_time.minute() and
                    current_qtime.second() == self.alarm_time.second()):
                self.trigger_alarm()

    def set_alarm(self):
        """Set the alarm"""
        self.alarm_time = self.alarmTimeEdit.time()
        self.alarm_active = True

        # Update UI
        self.statusLabel.setText(f"Alarm set for {self.alarm_time.toString('hh:mm:ss')}")
        self.statusLabel.setStyleSheet("color: green;")
        self.setAlarmButton.setText("Cancel Alarm")
        self.setAlarmButton.clicked.disconnect()
        self.setAlarmButton.clicked.connect(self.cancel_alarm)

    def cancel_alarm(self):
        """Cancel the alarm"""
        self.alarm_active = False
        self.alarm_time = None

        # Update UI
        self.statusLabel.setText("Alarm cancelled")
        self.statusLabel.setStyleSheet("color: red;")
        self.setAlarmButton.setText("Set Alarm")
        self.setAlarmButton.clicked.disconnect()
        self.setAlarmButton.clicked.connect(self.set_alarm)

    def trigger_alarm(self):
        """Trigger the alarm"""
        self.alarm_active = False

        # Update UI
        self.statusLabel.setText("ALARM RINGING!")
        self.statusLabel.setStyleSheet("color: red; font-weight: bold;")
        self.stopAlarmButton.setEnabled(True)
        self.setAlarmButton.setEnabled(False)

        # Play sound (you'll need a .wav file)
        try:
            # Use QSound for simple playback
            self.alarm_sound = QSound("alarm.wav")  # Add your alarm sound file
            self.alarm_sound.setLoops(-1)  # Loop indefinitely
            self.alarm_sound.play()
        except:
            print("Sound file not found. Add 'alarm.wav' to your project directory.")

    def stop_alarm(self):
        """Stop the ringing alarm"""
        if self.alarm_sound:
            self.alarm_sound.stop()

        # Reset UI
        self.statusLabel.setText("Alarm stopped")
        self.statusLabel.setStyleSheet("color: black;")
        self.stopAlarmButton.setEnabled(False)
        self.setAlarmButton.setEnabled(True)
        self.setAlarmButton.setText("Set Alarm")
        self.setAlarmButton.clicked.disconnect()
        self.setAlarmButton.clicked.connect(self.set_alarm)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = AlarmClock()
    clock.show()
    sys.exit(app.exec_())