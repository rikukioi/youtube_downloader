# Simple YT video/audio downloader console-app

## Installing
1. Clone repository:
   ```bash
   git clone https://github.com/rikukioi/youtube_downloader
   ```
   Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Download FFmpeg:
    - Linux
    ```bash
    sudo apt install ffmpeg
    ```
    - MacOS
    ```bash
    brew install ffmpeg
    ```
    - Windows
    ```bash
    winget install ffmpeg
    ```
## Use cases
1. Download highest-quality video .mp4
    ```bash
    python ydownloader.py -u "URL"
    ```
2. Download specific quality for video .mp4
    ```bash
    python ydownloader.py -u "URL" -q "1080"
    ```
3. Download file in specific directory
    ```bash
    python ydownloader.py -u "URL" -sp "E:/"
    ```
4. Download audio only
    ```bash
    python ydownloader.py -u "URL" -a
    ```
