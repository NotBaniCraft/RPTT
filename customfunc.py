import os
import sys

# Function to check if the terminal supports colors
def supports_colors():
    if not sys.stdout.isatty():
        return False

    # Check for Windows legacy cmd support for true color
    if os.name == 'nt':  # We're on Windows
        try:
            # Test for Windows legacy terminal support for ANSI codes
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong(0)
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            mode.value |= 0x0004  # Enable virtual terminal processing
            kernel32.SetConsoleMode(handle, mode)
            return True  # Windows Terminal or legacy CMD with color support
        except Exception:
            return False

    # Otherwise, test for color support by trying to print a color
    try:
        sys.stdout.write("\033[38;2;255;0;0mTest\033[0m")  # Test for true color
        return True
    except Exception:
        return False

def warn(text):
    if supports_colors():
        print(f"\033[1m\033[38;2;255;165;0m{text}\033[0m")  # Yellow
    else:
        print(f"WARN: {text}")

def error(text):
    if supports_colors():
        print(f"\033[1m\033[38;2;255;0;0m{text}\033[0m")  # Red
    else:
        print(f"ERROR: {text}")

def info(text):
    if supports_colors():
        print(f"\033[1m\033[38;2;100;200;255m{text}\033[0m")  # Light Sky Blue
    else:
        print(f"INFO: {text}")
