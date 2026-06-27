"""
Tic Tac Toe - Tkinter GUI
Two players or vs AI on a styled 3x3 grid.
"""

import tkinter as tk
from tkinter import font as tkfont


# ── Theme ──────────────────────────────────────────────────────────────────
THEME = {
    "bg": "#1a1b26",
    "surface": "#24283b",
    "surface_hover": "#2f3549",
    "border": "#414868",
    "text": "#c0caf5",
    "text_muted": "#787c99",
    "accent": "#7aa2f7",
    "x_color": "#f7768e",
    "o_color": "#7dcfff",
    "win": "#9ece6a",
    "draw": "#e0af68",
    "btn_primary": "#7aa2f7",
    "btn_primary_text": "#1a1b26",
    "btn_secondary": "#414868",
    "btn_secondary_text": "#c0caf5",
}

MARGIN = 28
CELL_PAD = 6
CELL_SIZE = 110


# ── Game logic ─────────────────────────────────────────────────────────────
def check_winner(board):
    win_combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for a, b, c in win_combos:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    return None, None


def is_board_full(board):
    return " " not in board


def get_available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]


def minimax(board, is_maximizing, ai_player, human_player):
    winner, _ = check_winner(board)
    if winner == ai_player:
        return 1
    if winner == human_player:
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for move in get_available_moves(board):
            board[move] = ai_player
            score = minimax(board, False, ai_player, human_player)
            board[move] = " "
            best_score = max(best_score, score)
        return best_score

    best_score = float("inf")
    for move in get_available_moves(board):
        board[move] = human_player
        score = minimax(board, True, ai_player, human_player)
        board[move] = " "
        best_score = min(best_score, score)
    return best_score


def get_ai_move(board, ai_player, human_player):
    best_score = -float("inf")
    best_move = None
    for move in get_available_moves(board):
        board[move] = ai_player
        score = minimax(board, False, ai_player, human_player)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


# ── GUI ────────────────────────────────────────────────────────────────────
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=THEME["bg"])
        self.root.resizable(False, False)

        self.board = [" "] * 9
        self.buttons = []
        self.vs_ai = False
        self.human_player = "X"
        self.ai_player = "O"
        self.current_player = "X"
        self.game_over = False
        self.winning_cells = None

        self.title_font = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.status_font = tkfont.Font(family="Segoe UI", size=13)
        self.cell_font = tkfont.Font(family="Segoe UI", size=36, weight="bold")
        self.btn_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)

        self._build_shell()
        self._show_menu()

    def _build_shell(self):
        self.outer = tk.Frame(self.root, bg=THEME["bg"], padx=MARGIN, pady=MARGIN)
        self.outer.pack(fill="both", expand=True)

        self.card = tk.Frame(
            self.outer,
            bg=THEME["surface"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
            padx=MARGIN,
            pady=MARGIN,
        )
        self.card.pack()

        self.title_label = tk.Label(
            self.card,
            text="Tic Tac Toe",
            font=self.title_font,
            fg=THEME["accent"],
            bg=THEME["surface"],
        )
        self.title_label.pack(pady=(0, 4))

        self.subtitle_label = tk.Label(
            self.card,
            text="",
            font=self.subtitle_font,
            fg=THEME["text_muted"],
            bg=THEME["surface"],
        )
        self.subtitle_label.pack(pady=(0, 16))

        self.content = tk.Frame(self.card, bg=THEME["surface"])
        self.content.pack()

        self.status_label = tk.Label(
            self.card,
            text="",
            font=self.status_font,
            fg=THEME["text"],
            bg=THEME["surface"],
            pady=14,
        )
        self.status_label.pack()

        self.footer = tk.Frame(self.card, bg=THEME["surface"])
        self.footer.pack(pady=(8, 0))

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        for widget in self.footer.winfo_children():
            widget.destroy()
        self.buttons.clear()

    def _make_button(self, parent, text, command, primary=False):
        bg = THEME["btn_primary"] if primary else THEME["btn_secondary"]
        fg = THEME["btn_primary_text"] if primary else THEME["btn_secondary_text"]
        btn = tk.Button(
            parent,
            text=text,
            font=self.btn_font,
            bg=bg,
            fg=fg,
            activebackground=THEME["accent"],
            activeforeground=THEME["btn_primary_text"],
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=10,
            command=command,
        )
        btn.pack(pady=6, fill="x")
        btn.bind("<Enter>", lambda e, b=btn, p=primary: self._on_btn_enter(b, p))
        btn.bind("<Leave>", lambda e, b=btn, p=primary: self._on_btn_leave(b, p))
        return btn

    def _on_btn_enter(self, btn, primary):
        btn.configure(bg=THEME["accent"] if primary else THEME["surface_hover"])

    def _on_btn_leave(self, btn, primary):
        bg = THEME["btn_primary"] if primary else THEME["btn_secondary"]
        btn.configure(bg=bg)

    def _show_menu(self):
        self._clear_content()
        self.game_over = True
        self.subtitle_label.configure(text="Choose a game mode")
        self.status_label.configure(text="", fg=THEME["text"])

        menu = tk.Frame(self.content, bg=THEME["surface"], padx=12, pady=8)
        menu.pack()

        self._make_button(
            menu, "Two Players", lambda: self._start_game(vs_ai=False), primary=True
        )
        self._make_button(
            menu, "Play vs AI", lambda: self._show_ai_setup(), primary=False
        )

    def _show_ai_setup(self):
        self._clear_content()
        self.subtitle_label.configure(text="Play against the computer")
        self.status_label.configure(text="Pick your symbol", fg=THEME["text_muted"])

        setup = tk.Frame(self.content, bg=THEME["surface"], padx=12, pady=8)
        setup.pack()

        self._make_button(
            setup,
            "Play as X  (go first)",
            lambda: self._start_game(vs_ai=True, human="X"),
            primary=True,
        )
        self._make_button(
            setup,
            "Play as O  (go second)",
            lambda: self._start_game(vs_ai=True, human="O"),
            primary=False,
        )
        self._make_button(setup, "Back", self._show_menu, primary=False)

    def _start_game(self, vs_ai=False, human="X"):
        self.vs_ai = vs_ai
        self.human_player = human
        self.ai_player = "O" if human == "X" else "X"
        self.current_player = "X"
        self.board = [" "] * 9
        self.game_over = False
        self.winning_cells = None

        mode_text = "vs AI" if vs_ai else "Two Players"
        self.subtitle_label.configure(text=mode_text)
        self._build_board()
        self._update_status()
        self._build_footer()

        if vs_ai and self.current_player == self.ai_player:
            self.root.after(400, self._ai_turn)

    def _build_board(self):
        self._clear_content()

        grid_wrap = tk.Frame(self.content, bg=THEME["border"], padx=2, pady=2)
        grid_wrap.pack()

        grid = tk.Frame(grid_wrap, bg=THEME["border"])
        grid.pack()

        for row in range(3):
            for col in range(3):
                idx = row * 3 + col
                cell_frame = tk.Frame(grid, bg=THEME["border"])
                cell_frame.grid(row=row, column=col, padx=CELL_PAD, pady=CELL_PAD)

                btn = tk.Button(
                    cell_frame,
                    text="",
                    font=self.cell_font,
                    width=3,
                    height=1,
                    bg=THEME["bg"],
                    fg=THEME["text"],
                    activebackground=THEME["surface_hover"],
                    relief="flat",
                    cursor="hand2",
                    command=lambda i=idx: self._handle_click(i),
                )
                btn.pack()
                btn.bind("<Enter>", lambda e, b=btn: self._on_cell_enter(b))
                btn.bind("<Leave>", lambda e, b=btn, i=idx: self._on_cell_leave(b, i))
                self.buttons.append(btn)

    def _on_cell_enter(self, btn):
        if not self.game_over and btn.cget("text") == "":
            btn.configure(bg=THEME["surface_hover"])

    def _on_cell_leave(self, btn, idx):
        if self.winning_cells and idx in self.winning_cells:
            btn.configure(bg=THEME["win"])
        elif btn.cget("text") == "":
            btn.configure(bg=THEME["bg"])

    def _build_footer(self):
        self._make_button(self.footer, "New Game", self._show_menu, primary=False)

    def _player_label(self, player):
        if self.vs_ai:
            return "You" if player == self.human_player else "AI"
        return f"Player {player}"

    def _update_status(self, message=None, color=None):
        if message:
            self.status_label.configure(text=message, fg=color or THEME["text"])
            return

        if self.game_over:
            return

        name = self._player_label(self.current_player)
        symbol_color = THEME["x_color"] if self.current_player == "X" else THEME["o_color"]
        self.status_label.configure(
            text=f"{name}'s turn  ({self.current_player})",
            fg=symbol_color,
        )

    def _handle_click(self, idx):
        if self.game_over or self.board[idx] != " ":
            return
        if self.vs_ai and self.current_player == self.ai_player:
            return

        self._place_move(idx)
        if not self.game_over:
            self.current_player = "O" if self.current_player == "X" else "X"
            self._update_status()
            if self.vs_ai and self.current_player == self.ai_player:
                self.root.after(350, self._ai_turn)

    def _place_move(self, idx):
        self.board[idx] = self.current_player
        color = THEME["x_color"] if self.current_player == "X" else THEME["o_color"]
        self.buttons[idx].configure(
            text=self.current_player,
            fg=color,
            bg=THEME["bg"],
            state="disabled",
        )
        self._check_end()

    def _ai_turn(self):
        if self.game_over:
            return
        move = get_ai_move(self.board, self.ai_player, self.human_player)
        if move is not None:
            self._place_move(move)
        if not self.game_over:
            self.current_player = self.human_player
            self._update_status()

    def _check_end(self):
        winner, cells = check_winner(self.board)
        if winner:
            self.game_over = True
            self.winning_cells = cells
            for i in cells:
                self.buttons[i].configure(bg=THEME["win"])
            if self.vs_ai:
                msg = "You win!" if winner == self.human_player else "AI wins!"
            else:
                msg = f"Player {winner} wins!"
            color = THEME["win"] if not self.vs_ai or winner == self.human_player else THEME["x_color"]
            self._update_status(msg, color)
            return

        if is_board_full(self.board):
            self.game_over = True
            self._update_status("It's a draw!", THEME["draw"])


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
