
# 🌐 **TerChat: Client-Server Chat Application**

Welcome to **TerChat**, a terminal-based client-server chat application designed as part of a software architecture assignment. This project showcases key software quality attributes like **time behavior**, **recoverability**, and **maintainability**, tested through automated fitness functions.

TerChat allows users to anonymously send messages, retrieve message counts, and experience seamless client-server communication with caching, error handling, and reconnection features.

---

## 🚀 **Features**

- **Anonymous messaging**: Send and receive messages in real-time.
- **Message count tracking**: View the total number of messages in the system.
- **Recoverability**: The client automatically handles disconnections and attempts to reconnect to the server.
- **Caching**: Frequently requested data (e.g., message counts) is cached to improve time behavior.
- **Unit tests**: Comprehensive test coverage with tools like `unittest` and `pytest` ensures maintainability.
- **Fitness functions**: Measure key quality attributes using dedicated test cases and analysis tools.

---

## 🗺 **Table of Contents**
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Set up the virtual environment](#2-set-up-the-virtual-environment)
  - [3. Install project dependencies](#3-install-project-dependencies)
- [Running the Application](#running-the-application)
  - [Running the Server](#running-the-server)
  - [Running the Client](#running-the-client)
- [Running Tests](#running-tests)
  - [1. Unit Tests for the Server](#1-unit-tests-for-the-server)
  - [2. Test Coverage for the Server](#2-test-coverage-for-the-server)
- [Technologies Used](#technologies-used)


---

## 📂 **Project Structure**

```
TerChat/
│
├── client/             # Client-side code
│   ├── ui/             # User interface components (Textual-based)
│   ├── static/         # styles for the client app
│   ├── services/       # Message services for sending/receiving
│   └── client.py       # Client entry point
│
├── server/             # Server-side code
│   ├── app.py          # Flask server
│   ├── db_service.py   # Database operations
│   ├── test_server.py  # Unit tests for server
│   └── messages.db     # SQLite database (auto-generated)
│
├── requirements.txt    # Project dependencies
├── run_client.sh       # Script to run the client
├── run_server.sh       # Script to run the server
├── init_venv.sh        # Script to init Virtual environment
├── run_covtest_server.sh # Script to run coverage tests for the server
├── run_unittest_server.sh # Script to run unittests for the server
└── README.md           # Project README
```

## ⚙️ **Setup Instructions**

### **1. Clone the repository**

```bash
git clone https://github.com/your-username/TerChat.git
cd TerChat
```

### **2. Set up the virtual environment**

If you haven't already, set up a Python virtual environment to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install project dependencies**

Run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

## 💻 **Running the Application**

### **Running the Server**

The `run_server.sh` script handles setting up the server, clearing the old database, and starting the Flask server.

To start the server:

```bash
./run_client.sh
```

- This script:
    - Activates the virtual environment.
    - Installs the required dependencies.
    - Launches the client in the terminal.

The client communicates with the server using real-time SocketIO for seamless messaging.

## 🧪 **Running Tests**

### **1. Unit Tests for the Server**

You can run the server-side unit tests using `run_unittest_server.sh`:

```bash
./run_unittest_server.sh
```

- This script runs all the unit tests in the `server` directory and outputs the results. It checks if all tests pass and provides feedback.

### **2. Test Coverage for the Server**

To generate a test coverage report for the server, use the `run_covtest_server.sh` script:

```bash
./run_covtest_server.sh
```

This script runs the tests with coverage tracking and generates a detailed coverage report, which includes a breakdown of which lines of code are covered by tests.

## 🛠️ **Technologies Used**

- **Python 3.12**: Core programming language.
- **Flask**: Lightweight WSGI web framework for the server-side implementation.
- **SocketIO**: Enables real-time communication between the client and server.
- **Textual**: A TUI (Text User Interface) library used for the client's terminal interface.
- **SQLite**: Lightweight database for message storage.
- **Pytest & Unittest**: Used for testing and ensuring maintainability.
- **Coverage.py**: Used to measure the test coverage.

---
