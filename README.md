# Custom CLI Editor

> A lightweight, DIY command-line text editor with ANSI-driven cursors, undo/redo, word motions, line operations, and more.

![CLI Demo](https://raw.githubusercontent.com/ThemisF/Custom_CLI_Editor.git/main/images/codeUse_1.png)

---

## Table of Contents


- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Cursor Modes](#cursor-modes)
- [Command Reference](#command-reference)
- [Sample Session](#sample-session)
- [Contributing](#contributing)

---

## Features

- **Row & Line Cursors**  
  - **Row cursor** highlights the character at the cursor position using ANSI escape sequences.  
  - **Line cursor** prefixes the current line with `*` and shifts other lines by one space.
- **Basic Editing**  
  - **Insert (`i <text>`)**: Inserts `<text>` left of the cursor and moves the cursor to the start of the inserted text.  
  - **Append (`a <text>`)**: Inserts `<text>` right of the cursor and moves the cursor to the end of the inserted text.  
  - **Delete Character (`x`)**: Deletes the character at the cursor.  
  - **Delete Word (`dw`)**: Deletes from the cursor to the start of the next word or end of line.
- **Cursor Movements**  
  - **Horizontal**: `h` (left), `l` (right), `^` (start of line), `$` (end of line).  
  - **Vertical**: `j` (down), `k` (up) — maintains column if possible, otherwise goes to end of shorter lines.
- **Word Motions**  
  - `w`: Move to the start of the next word.  
  - `b`: Move to the start of the previous word.  
- **Line Operations**  
  - **Copy (`yy`)**: Copy the current line into the buffer.  
  - **Paste (`p`/`P`)**: Paste below (`p`) or above (`P`) the current line.  
  - **Empty Line Insert (`o`/`O`)**: Insert a blank line below (`o`) or above (`O`).  
  - **Delete Line (`dd`)**: Delete the current line.
- **History**  
  - **Undo (`u`)**: Revert the last change command.  
  - **Repeat (`r`)**: Re-execute the last change command (ignores `u`, `s`, and `?`). After an undo, repeats the command preceding the undone action.
- **Help & Quit**  
  - `?`: Show detailed help.  
  - `s`: Display current content.  
  - `q`: Quit the editor.

---

## Installation

1. Clone the repository  
    git clone https://github.com/ThemisF/Custom_CLI_Editor.git  
    cd Custom_CLI_Editor  

2. python DIY_CLI_Editor.py

---

## Usage

At the `>` prompt, enter commands. Use `s` to show current content and cursor positions.

---

## Cursor Modes

### Row Cursor (`.` toggle)  
Highlights the active character with a green background

### Line Cursor (`;` toggle)  
Prefixes the current line with `*`:  

     first line  
    *second line  
     third line

---

## Command Reference

| Category        | Command         | Description                                                                   |
|-----------------|-----------------|-------------------------------------------------------------------------------|
| **Help/Quit**   | `?`             | Display detailed help information.                                            |
|                 | `q`             | Quit the program.                                                             |
| **Cursor**      | `.`             | Toggle row cursor on/off.                                                     |
|                 | `;`             | Toggle line cursor on/off.                                                    |
|                 | `h`             | Move cursor left (with optional count).                                        |
|                 | `l`             | Move cursor right.                                                            |
|                 | `j`             | Move cursor down one line.                                                    |
|                 | `k`             | Move cursor up one line.                                                      |
|                 | `^`             | Move to beginning of line.                                                    |
|                 | `$`             | Move to end of line.                                                          |
| **Word**        | `w`             | Move to beginning of next word.                                               |
|                 | `b`             | Move to beginning of previous word.                                           |
| **Editing**     | `i <text>`      | Insert `<text>` before cursor; cursor moves to start of it.                   |
|                 | `a <text>`      | Append `<text>` after cursor; cursor moves to end of it.                      |
|                 | `x`             | Delete character at cursor.                                                   |
|                 | `dw`            | Delete word (and trailing spaces) at cursor.                                  |
| **Line Ops**    | `yy`            | Copy current line into buffer.                                                |
|                 | `p`             | Paste copied line(s) below the current line.                                  |
|                 | `P`             | Paste copied line(s) above the current line.                                  |
|                 | `dd`            | Delete current line.                                                          |
|                 | `o`             | Insert an empty line below current line.                                      |
|                 | `O`             | Insert an empty line above current line.                                      |
| **History**     | `u`             | Undo last change.                                                             |
|                 | `r`             | Repeat last change command (ignores non-edit commands).                       |
| **Display**     | `s`             | Show current content with cursors.                                            |

---

## Sample Session



---

## Contributing

1. Fork the repository  
    git clone https://github.com/your-username/Custom_CLI_Editor.git  
2. Create a feature branch  
    git checkout -b feature/YourFeature  
3. Commit your changes  
    git commit -m "Add YourFeature"  
4. Push to your branch  
    git push origin feature/YourFeature  
5. Open a Pull Request
