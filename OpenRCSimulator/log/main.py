"""This module handles the app's logging."""
import subprocess
import threading

from OpenRCSimulator.log.log_controller import LogController


def start_logging_process():
    """Starts the logger in its own separate main thread. The logger attaches using sockets.
    """
    process = subprocess.Popen(
        ["openrc-log"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    threading.Thread(target=process.communicate).start()


def main():
    """Main method to start the app.
    """
    stat = LogController(window_size=(400, 800))
    stat.boot()
