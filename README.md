# LoadActiveMQ Module

The `LoadActiveMQ` module is a component of the **HACKtiveMQ Suite**, designed to load and run specific versions of Apache ActiveMQ from `.zip` archives on a Windows system. It provides a graphical interface to select and execute ActiveMQ instances for testing or interaction.

**Important Notes**:
- This module is currently **Windows-only** due to its reliance on Windows-specific commands (`activemq.bat`, `taskkill`) and file paths.
- **Classic versions** of Apache ActiveMQ `.zip` files (e.g., `apache-activemq-5.9.1-bin.zip`) must be placed in the `modules/Load_ActiveMQ` directory.

## Overview

The `LoadActiveMQ` module allows users to:
- List available ActiveMQ versions from `.zip` files in the `modules/Load_ActiveMQ` directory.
- Extract and run a selected ActiveMQ version using `activemq.bat`.
- Automatically stop and clean up previous instances when switching versions.
- Log all actions (extraction, execution, errors) in a status window.

The module automatically creates the `modules/Load_ActiveMQ` directory if it does not exist, ensuring a seamless setup process.

## Requirements

### Software
- **Python**: Version 3.8 or later recommended.
- **Java Development Kit (JDK)**: Required to run ActiveMQ instances. The module references JDK 24 (e.g., `C:\Program Files\Java\jdk-24`), but other versions may work. Install Oracle JDK or OpenJDK and ensure `JAVA_HOME` is set or the path is correctly configured.
- **Windows Operating System**: The module is Windows-only.

### Python Dependencies
The following Python packages are required:
PySide6>=6.0.0
packaging>=21.0

## Installation

1. **Obtain the Module**:
   - The `LoadActiveMQ` module is part of the HACKtiveMQ Suite. Clone or download the suite repository, or extract the `load_activemq.py` file and its dependencies.

2. **Install Python Dependencies**:
   - Create a virtual environment (optional but recommended):
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Alternatively, install directly:
     ```bash
     pip install PySide6>=6.0.0 packaging>=21.0
     ```

3. **Install Java Development Kit (JDK)**:
   - Download and install a JDK (e.g., [Oracle JDK](https://www.oracle.com/java/technologies/javase-downloads.html) or [OpenJDK](https://adoptium.net/)).
   - Set the `JAVA_HOME` environment variable to the JDK installation path (e.g., `C:\Program Files\Java\jdk-24`), or the module will attempt to set it automatically.

4. **Prepare ActiveMQ `.zip` Files**:
   - Download **classic versions** of Apache ActiveMQ `.zip` archives from the [Apache ActiveMQ website](https://activemq.apache.org/components/classic/download/) or other trusted sources.
   - Place the `.zip` files (e.g., `apache-activemq-5.9.1-bin.zip`) in the `modules/Load_ActiveMQ` directory. The module will create this directory automatically if it does not exist.

## Usage

1. **Launch the Module**:
   - Run the `LoadActiveMQ` module via the ningu framework or the HACKtiveMQ Suite.

2. **Select and Run ActiveMQ**:
   - The `ActiveMQ Versions` list displays available versions based on `.zip` files in `modules/Load_ActiveMQ`.
   - Click a version to:
     - Stop any running ActiveMQ instance (terminates `java.exe` processes).
     - Extract the selected `.zip` to a temporary directory (`modules/Load_ActiveMQ/temp`).
     - Run `activemq.bat` with the appropriate command (`start` for versions >= 5.10.0, otherwise no arguments).
   - Logs are displayed in the `Status` text box, including:
     - Directory creation (if applicable).
     - Extraction progress.
     - Command execution details.
     - Any errors (e.g., missing `activemq.bat`, JDK issues).

3. **Cleanup**:
   - Selecting a new version automatically stops the current instance and deletes the temporary directory.
   - The module ensures resources are released when closed, terminating any running ActiveMQ processes.

## Directory Structure
```
HACKtiveMQ_Suite/
├── modules/
│   ├── Load_ActiveMQ/              # Place ActiveMQ .zip files here
│   │   ├── apache-activemq-5.9.1-bin.zip
│   │   ├── apache-activemq-5.10.0-bin.zip
│   │   └── ...
└── 2_LoadActiveMQ.py               # LoadActiveMQ module
```

## Limitations
- **Windows-Only**: The module uses Windows-specific commands (`activemq.bat`, `taskkill`) and paths, making it incompatible with Linux or macOS without modifications.
- **ActiveMQ Classic**: Only classic versions of ActiveMQ are supported. Artemis or other variants may not work.
- **JDK Dependency**: A compatible JDK must be installed and configured.
- **Version Parsing**: The module assumes `.zip` filenames follow the format `apache-activemq-X.Y.Z-bin.zip`. Non-standard names may sort alphabetically instead of numerically.

## Troubleshooting
- **No Versions Listed**:
  - Ensure `.zip` files are in `modules/Load_ActiveMQ`.
  - Verify the files are valid ActiveMQ classic `.zip` archives.
- **JDK Errors**:
  - Check that `JAVA_HOME` is set or the JDK path in the code (`C:\Program Files\Java\jdk-24`) is correct.
  - Install a compatible JDK if missing.
- **Permission Issues**:
  - Run the application with administrator privileges if directory creation or process termination fails.
- **Logs**:
  - Check the `Status` text box for detailed error messages (e.g., extraction failures, command errors).

## Contributing
Contributions to the `LoadActiveMQ` module are welcome! To contribute:
1. Fork the HACKtiveMQ Suite repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please test changes on Windows and ensure compatibility with the module's functionality.

## License
This module is licensed under the GNU General Public License v3.0. See the [LICENSE](https://www.gnu.org/licenses/) file for details.

## Contact
For issues, questions, or suggestions, contact Garland Glessner at gglesner@gmail.com.
