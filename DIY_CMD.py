import re 

g_save = [("", None, "", 1, False, False, 1, [])]
g_copast = None
g_user_input = None
g_command_map={}

def display_cont() -> None:
    """
    Display the current editor content with the cursor position highlighted.

    This function retrieves the latest content, cursor position, and cursor toggle flag 
    from g_save. If the content is non-empty and the cursor toggle is enabled, 
    it highlights the character at the cursor position using ANSI escape codes. Otherwise, 
    it prints the plain content.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor = g_save[-1][2:4]
    for idx, row in enumerate(g_save[-1][7], start=1):
        if g_save[-1][6] == idx:
            astr = "*" if g_save[-1][5] else ""
            if len(edit_cont)>0:
                cont_list = list(edit_cont)
                cont_list[cursor - 1] = "\033[42m" + cont_list[cursor - 1] + "\033[0m"
                print(astr + "".join(cont_list) if g_save[-1][4] else astr + edit_cont)
            else:
                print(astr + edit_cont)
        else:
            print((" " if g_save[-1][5] else "") + row[0])
            
def turn_cursor_on_off() -> None:
    """
    Toggle the cursor highlight display on or off.

    Retrieves the current text and cursor position from the latest state and appends a new state 
    with the cursor toggle flag inverted. This lets the user switch between a highlighted and 
    non-highlighted cursor view.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    apend = ('.', None, edit_cont, cursor_pos, not g_save[-1][4]) + g_save[-1][5:8]
    g_save.append(apend)


def insert_text(text: str) -> None:
    """
    Insert text before the current cursor position.

    The function inserts the given 'text' at the position indicated by the 1-indexed cursor. 
    If the cursor is at the beginning (position 1), the text is prepended. Otherwise, the text 
    is inserted before the character currently at the cursor. The new state, with the updated content, 
    is appended to g_save.

    Parameters:
        text (str): The text to insert.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    g_content_list = list(edit_cont)
    if cursor_pos == 1:
        g_content_list = [text] + g_content_list
    else:
        g_content_list[cursor_pos - 1] = text + g_content_list[cursor_pos-1]
    edit_cont="".join(g_content_list)
    k = g_save[-1][4:6] + (g_save[-1][6], [[""]] if len(g_save[-1][7]) == 0 else g_save[-1][7])
    g_save.append(('i', " " + text, edit_cont, cursor_pos) + k)


def append_text(text: str) -> None:
    """
    Append text after the current cursor position and adjust the cursor accordingly.

    Depending on whether the cursor is at the beginning (position 1) or not, the function either 
    prepends or appends the given 'text' to the character at the current cursor position. The cursor 
    is then moved forward by the length of the inserted text (with an adjustment if the cursor was at the 
    very beginning). The new state is saved in g_save.

    Parameters:
        text (str): The text to append.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    g_content_list = list(edit_cont)
    o = len(g_content_list)
    if o == 0:
        g_content_list=[text]+g_content_list
    else:
        g_content_list[cursor_pos - 1] = g_content_list[cursor_pos - 1] + text
    edit_cont="".join(g_content_list)
    cursor_pos += len(text) - (o == 0 and 1 or 0)
    k = g_save[-1][4:6] + (g_save[-1][6], [[""]] if len(g_save[-1][7]) == 0 else g_save[-1][7])
    g_save.append(('a', " " + text, edit_cont, cursor_pos) + k)


def move_cursor_left() -> None:
    """
    Move the cursor one position to the left.

    Decreases the cursor position by one, ensuring it never goes below position 1. The updated 
    state is then saved to g_save.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    if g_save[-1][2]:
        cursor_pos = max(1, cursor_pos - 1)
    g_save.append(('h', None, edit_cont, cursor_pos) + g_save[-1][4:8])


def move_cursor_right() -> None:
    """
    Move the cursor one position to the right.

    Increases the cursor position by one, ensuring it does not exceed the length of the content. 
    The new state is then saved in g_save.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    if g_save[-1][2]:
        cursor_pos = min(cursor_pos + 1, len(edit_cont))
    g_save.append(('l', None, edit_cont, cursor_pos) + g_save[-1][4:8])


def move_cursor_beginning() -> None:
    """
    Move the cursor to the beginning of the content (position 1).

    Resets the cursor to the first position of the current text and appends the updated state 
    to g_save.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    cursor_pos = 1
    g_save.append(('^', None, edit_cont, cursor_pos) + g_save[-1][4:8])


def move_cursor_end() -> None:
    """
    Move the cursor to the end of the content.

    Sets the cursor to the end (equal to the length of the text) and saves the new state 
    in g_save.

    Returns:
        None
    """
    
    edit_cont, cursor_pos = g_save[-1][2:4]
    if g_save[-1][2]:
        cursor_pos = len(edit_cont)
    g_save.append(('$', None, edit_cont, cursor_pos) + g_save[-1][4:8])


def move_cursor_next_word() -> None:
    """
    Move the cursor to the beginning of the next word.

    Searches for the next occurrence of a whitespace followed by a non-whitespace character 
    in the text starting from the current cursor position. If found, the cursor is moved to that 
    position; otherwise, it remains unchanged. The new state is then saved.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    if g_save[-1][2]:
        k = cursor_pos - 1
        g = (m := re.search(r'\s\S', edit_cont[k:])) and k + m.end() or cursor_pos
        cursor_pos = g
    g_save.append(('w', None, edit_cont, cursor_pos) + g_save[-1][4:8])


def move_cursor_prev_word() -> None:
    """
    Move the cursor to the beginning of the previous word.

    Searches backwards from the current cursor position to locate the start of the previous 
    sequence of non-whitespace characters. The cursor is moved accordingly and the new state 
    is saved. If no previous word is found, the cursor position is adjusted minimally.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    if g_save[-1][2]:
        cursor_pos -= 1
        match = re.search(r'\S+', edit_cont[:cursor_pos][::-1])
        cursor_pos = max(1, cursor_pos - match.end() + 1) if match else cursor_pos + 1
    g_save.append(('b', None, edit_cont, cursor_pos) + g_save[-1][4:8])


def delete_char() -> None:
    """
    Delete the character at the current cursor position.

    Uses the 1-indexed cursor to compute the corresponding 0-indexed position and removes the character 
    at that position by slicing the string. If the deletion causes the cursor to exceed the new text 
    length, it is adjusted to stay within valid bounds. The updated content and cursor position are saved.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    if g_save[-1][2]:
        edit_cont = edit_cont[:cursor_pos - 1] + edit_cont[cursor_pos:]
        if cursor_pos == len(edit_cont)+1: cursor_pos=max(1, cursor_pos - 1)
    g_save.append(('x', None, edit_cont, cursor_pos) + g_save[-1][4:8])

def delete_word() -> None:
    """
    Delete a word starting from the current cursor position.

    Identifies a word as a sequence of non-whitespace characters starting at the current cursor. 
    Using a regular expression, it locates the end of the word and removes the entire word from the 
    content. The new state, including the modified text and adjusted cursor position, is saved.

    Returns:
        None
    """
    global g_save
    con, pos = g_save[-1][2:4]
    if con and con[pos - 1] != " ":
        g = (m := re.search(r'\s\S', con[pos:])) and pos - 1 + m.end() or len(con)
        new_con = con[:pos - 1] + con[g:]
        if g == len(con): pos = max(1, pos - 1)
        con = new_con
    elif con and con[pos - 1] == " ":
        g = (m := re.search(r'\S', con[pos:])) and pos - 1 + m.end() or len(con)
        new_con = con[:pos - 1] + con[g:]
        if g == len(con): pos = max(1, pos - 1)
        con = new_con
    g_save.append(('dw', None, con, pos) + g_save[-1][4:8])

def move_cursor_up() -> None:
    """
    Move the cursor up one row in the screen buffer.

    Shifts the current row index up (if not already at the top), loads that row’s content
    as the new editing line, adjusts the cursor column if it exceeds the line length,
    and records the updated state in g_save.

    Returns:
        None
    """
    global g_save
    cont, curs_pos = g_save[-1][2:4]
    curs, screen = g_save[-1][6:8]
    if curs > 1:
        cont = screen[curs-2][0]
        screen[curs-1][0] = g_save[-1][2]
        curs_pos = curs_pos if curs_pos < len(cont) else len(cont)
        curs -= 1
        curs_pos = 1 if curs_pos == 0 else curs_pos
    g_save.append(('j', None, cont, curs_pos) + g_save[-1][4:6] + (curs, screen))

def move_cursor_down() -> None:
    """
    Move the cursor down one row in the screen buffer.

    Advances the current row index down (if not at the bottom), loads that row’s content
    as the new editing line, adjusts the cursor column if needed,
    and appends the new state to g_save.

    Returns:
        None
    """
    global g_save
    cont, curs_pos = g_save[-1][2:4]
    curs, screen = g_save[-1][6:8]
    if curs < len(screen):
        cont = screen[curs][0]
        screen[curs-1][0] = g_save[-1][2]
        curs_pos = curs_pos if curs_pos < len(cont) else len(cont)
        curs += 1
        curs_pos = 1 if curs_pos == 0 else curs_pos
    g_save.append(('k', None, cont, curs_pos) + g_save[-1][4:6] + (curs, screen))

def copy_line() -> None:
    """
    Copy the current line content into the clipboard (g_copast).

    Saves the text of the active row into g_copast without altering the displayed content,
    and pushes a marker state to g_save.

    Returns:
        None
    """
    global g_save, g_copast
    g_copast = g_save[-1][2] if g_save[-1][7] != [] else None
    g_save.append((('yy', None) + g_save[-1][2:8])) 

def paste_line_below() -> None:
    """
    Paste the clipboard content below the current row.

    If g_copast is empty, performs no change; otherwise,
    inserts the copied text as a new line immediately below the cursor row,
    sets the cursor within the pasted line, and logs the state.

    Returns:
        None
    """
    global g_save, g_copast
    if g_copast == None:
        g_save.append(('p', None) + g_save[-1][2:8])
    elif g_save[-1][7] == [] and g_copast != None:
        o = len(g_copast) if len(g_copast)>0 else 1
        g_save.append(('p', None, g_copast, o) + g_save[-1][4:6] + (1, [[""]]))
    else:
        curs = g_save[-1][3] if g_save[-1][3] < len(g_copast) else len(g_copast)
        curs = 1 if curs == 0 else curs
        g_save.append(('p', None, g_copast, curs) + g_save[-1][4:6] + (line_handler(g_copast,0)))
    
def paste_line_above() -> None:
    """
    Paste the clipboard content above the current row.

    If g_copast is empty, does nothing; otherwise,
    inserts the copied text as a new line immediately above the cursor row,
    positions the cursor on that line, and records the new state.

    Returns:
        None
    """
    global g_save, g_copast
    if g_copast == None:
        g_save.append(('P', None) + g_save[-1][2:8])
    elif g_save[-1][7] == [] and g_copast != None:
        o = len(g_copast) if len(g_copast)>0 else 1
        g_save.append(('P', None, g_copast, o) + g_save[-1][4:6] + (1, [[""]]))
    else:
        curs = g_save[-1][3] if g_save[-1][3] < len(g_copast) else len(g_copast)
        curs = 1 if curs == 0 else curs
        g_save.append(('P', None, g_copast, curs) + g_save[-1][4:6] + (line_handler(g_copast,1)))
    
def delete_line() -> None:
    """
    Delete the current row from the screen buffer.

    Removes the active row; if multiple rows remain, moves the cursor to the next or
    previous valid line, otherwise resets to a single empty line.
    Records the resulting state in g_save.

    Returns:
        None
    """
    global g_save
    tog1, tog2 = g_save[-1][4:6]
    if len(g_save[-1][7]) > 1 and len(g_save)>1:
        curs = g_save[-1][6] 
        screen = [val for i, val in enumerate(g_save[-1][7]) if i != curs - 1]
        m = -1 if g_save[-1][6] == len(g_save[-1][7]) != 1 else 0
        cont = screen[curs - 1 + m][0]
        cursor = g_save[-1][3] if g_save[-1][3] < len(cont) else len(cont)
        cursor = 1 if cursor == 0 else cursor
        g_save.append(('dd', None, cont, cursor) + g_save[-1][4:6] + (curs + m, screen))   
    else:
        g_save.append(('dd', None, "", 1, tog1, tog2, 1, []))

def insert_line_below() -> None:
    """
    Insert an empty line below the current cursor row.

    Adds a blank row immediately after the current row, resets the edit buffer to empty,
    positions the cursor on the new line, and appends the updated state.

    Returns:
        None
    """
    global g_save
    if len(g_save[-1][7]) == 0:
        g_save.append(('o', None, "", 1) + g_save[-1][4:6] + (g_save[-1][6], [[""]]))
    else:
        g_save.append(('o', None, "", 1) + g_save[-1][4:6] + (line_handler("",0)))

def insert_line_above() -> None:
    """
    Insert an empty line above the current cursor row.

    Adds a blank row immediately before the current row, clears the edit buffer,
    keeps focus on the newly inserted line, and logs the new state.

    Returns:
        None
    """
    global g_save
    if len(g_save[-1][7]) == 0:
        g_save.append(('O', None, "", 1) + g_save[-1][4:6] + (g_save[-1][6], [[""]]))
    else:
        g_save.append(('O', None, "", 1) + g_save[-1][4:6] + (line_handler("",1)))

def line_handler(content: str, up_down: int) -> tuple[int, list[list[str]]]:
    """
    Helper to insert a new line in the screen buffer.

    Takes `content` for the new row and `up_down` as 0 (below) or 1 (above),
    clones the existing buffer, applies the insertion, and returns the new
    cursor-row index along with the updated screen list.

    Args:
        content (str): Text for the newly inserted line.
        up_down (int): 0 to insert below the cursor row; 1 to insert above.

    Returns:
        Tuple[int, List[List[str]]]: (new_cursor_row, updated_screen_buffer)
    """
    global g_save
    curs = g_save[-1][6]
    screen = [val for val in g_save[-1][7]]
    screen[curs-1][0] = g_save[-1][2]
    screen.insert(curs - up_down, [content])
    return curs + 1 - up_down, screen

def toggle_line_cursor() -> None:
    """
    Toggle the line-level cursor visibility flag.

    Inverts the `cursor_visible` toggle used for line highlighting,
    leaves other state unchanged, and appends the new state to g_save.

    Returns:
        None
    """
    global g_save
    okeik = (g_save[-1][4], not g_save[-1][5])
    g_save.append((';', None) + g_save[-1][2:4] + okeik + g_save[-1][6:8])

def undo_last_action() -> None:
    """
    Undo the last editing action.

    Reverts the editor to its previous state by removing the most recent state from g_save, 
    provided that more than one state is stored. This allows the user to step back through their changes.

    Returns:
        None
    """
    global g_save
    edit_cont, cursor_pos = g_save[-1][2:4]
    if len(g_save)>1:
        g_save.pop()


def repeat_last_action() -> None:
    """
    Repeat the last valid editing action.

    Retrieves the last action (and its associated user input) from g_save and uses the 
    command mapping (g_command_map) to re-execute that action. This allows the user to repeat the 
    previous command without retyping it.

    Returns:
        None
    """
    global g_save, g_user_input
    if len(g_save)>1:
        action, g_user_input = g_save[-1][0:2]
        if action not in ["a","i"]:
            g_user_input = action
        g_command_map[action]()


g_command_map.update({
'q': lambda: exit(),'a': lambda: append_text(g_user_input[1:]),
'i': lambda: insert_text(g_user_input[1:]),'h': move_cursor_left,'l': move_cursor_right,
'^': move_cursor_beginning,'$': move_cursor_end,'w': move_cursor_next_word,
'b': move_cursor_prev_word,'x': delete_char,'dw': delete_word,
'u': undo_last_action,'r': repeat_last_action,".": turn_cursor_on_off,'j': move_cursor_up,
'k': move_cursor_down,'yy': copy_line,'p': paste_line_below,'P': paste_line_above,
'dd': delete_line,'o': insert_line_below,'O': insert_line_above,';': toggle_line_cursor,
's': lambda: g_save.append((('s', None) + g_save[-1][2:8])),
'?': lambda: print("\n".join([
    "? - display this help info",". - toggle row cursor on and off",
    "; - toggle line cursor on and off","h - move cursor left","j - move cursor up",
    "k - move cursor down","l - move cursor right","^ - move cursor to beginning of the line",
    "$ - move cursor to end of the line","w - move cursor to beginning of next word",
    "b - move cursor to beginning of previous word",
    "i - insert <text> before cursor","a - append <text> after cursor",
    "x - delete character at cursor","dw - delete word and trailing spaces at cursor",
    "yy - copy current line to memory","p - paste copied line(s) below line cursor",
    "P - paste copied line(s) above line cursor","dd - delete line",
    "o - insert empty line below","O - insert empty line above",
    "u - undo previous command","r - repeat last command",
    "s - show content","q - quit program"
    ]))})


if __name__ == "__main__":
    """
    Run the text editor in an interactive loop.

    This main loop continuously prompts the user for input. Depending on the command entered, it either 
    processes text insertion/appending (when extra text is provided) or executes the corresponding command 
    from g_command_map. After each command, it displays the current editor state via display_cont.

    Returns:
        None
    """
    while True:
        g_user_input = input(">")       
        if g_user_input.startswith(('i','a')) and len(g_user_input)>1:
            g_command_map[g_user_input[0]]()
            display_cont()
        elif g_user_input in g_command_map and not g_user_input.startswith(('i','a')):
            g_command_map[g_user_input]()
            display_cont() if g_user_input[0] != "?" else None