#!/usr/bin/env python3
import argparse
import os
import sys
import io
import locale
import time
from yt_dlp import YoutubeDL


def download_video(url: str, save_path: str, quality: str = 'best', audio_only: bool = False, retries: int = 3):
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: print_progress(d)],
            'noplaylist': True,
            'merge_output_format': 'mp4',
            'retries': retries,
            'fragment_retries': retries,
            'socket_timeout': 30,
            'extract_flat': False
        }

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3'
                }],
            })
        else:
            if quality == 'best':
                ydl_opts['format'] = 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b'
            else:
                ydl_opts['format'] = f'bv*[height<={quality}][ext=mp4]+ba[ext=m4a]/b[height<={quality}][ext=mp4]/b'

        attempts = 0
        while attempts < retries:
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print("\nSuccesfully downloading!")
                return
            except Exception as e:
                attempts += 1
                if attempts < retries:
                    print(
                        f"\nError by downloading (retry {attempts}/{retries}): {str(e)}")
                    print("Retry after 5 seconds...")
                    time.sleep(5)
                else:
                    raise

    except Exception as e:
        print(f"\nFailed to download video after {retries} retries: {str(e)}")


def print_progress(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(
            f"\rProgress: {percent} | Speed: {speed} | ETA : {eta}", end='')


def main():
    parser = argparse.ArgumentParser(
        description='YouTube Downloader с повторными попытками')
    parser.add_argument('--url', '-u', required=True,
                        help='URL from YouTube')
    parser.add_argument('--save-path', '-sp',
                        default="./downloads", help='Save-path for files')
    parser.add_argument('--quality', '-q', default='best',
                        help='Video quality (720, 1080, etc), best by default')
    parser.add_argument('--audio-only', '-a',
                        action='store_true', help='Download only audio (MP3)')
    parser.add_argument('--retries', '-r', type=int, default=3,
                        help='Retries attempts')

    args = parser.parse_args()

    if not args.url.startswith(('http://', 'https://')):
        print("Invalid URL. Must started with http:// or https://")
        return

    print(
        f"\nStart downloading...\nURL: {args.url}\nSave in: {args.save_path}")
    if args.audio_only:
        print("Only audio (MP3)")
    else:
        print(f"Quality: {args.quality}")
    print(f"Max retries: {args.retries}")

    download_video(args.url, args.save_path, args.quality,
                   args.audio_only, args.retries)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    main()
