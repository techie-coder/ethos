**<h1 align="center">Ethos</h1>**

<p align="center">
  <img src="src/img/ethos_logo.jpg" alt="Logo of Ethos" width="300", height="300">
</p>

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Itz-Agasta/ethos/pulls)
[![Code Coverage](https://img.shields.io/codecov/c/github/Itz-Agasta/ethos)](https://codecov.io/gh/Itz-Agasta/ethos)
[![Downloads](https://img.shields.io/pypi/dm/ethos)](https://pypi.org/project/ethos/)
[![GitHub Issues](https://img.shields.io/github/issues/Itz-Agasta/ethos)](https://github.com/Itz-Agasta/ethos/issues)
[![GitHub Stars](https://img.shields.io/github/stars/Itz-Agasta/ethos)](https://github.com/Itz-Agasta/ethos/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/Itz-Agasta/ethos)](https://github.com/Itz-Agasta/ethos/commits/main)

</div>

  <p align="center">
    A modern, resource-efficient CLI music player that seamlessly integrates local music libraries with online streaming services. Experience high-quality audio playback, Spotify playlist synchronization, and an intuitive terminal interface designed for both developers and music enthusiasts.
    <br />
    <br />
    <a href="https://www.youtube.com/watch?v=E1AjSHxe5NU&feature=youtu.be">View Demo</a>
    ·
    <a href="https://github.com/Itz-Agasta/ethos/issues">Report Bug</a>
    ·
    <a href="https://github.com/Itz-Agasta/ethos/issues">Request Feature</a>
    ·
    <a href="https://github.com/Itz-Agasta/ethos/pulls">Send a Pull Request</a>
  </p>
</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Preview](#preview)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
  - [For Development:](#for-development)
  - [For Distribution:](#for-distribution)
- [Usage:](#usage)
  - [Basic Commands](#basic-commands)
  - [Queue Management](#queue-management)
  - [Keyboard Shortcuts](#keyboard-shortcuts)
  - [Basic Workflow](#basic-workflow)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
- [Repository Structure](#repository-structure)
- [Contributors](#contributors)
- [License](#license)

## Features

🎵 **Universal Accessibility**

- High-quality terminal music playback accessible to both developers and general users
- Modern and feature-rich interface in your terminal
- Support for multiple audio formats (MP3, FLAC, WAV, AAC)

💻 **Resource Efficient**

- Lightweight application with minimal system resource consumption
- Can be used in devices like Raspberry Pi
- Optimized for lower-end devices without compromising functionality

🔄 **Unified Music Experience**

- Seamlessly bridges local music libraries with online streaming services
- All your music needs handled from a single terminal interface
- Import and sync your Spotify playlists
- Offline playback for downloaded tracks

⚡ **Developer-Centric**

- Terminal-native music solution that integrates with your development workflow
- Enhances productivity by keeping you in your preferred environment

## Preview

<p align="center">
  <img src="src/img/ethos_ui.jpg" alt="Logo of Ethos">
</p>

## Technologies Used

- **Backend:** yt-dlp, python-vlc, spotify API, spotipy
- **Frontend:** Rich, Textual
- **Language:** Python

## Prerequisites

Make sure you have the following installed:

- Python 3.8 or later
- pip (Python package installer)
- VLC media player

## Quick Start

```bash
# Install Ethos
pip install ethos

# Start playing music
ethos
```

## Installation

### For Development:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com//Itz-Agasta/ethos.git
   cd ethos
   ```
2. **Install Poetry:**

   ```bash
   pipx install poetry
   ```

   > **Note:** It is recommended to use `pipx` for installing Poetry, but you can also use `pip` if `pipx` is not available. For more information, please refer to the [official documentation](https://python-poetry.org/docs/).

3. **Configure Poetry to Create Virtual Environment in Project Root:**

   ```sh
   poetry config virtualenvs.in-project true
   ```

4. **Install Dependencies:**
   ```bash
   poetry install
   ```
5. **Setup the .env file:** see the `.env.example` for reference and create a `.env` file in the root.

6. **Start the application:**
   ```bash
   poetry run python ethos/main.py
   ```

### For Distribution:

Coming Soon

## Usage:

https://github.com/user-attachments/assets/e46a7585-ccf1-4e30-bc20-3c48b0767969

### Basic Commands

```bash
/play <track name>     # Search and play a track
/pause                 # Pause current playback
/resume                # Resume playback
/volume <0-100>        # Set volume level
```

### Queue Management

```bash
/queue-add <track>    # Add a track to queue
/show-queue           # Display current queue
/qp <number>          # Play track number from queue
```

### Keyboard Shortcuts

| Shortcut             | Action           |
| -------------------- | ---------------- |
| `Ctrl+C` or `Ctrl+Q` | Quit application |
| `Ctrl+M`             | Pause playback   |
| `Ctrl+R`             | Resume playback  |
| `Ctrl+1`             | Increase volume  |
| `Ctrl+2`             | Decrease volume  |

### Basic Workflow

1. Search for a track:

   ```bash
   /play never gonna give you up
   ```

2. Select from search results by entering the track number (e.g. 1)

3. Control playback:

- Use `/pause` and `/resume` to control playback
- Adjust volume with `/volume 75`
- View all commands with `/help`

## Troubleshooting

### Common Issues

| Issue                     | Solution                                          |
| ------------------------- | ------------------------------------------------- |
| No audio output           | Check system volume and VLC installation          |
| Spotify integration fails | Verify `.env` configuration                       |
| Installation errors       | Update pip: `python -m pip install --upgrade pip` |

## Repository Structure

```bash
ethos/
├── .env.example
├── .gitignore
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── docker/
│   ├── dockerfile
│   ├── compose.yaml
│   └── readme.md
├── src/
│   └── img/
├── ethos/
│   ├── __init__.py
│   ├── main.py    # entry point of the application.
│   ├── config.py  # Manages configuration settings.
│   ├── player.py  # Handles the core functionality of the music player.
│   ├── utils.py   # Contains utility functions and other helper functions.
│   ├── spotify_importer.py # User's Spotify playlist integration
├── ├── tools/         # Helper tools and utilities
│   │   ├── __init__.py
│   │   ├── endless_playback.py
│   │   └── helper.py
│   ├── ui/           # Terminal UI components
│   │   ├── __init__.py
│   │   ├── rich_layout.py
│   │   ├── styles.tcss
│   │   ├── textual_app.py
│   │   └── ui.py
├── tests/          # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   └── test_player/
│       ├── __init__.py
│       └── test_playback.py
├── LICENSE
├── README.md
├── pyproject.toml  # Project configuration and dependencies
├── pytest.ini      # PyTest configuration
├── setup.py        # Contains the setup script
└── requirements.txt
```

## Contributors

<a href="https://github.com/Itz-Agasta/ethos/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Itz-Agasta/ethos" />
</a>

## License

This project is licensed under the [MIT License](https://github.com/Itz-Agasta/ethos/blob/main/License). See the LICENSE file for more details.

Feel free to Send a [Pull Request](https://github.com/Itz-Agasta/ethos/pulls) if you have improvements or fixes.
