# PSP Playlist Maker

A specialized tool for creating and managing music playlists (.m3u8) specifically for the Sony PlayStation Portable (PSP).

## Description

This application provides a simple Graphical User Interface (GUI) to build, read, and update playlists. It ensures your music is formatted correctly for the PSP's legacy software to recognize.

The program is made and tested on **Windows 10** and **Linux Mint** (Ubuntu/Debian-based distributions).

## 📂 PSP File Setup (Critical!)
For playlists to work on your PSP, you **must** follow the official Sony PlayStation Portable directory structure. Ensure your folders are organized as follows on your Memory Stick:

1. **Music Files:** Place all your audio files in:  
   `[Memory Stick]:\MUSIC\`
2. **Playlist Files:** This application should save your generated playlists to:  
   `[Memory Stick]:\PSP\PLAYLIST\MUSIC\`

Do ensure that your PSP firmware is up to date in order to be able to use the playlist features.

(information regarding to early supported firmware version with playlist is reported around [6.10](https://www.psdevwiki.com/psp/Official_Firmware_(OFW)#6.10))
> **Note:** If the `PLAYLIST` or `MUSIC` subfolders do not exist under the `PSP` directory, you must create them manually.

## 🛠 Getting Started

### Dependencies & Setup

**For Windows**
* **Python 3.x**
* Install the drag-and-drop library via your terminal:

```
pip install tkinterdnd2
```

**For Linux (Mint/Ubuntu/Debian)**
* Linux requires the system-level GUI toolkit for Python to draw the application window. Open your terminal and run:

```
sudo apt update && sudo apt install python3-tk python3-pip python3-venv -y
```

### Instructions to use the program

#### If cloned from repository
#### On Windows:
* Use Python command to run the python file. Example as shown below:

```
py mainv2.py
```
* Feel free to try out "py main.py" if you want to use the legacy version without drag-and-drop.

#### On Linux:
* It is highly recommended to use a Virtual Environment to keep your system claen, and to run main.py (v1) as the drag-and-drop library in v2 requires complex C++ wrappers on Linux.

```
# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate the environment
source .venv/bin/activate

# 3. Run the legacy GUI version
python3 mainv2-linux-mint.py
```

#### How to use the program
* A GUI will appear, and you start selecting songs with the file picker.
* Once all changes is done, hit save, name your playlist (e.g., RockMix), and ensure the destination is the \PSP\PLAYLIST\MUSIC\ folder mentioned above.

## 📜 Version History
* v2
    * Added Drag & Drop support (Optimized for Windows).
    * New dropdown menu for file operations (Add Songs, Save Playlist, Load Playlist).
    * Integrated "About" section and direct GitHub links.
    * Fixed issue on Linux Mint regarding to how the playlist file directory is saved.
* v1
    * Initial release with basic GUI and manual file selection.

## ❤️ Credits & Attribution

* **Icon Design:** [Tina](https://www.artstation.com/tinayong96) – Created the application icon.
* **Libraries:** [tkinterdnd2](https://github.com/Eliav2/tkinterdnd2) for drag-and-drop support.