# LoadActiveMQ - part of the HACKtiveMQ Suite
# Copyright (C) 2025 Garland Glessner - gglesner@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QFileDialog, QSpacerItem, QSizePolicy, QListWidget, QListWidgetItem
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Qt
import os
import shutil
import subprocess
import threading
import zipfile
import sys
import time
from packaging import version  # Added for version comparison

# Define the version number
VERSION = "1.0.0"

# Define the tab label
TAB_LABEL = f"LoadActiveMQ v{VERSION}"

class Ui_TabContent:
    def setupUi(self, widget, parent):
        """Set up the UI components for the ActiveMQ Loader tab."""
        parent.log_to_status("Setting up UI for ActiveMQ Loader")  # Log directly to StatusTextBox
        widget.setObjectName("TabContent")

        # Main vertical layout
        self.verticalLayout_3 = QVBoxLayout(widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setSpacing(5)

        self.verticalLayout_3.addSpacerItem(QSpacerItem(0, 1, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Header frame with title
        self.frame_8 = QFrame(widget)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.frame_5 = QFrame(self.frame_8)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.horizontalLayout_3.addWidget(self.frame_5)

        self.label_3 = QLabel(self.frame_8)
        font = QFont("Courier New", 14)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.horizontalLayout_3.addWidget(self.label_3)

        # Spacer to push content
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.verticalLayout_3.addWidget(self.frame_8)

        self.verticalLayout_3.addSpacerItem(QSpacerItem(0, 1, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Main content frame for module list
        self.frame_3 = QFrame(widget)
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setStyleSheet("QFrame { border: 2px solid black; }")
        self.verticalLayout_client = QVBoxLayout(self.frame_3)
        self.verticalLayout_client.setContentsMargins(5, 5, 5, 5)

        # ActiveMQ versions list
        self.label_client = QLabel(self.frame_3)
        self.label_client.setText("ActiveMQ Versions:")
        self.verticalLayout_client.addWidget(self.label_client)

        self.ActiveMQList = QListWidget(self.frame_3)
        self.verticalLayout_client.addWidget(self.ActiveMQList)

        self.verticalLayout_3.addWidget(self.frame_3)

        # Status frame at the bottom
        self.frame_4 = QFrame(widget)
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.verticalLayout = QVBoxLayout(self.frame_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.StatusTextBox = QPlainTextEdit(self.frame_4)
        self.StatusTextBox.setReadOnly(True)
        status_font = QFont("Courier New", 10)
        status_font.setFixedPitch(True)
        self.StatusTextBox.setFont(status_font)
        self.verticalLayout.addWidget(self.StatusTextBox)

        self.verticalLayout_3.addWidget(self.frame_4)

        self.retranslateUi(widget)

    def retranslateUi(self, widget):
        """Set up UI text."""
        self.label_3.setText(f"""
 __              _ _____     _   _         _____ _____ 
|  |   ___ ___ _| |  _  |___| |_|_|_ _ ___|     |     |
|  |__| . | .'| . |     |  _|  _| | | | -_| | | |  |  |
|_____|___|__,|___|__|__|___|_| |_|\_/|___|_|_|_|__  _|
                                                   |__|
 Version: {VERSION}""")
        self.label_client.setText("ActiveMQ Versions:")

class TabContent(QWidget):
    def __init__(self):
        """Initialize the TabContent widget."""
        super().__init__()

        # Queue for early logs before StatusTextBox exists
        self.early_logs = []

        # Log initialization (queued until StatusTextBox is ready)
        self.early_logs.append("Initializing ActiveMQ Loader module")

        # Set up UI
        self.ui = Ui_TabContent()
        self.ui.setupUi(self, self)

        # State
        self.current_process = None
        self.current_thread = None
        self.temp_dir = os.path.join("modules", "Load_ActiveMQ", "temp")
        self.current_version = None

        # Create modules/Load_ActiveMQ directory if it doesn't exist
        version_dir = os.path.join("modules", "Load_ActiveMQ")
        try:
            os.makedirs(version_dir, exist_ok=True)
            self.log_to_status(f"Ensured directory exists: {version_dir}")
        except Exception as e:
            self.log_to_status(f"Error creating directory {version_dir}: {e}")

        # Flush early logs to StatusTextBox
        for log in self.early_logs:
            self.log_to_status(log)
        self.early_logs.clear()

        # Log initialization completion
        self.log_to_status(f"ActiveMQ Loader v{VERSION} initialized.")

        # Connect signals
        self.ui.ActiveMQList.itemClicked.connect(self.handle_version_selection)

        # Initialize ActiveMQ versions list
        self.update_version_list()

    def log_to_status(self, message):
        """Log a message to StatusTextBox with autoscroll."""
        if hasattr(self.ui, 'StatusTextBox') and self.ui.StatusTextBox:
            self.ui.StatusTextBox.appendPlainText(message.rstrip())
            self.ui.StatusTextBox.moveCursor(QTextCursor.End)
            self.ui.StatusTextBox.ensureCursorVisible()
        else:
            # Queue message if StatusTextBox isn't ready
            self.early_logs.append(message)

    def update_version_list(self):
        """Update the ActiveMQ versions list, sorted by numerical version number."""
        self.log_to_status("Updating ActiveMQ versions list")
        self.ui.ActiveMQList.clear()
        version_dir = os.path.join("modules", "Load_ActiveMQ")
        if not os.path.exists(version_dir):
            self.log_to_status(f"ActiveMQ directory not found: {version_dir}")
            return

        # Collect zip files and their version numbers
        version_files = []
        for filename in os.listdir(version_dir):
            if filename.endswith(".zip"):
                version_name = filename[:-4]  # Remove .zip
                try:
                    # Extract version number (e.g., "5.9.1" from "apache-activemq-5.9.1-bin")
                    version_parts = version_name.split('-')
                    version_str = version_parts[-2] if version_parts[-1] == 'bin' else version_parts[-1]
                    parsed_version = version.parse(version_str)
                    version_files.append((parsed_version, version_name, filename))
                except Exception as e:
                    self.log_to_status(f"Error parsing version for {version_name}: {e}, using as-is")
                    # Fallback: use version_name as a string for sorting (will sort alphabetically at the end)
                    version_files.append((version_name, version_name, filename))

        # Sort by version number (parsed_version or string for invalid versions)
        version_files.sort(key=lambda x: x[0] if isinstance(x[0], version.Version) else x[1])

        # Add sorted versions to the list
        for _, version_name, filename in version_files:
            item = QListWidgetItem(version_name)
            item.setData(Qt.UserRole, filename)
            self.ui.ActiveMQList.addItem(item)
            self.log_to_status(f"Added version: {version_name}")

        self.log_to_status("Loaded ActiveMQ versions.")

    def run_activemq(self, version_name, zip_path):
        """Extract and run ActiveMQ in a thread."""
        self.log_to_status(f"Running ActiveMQ version: {version_name}")
        try:
            # Clean up existing temp directory
            if os.path.exists(self.temp_dir):
                self.delete_temp_dir_with_retries()

            # Create temp directory
            os.makedirs(self.temp_dir)
            self.log_to_status(f"Created temporary directory: {self.temp_dir}")

            # Extract zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            self.log_to_status(f"Extracted {version_name} to {self.temp_dir}")

            # Find the extracted directory
            extracted_dirs = [d for d in os.listdir(self.temp_dir) if os.path.isdir(os.path.join(self.temp_dir, d))]
            if not extracted_dirs:
                self.log_to_status(f"Error: No directory found in extracted zip for {version_name}")
                return
            activemq_dir = os.path.join(self.temp_dir, extracted_dirs[0])

            # Path to activemq.bat
            bat_path = os.path.join(activemq_dir, "bin", "activemq.bat")
            if not os.path.exists(bat_path):
                self.log_to_status(f"Error: activemq.bat not found in {bat_path}")
                return

            # Extract version number from version_name (e.g., "apache-activemq-5.9.1-bin" -> "5.9.1")
            try:
                version_parts = version_name.split('-')
                version_str = version_parts[-2] if version_parts[-1] == 'bin' else version_parts[-1]
                activemq_version = version.parse(version_str)
                use_start = activemq_version >= version.parse("5.10.0")
            except Exception as e:
                self.log_to_status(f"Error parsing version {version_name}: {e}, defaulting to 'start' argument")
                use_start = True

            # Run activemq.bat in a thread
            def run_process():
                try:
                    # Set JAVA_HOME if not set
                    if "JAVA_HOME" not in os.environ:
                        os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-24"  # Adjust path as needed
                        self.log_to_status(f"Set JAVA_HOME to {os.environ['JAVA_HOME']}")

                    # Choose command based on version
                    command = [bat_path, "start"] if use_start else [bat_path]
                    self.log_to_status(f"Running command: {' '.join(command)}")

                    # Run activemq.bat
                    process = subprocess.Popen(
                        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
                    )
                    stdout, stderr = process.communicate(timeout=10)
                    # Check for usage message
                    if "Usage: Main" in stdout or "Usage: Main" in stderr:
                        self.log_to_status(f"Error: activemq.bat failed, got usage message: {stdout or stderr}")
                        # Fallback to activemq.bat without arguments if "start" was used
                        if use_start:
                            self.log_to_status(f"Retrying with {bat_path} alone")
                            process = subprocess.Popen(
                                [bat_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
                            )
                            stdout, stderr = process.communicate(timeout=10)
                            if process.returncode == 0 and "Usage: Main" not in stdout and "Usage: Main" not in stderr:
                                self.log_to_status(f"ActiveMQ {version_name} started with activemq.bat: {stdout}")
                            else:
                                self.log_to_status(f"Error running {version_name} with activemq.bat: {stderr or stdout}")
                        else:
                            self.log_to_status(f"Error running {version_name}: {stderr or stdout}")
                    else:
                        self.log_to_status(f"ActiveMQ {version_name} started: {stdout}")
                except subprocess.TimeoutExpired:
                    self.log_to_status(f"ActiveMQ {version_name} is running in the background.")
                except Exception as e:
                    self.log_to_status(f"Error running {version_name}: {e}")

            self.current_process = None
            self.current_thread = threading.Thread(target=run_process)
            self.current_thread.daemon = True
            self.current_thread.start()

        except Exception as e:
            self.log_to_status(f"Error processing {version_name}: {e}")

    def delete_temp_dir_with_retries(self, max_retries=7, delay=1):
        """Attempt to delete the temp directory with retries."""
        for attempt in range(max_retries):
            try:
                if os.path.exists(self.temp_dir):
                    shutil.rmtree(self.temp_dir)
                    self.log_to_status(f"Cleaned up temporary directory: {self.temp_dir}")
                return
            except Exception as e:
                self.log_to_status(f"Attempt {attempt + 1}/{max_retries} to clean up temporary directory failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
        self.log_to_status(f"Failed to clean up temporary directory after {max_retries} attempts.")

    def stop_current_activemq(self):
        """Stop the currently running ActiveMQ process and clean up."""
        self.log_to_status("Stopping current ActiveMQ instance")
        try:
            # Always attempt to terminate java.exe processes
            self.log_to_status("Using taskkill /F to terminate java.exe")
            for attempt in range(3):  # Retry up to 3 times
                result = subprocess.run(
                    ["taskkill", "/IM", "java.exe", "/F"], capture_output=True, text=True
                )
                self.log_to_status(f"taskkill attempt {attempt + 1}/3: stdout={result.stdout}, stderr={result.stderr}")
                time.sleep(1)  # Allow time for process to exit
                # Check if java.exe is still running
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq java.exe"], capture_output=True, text=True
                )
                self.log_to_status(f"tasklist after attempt {attempt + 1}: {result.stdout}")
                if "java.exe" not in result.stdout.lower():
                    self.log_to_status("All java.exe processes terminated successfully")
                    break
                else:
                    self.log_to_status("java.exe processes still running, retrying taskkill")
            else:
                self.log_to_status("Warning: java.exe processes may still be running after 3 taskkill attempts")
        except Exception as e:
            self.log_to_status(f"Error stopping ActiveMQ: {e}")
        
        # Reset thread state
        self.current_thread = None

        # Attempt to delete temp directory
        self.delete_temp_dir_with_retries()

        self.current_version = None

    def handle_version_selection(self, item):
        """Handle selection of an ActiveMQ version."""
        version_name = item.text()
        zip_filename = item.data(Qt.UserRole)
        zip_path = os.path.join("modules", "Load_ActiveMQ", zip_filename)
        self.log_to_status(f"Selected ActiveMQ version: {version_name}")

        # Stop and clean up any running ActiveMQ
        self.stop_current_activemq()

        # Update list to bold selected item
        for i in range(self.ui.ActiveMQList.count()):
            list_item = self.ui.ActiveMQList.item(i)
            font = QFont()
            font.setBold(list_item.text() == version_name)
            list_item.setFont(font)

        # Run the selected version
        self.current_version = version_name
        self.run_activemq(version_name, zip_path)

    def cleanup(self):
        """Clean up resources before closing."""
        self.log_to_status("Cleaning up ActiveMQ Loader")
        self.stop_current_activemq()

    def showEvent(self, event):
        """Handle tab show event."""
        super().showEvent(event)
        self.ui.ActiveMQList.setFocus()
        #self.log_to_status("ActiveMQ Loader tab shown")
