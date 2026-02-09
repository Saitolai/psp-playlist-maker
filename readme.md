# PSP Playlist Maker

A specialized tool for creating and managing music playlists (.m3u8) specifically for the Sony PlayStation Portable (PSP).

## Description

This application provides a simple Graphical User Interface (GUI) to build, read, and update playlists. It ensures your music is formatted correctly for the PSP's legacy software to recognize.

The program is made and tested in Windows 10, and have not been confirmed for other operating system currently.

## 📂 PSP File Setup (Critical!)
For playlists to work on your PSP, you **must** follow the official Sony PlayStation Portable directory structure. Ensure your folders are organized as follows on your Memory Stick:

1. **Music Files:** Place all your audio files in:  
   `[Memory Stick]:\MUSIC\`
2. **Playlist Files:** This application should save your generated playlists to:  
   `[Memory Stick]:\PSP\PLAYLIST\MUSIC\`

> **Note:** If the `PLAYLIST` or `MUSIC` subfolders do not exist under the `PSP` directory, you must create them manually.

## Getting Started

### Dependencies
* **Python 3.x**
* **Dependencies:** Install the drag-and-drop library via your terminal:

```
pip install tkinterdnd2
```

### Instructions to use the program

#### If cloned from repository
* Use Python command to run the python file. Example as shown below:
```
py mainv2.py
```
* Feel free to try out "py main.py" if you want to use the legacy version.

#### How to use the program
* A GUI will appear, and you start selecting songs with the file picker.
* Once all changes is done, hit save, name your playlist (e.g., RockMix), and ensure the destination is the \PSP\PLAYLIST\MUSIC\ folder mentioned above.

## Version History
* v2
    * Added Drag & Drop support.
    * New dropdown menu for file operations (Add Songs, Save Playlist, Load Playlist).
    * Integrated "About" section and direct GitHub links.
* v1
    * Initial release with basic GUI and manual file selection.

## Credits

* **Icon Design:** [Tina](https://www.artstation.com/tinayong96) – Created the application icon.
* **Libraries:** [tkinterdnd2](https://github.com/Eliav2/tkinterdnd2) for drag-and-drop support.