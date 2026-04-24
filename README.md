# PyNotepad
A text editor written in Python (tkinter)
<img width="881" height="656" alt="pynotepad" src="https://github.com/user-attachments/assets/8f276c94-3441-4bb8-81a6-e4dec65d7acb" />
The PyNotepad text editor is written in Python
and inspired by Florian Balmer's Notepad2 program.<br>
PyNotepad can work with files in several
popular (and less popular) encodings, such as
CP1252, CP437, and Mac Roman.<br>
It is possible to encrypt text files using
the Vigenère cipher.<br>
It also has a search and replace mechanism, simplifying
routine editing tasks.<br>
The program has been tested under Windows 7
(Python 3.5) and Linux Mint 21.3 (Python 3.10).

To run the program, we recommend using
the files in the project's root directory: **start.bat** for Windows<br>
and **start.sh** for Linux.<br>
Linux users should note
that the program's interface is rendered using
the tkinter library. If you don't have it installed, you
can install it using the terminal.<br>
**Ubuntu / Debian / Linux Mint:** <br>
sudo apt update<br>
sudo apt install python3-tk

**Fedora:** <br>
sudo dnf install python3-tkinter

**Arch Linux:** <br>
sudo pacman -S tk

To enable or disable encryption, use the corresponding button
on the right side of the toolbar.
