# Time Warp Attack: Side-Channel Timing Security Game

## Overview
Learn about timing side-channel vulnerabilities by exploiting and patching a flawed authentication service.

## Quick Start (Docker)
```bash
docker-compose up --build
```
- Vulnerable service: `http://localhost:5000`
- Fixed (patched) service: `http://localhost:5001`

## Game Files
- `code.py` — vulnerable service
- `solution.py` — fixed service
- `hack.py` — attack tool
- `tests.py` — validation tests
- `hint.txt` — hints for learners
- `graph.py` — visualize response timings

## How to Play
1. Try attacking the vulnerable service using `hack.py`.
2. Analyze timing information to find valid users and PINs.
3. Patch the service (see `solution.py`) and re-test.
4. Use visual graphs for deeper understanding.

## Educational Objectives
- Identify and exploit timing side-channels
- Learn constant-time coding techniques
- Understand authentication security best practices
- 
Key Enhancements:
Concurrent Testing:

Uses ThreadPoolExecutor to test multiple user IDs simultaneously

Dramatically reduces total execution time

Statistical Analysis:

Uses Median Absolute Deviation (MAD) to automatically detect anomalies

Configurable threshold for identifying valid users

Improved Brute-Force:

Checks common PINs first before full brute-force

Implements chunked brute-forcing with progress tracking

Also uses concurrent requests for PIN testing

Better Visualization:

Highlights potential valid users in red

Shows threshold line for anomaly detection

Saves plot to file

Error Handling:

More robust error handling for network issues

Timeouts to prevent hanging

Progress Tracking:

Uses tqdm for progress bars during both phases

Shows elapsed time for complete attack

Results Saving:

Saves successful credentials to JSON file

Includes timestamp and authentication token

Configuration:

All important parameters are configurable at the top

Easy to adjust for different scenarios

Modular Design:

Separated into logical functions for better maintainability

Each phase can be run independently if needed
See `hint.txt` for help!
[![Ask AI Agent](https://img.shields.io/badge/Ask%20AI-Agent-blue)](https://huggingface.co/chat?repo=your-repo)
#### my_streaming_software
my_streaming_software/
├── src/
│   ├── main.cpp
│   ├── recorder/
│   │   ├── screen_recorder.cpp
│   │   └── screen_recorder.h
│   │   ├── webcam_recorder.cpp
│   │   └── webcam_recorder.h
│   │   ├── audio_recorder.cpp
│   │   └── audio_recorder.h
│   ├── streamer/
│   │   ├── live_streamer.cpp
│   │   └── live_streamer.h
│   ├── gui/
│   │   ├── main_window.cpp
│   │   └── main_window.h
│   └── utils/
│       ├── ffmpeg_wrapper.cpp
│       └── ffmpeg_wrapper.h
├── docs/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── INSTALL.md
├── tests/
│   ├── test_recorder.cpp
│   ├── test_streamer.cpp
│   ├── test_webcam_recorder.cpp
│   ├── test_audio_recorder.cpp
│   └── test_real_time_effects.cpp
└── LICENSE
