from board import Board, illegal_move_exception
import moves
import tkinter

key_pressed = {
    "Up": moves.UP,
    "Down": moves.DOWN,
    "Left": moves.LEFT,
    "Right": moves.RIGHT,
}

def play_game():
    a = Board()
    print("Welcome to 2048 game.\nPress Esc to quit game.\n\n")
    print(repr(a))
        
    def key(event):
        if(event.keysym in key_pressed):
            try:
                a.move(key_pressed[event.keysym])
                print(repr(a))
            except(illegal_move_exception):
                pass

        if(event.keysym == 'Escape' or not a.has_legal_moves()):
            z = 0
            for i in range(4):
                for j in range(4):
                    if(a[i,j] > z):
                        z = a[i,j]
            print("Your score : "+str(z))
            root.destroy()

    root = tkinter.Tk()
    root.bind_all('<Key>', key)

    # don't show the tkinter window
    root.withdraw()
    root.mainloop()

play_game()
