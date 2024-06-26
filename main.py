from tkinter import *
from tkinter import ttk
from string import ascii_uppercase as upper
from PIL import ImageTk,Image
import os
import glob
from Text_File_Functions import *
from Piece import Piece
from King import King
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn
from datetime import datetime

##declare all classes
k=King()
q=Queen()
ro=Rook()
b=Bishop()
kn=Knight()
pa=Pawn()
p=Piece()

table = Tk()
table.title("Chess")
table.geometry("1200x600")
#window=Toplevel(table)
#btn_frame=Button(window, text="ahoj").grid(row=13,column=13)
##create labels that will be used for giving players information
name_txt_label=Label(table,text="White player is on turn",width=30,height=2,relief=RAISED)
name_txt_label.grid(row=0,column=11)
inf_txt_label=Label(table,text="Information window:",width=20,height=2).grid(row=1,column=10)
txt_inf_label=Label(table,text="",width=50,height=2,relief=RAISED)
txt_inf_label.grid(row=1,column=11)
movement_txt_label=Label(table,text="Movement window:",width=20,height=2).grid(row=2,column=10)
txt_movement_label=Label(table,text="",width=50,height=2,relief=RAISED)
txt_movement_label.grid(row=2,column=11)

##create chessboard, 0 represents empty empty squere, each type of chess piece gets uniqe id, white pieces have 1-6, black pieces have 7-12
chess_board=[[0 for i in range(8)] for j in range(8)]     
chess_board[0][4]=1   ##white king
chess_board[0][3]=2   ##white queen
chess_board[0][2]=3;chess_board[0][5]=3   ##white bishops
chess_board[0][1]=4;chess_board[0][6]=4   ##white knights
chess_board[0][0]=5;chess_board[0][7]=5   ##white rooks
chess_board[1]=[6 for i in range(8)]    ##white pawns

chess_board[7][4]=7   ##black king
chess_board[7][3]=8   ##black queen
chess_board[7][2]=9;chess_board[7][5]=9   ##black bishops
chess_board[7][1]=10;chess_board[7][6]=10  ##black knights
chess_board[7][0]=11;chess_board[7][7]=11  ##black rooks
chess_board[6]=[12 for i in range(8)]   ##black pawns 

before_chess_board=[row.copy() for row in chess_board]

##import images of numbers and letters that will be used for making border of chessboard
numbers_arr=[]
letters_arr=[]
for i in range(8):
    numbers_arr.append(ImageTk.PhotoImage(Image.open(f"icons/numbers_letters/{i+1}.png")))
    letters_arr.append(ImageTk.PhotoImage(Image.open(f"icons/numbers_letters/{upper[i]}.png")))

##import images of pieces with white background
img_white_arr=[]
for filename in glob.glob("icons/pieces_white_background/*.png"):
    im=ImageTk.PhotoImage(Image.open(filename))
    img_white_arr.append(im)

##import images of pieces with grey background
img_grey_arr=[]
for filename in glob.glob("icons/pieces_grey_background/*.png"):
    im=ImageTk.PhotoImage(Image.open(filename))
    img_grey_arr.append(im)

##import images of pieces with red background
img_red_arr=[]
for filename in glob.glob("icons/pieces_red_background/*.png"):
    im=ImageTk.PhotoImage(Image.open(filename))
    img_red_arr.append(im)

##import images of pieces with green background
img_green_arr=[]
for filename in glob.glob("icons/pieces_green_background/*.png"):
    im=ImageTk.PhotoImage(Image.open(filename))
    img_green_arr.append(im)

##import images of pieces with blue background
img_blue_arr=[]
for filename in glob.glob("icons/pieces_blue_background/*.png"):
    im=ImageTk.PhotoImage(Image.open(filename))
    img_blue_arr.append(im)

##create buttons that will be used for making corner of chessboard
corner_arr=[[0,0],[0,9],[9,0],[9,9]]        ##array that keeps coordinates of each corner
for i in range(4):
    r,c=corner_arr[i]
    Button(table,image=img_white_arr[0],state=DISABLED).grid(row=r,column=c)

##create buttons that will be used for making border of chessboard
for i in range(8):
    Button(table,image=numbers_arr[i],state=DISABLED).grid(row=i+1,column=0)
    Button(table,image=letters_arr[i],state=DISABLED).grid(row=0,column=i+1)
    Button(table,image=numbers_arr[i],state=DISABLED).grid(row=i+1,column=9)
    Button(table,image=letters_arr[i],state=DISABLED).grid(row=9,column=i+1)

btn_arr=[[] for i in range(8)]      ##create 2D array to save all buttons, that represents one squere
for i in range(8):
    for j in range(8):
        ##loading buttons to array, I can use id from chess_board to load right image of piece to specific square
        if((i+j)%2==0):     ##changing grey and white background
            btn_arr[i].append(Button(table,image=img_grey_arr[chess_board[i][j]],command=lambda row=i,column=j:click_piece(row,column)))
            btn_arr[i][-1].grid(row=i+1,column=j+1) 
        else:
            btn_arr[i].append(Button(table,image=img_white_arr[chess_board[i][j]],command=lambda row=i,column=j:click_piece(row,column))) 
            btn_arr[i][-1].grid(row=i+1,column=j+1) 
opt_table = [[0 for i in range(8)] for j in range(8)]
turn_number = 0
turns_back = 0
movement_back = False
current_date = datetime.today().strftime('%Y-%m-%d, %H-%M-%S') + ".txt"
white_on_turn=True      ##variable that signals which player is on turn, white player starts
already_picked=False    ##variable that signals if player has choosen piece to move
WK_position=[0,4]
BK_position=[7,4]
before_WK_position=WK_position.copy()
before_BK_position=BK_position.copy()
castling=[[True,True],[True,True]]      ##variable that has 4 bool values, each for one rook, signaling if rook has already made move, if king would move, his array will be set to twice False
before_castling=[row.copy() for row in castling]
en_passant_arr=[[False for i in range(8)] for j in range(2)]    ##array for saving information, that specific pawn has moved 2 squares ahead (first array for white pawns, second for black pawns)
before_en_passant_arr=[row.copy() for row in en_passant_arr]
save_turn(current_date, chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr)

##function that clears all green and blue background, or reloads images to all butons based on their id in white and grey background if reset_all=True
def white_background_all(reset_all,row,column,opt_table):
    for i in range(8):
        for j in range(8):
            if(opt_table[i][j]!=0 or (i==row and j==column) or reset_all):     ##
                ##loading right image with white or grey background to each button by using id from chessboard
                if((i+j)%2==0):     ##changing grey and white background(in the way that grey squares has border with white ones and vice versa)
                    btn_arr[i][j].configure(image=img_grey_arr[chess_board[i][j]])
                else:                
                    btn_arr[i][j].configure(image=img_white_arr[chess_board[i][j]])

##function that loads last turn
def turn_back():
    global chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr, turn_number, already_picked, movement_back, turns_back
    turn_number -= 1
    turns_back += 1
    btn_forward.configure(state = ACTIVE)
    movement_back = True
    turn.set("Turn " + str(turn_number))
    chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr = load_turn(current_date, turn_number)
    white_background_all(True, 0, 0, opt_table)
    if white_on_turn:
        name_txt_label.configure(text="White player is on the turn")
    else:
        name_txt_label.configure(text="Black player is on the turn")
    txt_inf_label.configure(text = "")
    txt_movement_label.configure(text = "")
    if(turn_number == 0): btn_back.configure(state = DISABLED)
        

def turn_forward():
    global chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr, turn_number, already_picked, movement_back, turns_back
    turn_number += 1
    turns_back -= 1 
    turn.set("Turn " + str(turn_number))
    chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr = load_turn(current_date, turn_number)
    white_background_all(True, 0, 0, opt_table)
    if white_on_turn:
        name_txt_label.configure(text="White player is on the turn")
    else:
        name_txt_label.configure(text="Black player is on the turn")
    txt_inf_label.configure(text = "")
    txt_movement_label.configure(text = "")
    if(turns_back == 0): btn_forward.configure(state = DISABLED)  

def choose_turn():
    turns_window = Toplevel(table)
    all_turns = turn_number + turns_back + 1
    choosen_turn = StringVar()

    ##function that will be called after player clicked on specific turn
    def clicked_combobox(var, indx, mode):
        global turn_number, turns_back, movement_back
        turn_str = choosen_turn.get()
        turn_number = int(turn_str.split(" ")[1]) + 1
        turns_back = all_turns - turn_number - 1
        turn_back()
        if(turn_number == 0): btn_back.configure(state = DISABLED)            
        elif(turn_number == all_turns - 1): 
            btn_forward.configure(state = DISABLED)
            movement_back = False
        turns_window.destroy()

    turns_list = ["turn " + str(i) for i in range(all_turns)]
    combo_turns = ttk.Combobox(turns_window, values = turns_list, textvariable = choosen_turn, state = "readonly")
    combo_turns.set("Choose turn")
    choosen_turn.trace_add("write", clicked_combobox)
    combo_turns.grid(row = 0, column = 0)
    turns_window.mainloop()

turns_window = Frame(table)
turns_window.grid(row = 5, column = 11, sticky = "N")
turn = StringVar(table, "Turn 0")
btn_current_turn = Button(turns_window, textvariable = turn, width=10, height = 2, font = ("Arial", 9), command = choose_turn).grid(row = 0, column = 1)
btn_back = Button(turns_window, text = "<<", width = 5, height = 2, font = ("Arial", 9), command = turn_back, state = DISABLED)
btn_back.grid(row = 0, column = 0, sticky = "E")
btn_forward = Button(turns_window, text = ">>", width = 5, height = 2, font = ("Arial", 9), command = turn_forward, state = DISABLED)
btn_forward.grid(row = 0, column = 2, sticky = "W")

##function that will load different save, after player writes name of it
def load_dif_file():
    global current_date, turn_number, turns_back
    name_open_file = entry_widget.get()
    entry_widget.delete(0, END)
    if(not os.path.isfile(f"saves/{name_open_file}.txt")):
        txt_inf_label.configure(text = "name of the file is incorrect")
        return
    with open(f"saves/{name_open_file}.txt", "r") as original_file:
        copy_file = open(f"saves/copy_{name_open_file}.txt", "w")
        for line_number, line in enumerate(original_file):
            copy_file.write(line)
        turn_number = int((line_number - 5)/6)  - 1
        copy_file.close()
    current_date = f"copy_{name_open_file}.txt"
    turns_back = 1
    turn_forward()


Label(table, text = "If you want to load different save, enter a name (without .txt):", font = ("Arial", 9), height = 2, relief = RAISED, padx = 5).grid(row = 3, column = 11, sticky = "S")
entry_widget = Entry(table, font = ("Arial", 9), width = 47)
entry_widget.grid(row = 4, column = 11)
Button(table, text = "Enter", command = load_dif_file, height = 2).grid(row = 4, column = 12)


##function that returns name of piece base on their id
def piece_name(id):
    if id==0:
        return "empty square"
    elif id==1:
        return "white king"
    elif id==2:
        return "white queen"
    elif id==3:
        return "white bishop"
    elif id==4:
        return "white knight"
    elif id==5:
        return "white rook"
    elif id==6:
        return "white pawn"
    elif id==7:
        return "black king"
    elif id==8:
        return "black queen"
    elif id==9:
        return "black bishop"
    elif id==10:
        return "black knight"
    elif id==11:
        return "black rook"
    elif id==12:
        return "black pawn"
    else:
        print("wrong id")
            
##function that is called after clicking gaming button
def click_piece(row,column):
    global before_chess_board,WK_position,BK_position,already_picked,id_before,row_before,column_before,opt_table,chess_board,white_on_turn,en_passant_arr,before_BK_position,before_WK_position,before_en_passant_arr,before_castling, turn_number, movement_back, turns_back
    id=chess_board[row][column]     
    white=p.is_white(id)            ##loading information about square/piece that was clicked
    
    ##function that updates kings position 
    def update_king(this_id,this_row,this_column):
        global WK_position,BK_position
        if(this_id==1):
            WK_position=[this_row,this_column]        ##if moving piece is white king, array that keeps his position is updated
        elif(this_id==7):
            BK_position=[this_row,this_column]        ##if moving piece is black king, array that keeps his position is updated
    
    ##based on id of piece, function calls right Option function of pieces class, prints error on console if id does not match piece
    def switch_opt_fct(row,column,chess_board,white,id,castling,en_passant_arr):
        if id==0:
            print("Empty square does not have options function")
        elif id==1 or id==7:
            opt_table=k.Options(row,column,chess_board,white,castling)   ##finish castling
            return opt_table
        elif id==2 or id==8:
            opt_table=q.Options(row,column,chess_board,white)
            return opt_table
        elif id==3 or id==9:
            opt_table=b.Options(row,column,chess_board,white)
            return opt_table
        elif id==4 or id==10:
            opt_table=kn.Options(row,column,chess_board,white)
            return opt_table
        elif id==5 or id==11:
            opt_table=ro.Options(row,column,chess_board,white)
            return opt_table
        elif id==6 or id==12:
            opt_table=pa.Options(row,column,chess_board,white,en_passant_arr)   ##finish el passant
            return opt_table
        else:
            print("You called function with bad id")        
    
    ##function that returns two bools symbolizing if in current chess_board is white or black king in chess
    def find_check(local_chess_board):
        global WK_position,BK_position
        WK_check=False  ##bool variable that signals if white king is in check
        BK_check=False  ##bool variable that signals if black king is in check
        ##loop for searching chess_board
        for local_row in range(8):
            for local_column in range(8):     
                local_id=local_chess_board[local_row][local_column]     ##getting id of specific square
                if(local_id!=0):                  ##current coordinates does not select empty square 
                    local_white=p.is_white(local_id)    ##getting color of piece
                    local_opt_table=switch_opt_fct(local_row,local_column,local_chess_board,local_white,local_id,castling,en_passant_arr)   ##calling function to find out possible optins where can piece move
                    if(local_white):
                        if(local_opt_table[BK_position[0]][BK_position[1]]!=0):   
                            BK_check=True       ##if the piece is white and can move to coordinates of black king, black king is in check
                    else:
                        if(local_opt_table[WK_position[0]][WK_position[1]]!=0):
                            WK_check=True       ##if the piece is black and can move to coordinates of white king, white king is in check
                if(BK_check and WK_check):
                    return WK_check,BK_check    ##if both kings are in check, there is no need to search if some other piece gets them in check
        return WK_check,BK_check        ##returns information about checks on kings
    
    ##function that removes possibility to do castling if enemy rook was taken
    def taken_enemy_rook(row, column, id_before):
        global castling
        white = p.is_white(id_before)
        if(white):
            if(castling[1][0] and row == 7 and column == 0):
                castling[1][0] = False
            elif(castling[1][1] and row == 7 and column == 7):
                castling[1][1] = False
        else:
            if(castling[0][0] and row == 0 and column == 0):
                castling[0][0] = False
            elif(castling[0][1] and row == 0 and column == 7):
                castling[0][1] = False

    ##function for promotion of pawn, will print window with every piece(except pawn) and player will choose witch piece to promote
    def promotion():        
        promotion_window=Toplevel(table)
        promotion_window.title("promotion")

        ##function that promotes pawn to piece that player has choosen
        def promote(index):
            global chess_board
            chess_board[row][column]=index
            promotion_window.destroy()
            promotion_window.quit()
            
        white=p.is_white(id_before)
        if(white):
            dif=0
        else:
            dif=6
        Label(promotion_window,text="Choose witch piece you want to promote:").grid(row=0,columnspan=4)
        for i in range(2,6):
            Button(promotion_window,image=img_white_arr[i+dif],command=lambda index=i+dif:promote(index)).grid(row=1,column=i-2)
        promotion_window.mainloop()

    def chosen():                   ##function that is called if player chooses piece that he wants to move
        opt_table=switch_opt_fct(row,column,chess_board,white,id,castling,en_passant_arr)      ##returns 2D array with possible options to move
        for i in range(8):
            for j in range(8):
                if(opt_table[i][j]!=0):        ##every square where is possible to move piece, will have it´s background to green
                    btn_arr[i][j].configure(image=img_green_arr[chess_board[i][j]])
        return opt_table

    ##after player ends his turn, this function resets variables that signals player has choosen piece and writes on name label that oponnent is on turn
    def change_players():
        global already_picked, id_before, row_before, column_before, white_on_turn
        already_picked=False
        id_before=None                  ##resets variables that signals player has already choosen piece to move
        white_background_all(True,row,column,opt_table)      ##reloads grey and white background to all squares
        white_on_turn = not white_on_turn       ##change variable that signals which player is on turn
        if white_on_turn:
            name_txt_label.configure(text="White player is on the turn")
        else:
            name_txt_label.configure(text="Black player is on the turn")
        return

    ##function that tests players move, if his king would be in check, function returns False and prints information, if enemy king is in check, function returns True and prints the information, if no king is in check returns True
    def move_help_fct(test_chess_board):
        global WK_position,BK_position
        update_king(id_before,row,column)
        checks=find_check(test_chess_board)     ##calling function that returns array of two bool variables, first signals that white king is in check(if True), second that black king is in check(if True)
        white=p.is_white(id_before)         ##loading color of moving piece
        if((white and checks[0]) or (not white and checks[1])):     ##after move, players king would be in check
            txt_inf_label.configure(text="your king is in check, you have to another move")     ##printing the information
            update_king(id_before,row_before,column_before)
            return False
        elif((white and checks[1]) or (not white and checks[0])):       ##after move, enemy king is in check
            if(white):
                txt_inf_label.configure(text="black king is in check")
            else:
                txt_inf_label.configure(text="white king is in check")  ##prints the information
        return True

    ##function that finds out if it is possible to do castling after player wants to
    def castling_possible():
        local_white=p.is_white(id_before)
        if(column==6):
            dir=1
        elif(column==2):
            dir=-1
        if(local_white):
            index=0
        else:
            index=1
        test_castling_chess_board=[row.copy() for row in chess_board]    ##making deep copy of chess_board
        for i in range(1,3):
            test_castling_chess_board[row_before][column_before+i*dir]=id_before 
            update_king(id_before,row_before,column_before+i*dir)
            is_check=find_check(test_castling_chess_board)[index]
            if(is_check):
                if(i==1):
                    txt_inf_label.configure(text="king would cross square that is attacked by enemy piece")
                    
                elif(i==2):
                    txt_inf_label.configure(text="king would end on square that is attacked by enemy piece")  ##prints the information
                update_king(id_before,row_before,column_before)
                return False
        update_king(id_before,row,column)
        return True    
        
    ##function that controls movement of kings and rooks(information that we need to find out if castling is possible
    def movement_king_rook():
        global castling
        local_white=p.is_white(id_before)
        kings_id=[1,7]
        if(local_white):
            base_row=0
            index=0
        else:
            base_row=7
            index=1
        if((True in castling[index]) and id_before==kings_id[index]):
            castling[index]=[False,False]
        if(castling[index][0] and row_before==base_row and column_before==0):
            castling[index][0]=False
        if(castling[index][1] and row_before==base_row and column_before==7):
            castling[index][1]=False       

    ##function that sets id of moving piece to it´s new position and saves 0 to it´s old position
    def move_piece():
        if(p.is_white(id_before)):
            dir=-1
        else:
            dir=1
        test_chess_board=[row.copy() for row in chess_board]    ##making deep copy of chess_board
        test_chess_board[row][column]=id_before          ##setting id of moving piece to clicked square on testing chest board
        test_chess_board[row_before][column_before]=0    ##setting empty square on previous square of piece on testing chest board
        if(opt_table[row][column]==5):
            test_chess_board[row+dir][column]=0          ##clearing enemy pawn after making en passant move
        can_move=move_help_fct(test_chess_board)         ##calling function that returns true if player can do the move(players king is not in check) or not(returns False)
        if(can_move):
            chess_board[row][column]=id_before          ##setting id of moving piece to clicked square
            chess_board[row_before][column_before]=0    ##setting empty square on previous square of piece
            if(opt_table[row][column]==5):
                chess_board[row+dir][column]=0          ##clearing enemy pawn after making en passant move
            movement_king_rook()
            return True
        else:
            return False

    if(not already_picked):       ##player has not yet choosen piece to move
        if(id==0):      ##player chooses empty square
            txt_inf_label.configure(text="You can not choose empty square if you want to move piece")
            return 
        if((not white and white_on_turn) or (white and not white_on_turn)):  ##player chooses piece of his oponent 
            txt_inf_label.configure(text="this is not your piece")
        else:           ##player chooses his piece        
            txt_inf_label.configure(text="")
            already_picked=True     ##next time will player click where he wants to move
            btn_arr[row][column].configure(image=img_blue_arr[id])
            id_before=id
            row_before=row
            column_before=column
            opt_table=chosen()      ##calls function that will return 2D array of possible options to move and changes background of that pieces to green
    else:       ##player has already choosen piece to move, now he chooses where to go
        if(row==row_before and column==column_before):   ##after choosing specific piece, player clicks on it again, meaning he wants to choose diferent piece
            txt_inf_label.configure(text="")
            white_background_all(False,row,column,opt_table)  ##clears all green and blue background
            already_picked=False    
            return
        elif(opt_table[row][column]==0):    ##player clicks on square where piece can not move
            txt_inf_label.configure(text="You can not move your piece here")
            return
        elif(opt_table[row][column]==1 or opt_table[row][column]==4):    ##player clicks on empty square where piece can move
            txt_inf_label.configure(text="")
            success=move_piece()                    ##function that sets id of moving piece to it´s new position and saves 0 to it´s old position
            if(success):
                if((p.is_white(id_before) and row==7 and id_before==6)or(not p.is_white(id_before) and row==0 and id_before==12)):     ##promotion of pawn    
                    promotion()
                txt_movement_label.configure(text=""+piece_name(id_before)+" went from "+upper[column_before]+""+str(row_before+1)+" to "+upper[column]+""+str(row+1))   ##prints to information window information about the move
                en_passant_arr=[[False for i in range(8)] for j in range(2)]
                if(opt_table[row][column]==4):
                    if(p.is_white(id_before)):
                        en_passant_arr[0][column]=True
                    else:
                        en_passant_arr[1][column]=True
                change_players()                ##this function resets variables that signals player has choosen piece and writes on name label that oponnent is on turn
                if(movement_back):
                    copy_save(current_date, turn_number)
                    movement_back = False
                save_turn(current_date, chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr)
                btn_back.configure(state = ACTIVE)
                turn_number += 1
                turns_back = 0
                btn_forward.configure(state = DISABLED)
                turn.set("Turn " + str(turn_number))
                
            else:
                white_background_all(True,row,column,opt_table)
                already_picked=False
            return
        elif(opt_table[row][column]==2 or opt_table[row][column]==5):    ##player clicks on enemy piece which can his choosen piece take or player has choosen to do en passant move
            txt_inf_label.configure(text="")
            success=move_piece()                    ##function that sets id of moving piece to it´s new position and saves 0 to it´s old position
            if(success):
                if((p.is_white(id_before) and row==7 and id_before==6)or(not p.is_white(id_before) and row==0 and id_before==12)):     ##promotion of pawn    
                    promotion()
                else:
                    taken_enemy_rook(row, column, id_before)
                en_passant_arr=[[False for i in range(8)] for j in range(2)]
                if(opt_table[row][column]!=5):
                    txt_movement_label.configure(text=""+piece_name(id_before)+" went from "+upper[column_before]+""+str(row_before)+" to "+upper[column]+""+str(row)+" and took "+piece_name(id))   ##prints to information window information about the move
                else:
                    txt_movement_label.configure(text=""+piece_name(id_before)+" made en passant move from "+upper[column_before]+""+str(row_before)+" to "+upper[column]+""+str(row)+" and took "+piece_name(id))   ##prints to information window information about the en passant move
                change_players()                ##this function resets variables that signals player has choosen piece and writes on name label that oponnent is on turn
                if(movement_back):
                    copy_save(current_date, turn_number)
                    movement_back = False
                save_turn(current_date, chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr)
                btn_back.configure(state = ACTIVE)
                turn_number += 1
                turns_back = 0
                btn_forward.configure(state = DISABLED)
                turn.set("Turn " + str(turn_number))
            else:
                white_background_all(True,row,column,opt_table)
                already_picked=False

            return
        elif(opt_table[row][column]==3):    ##player wants to make castling
            txt_inf_label.configure(text="")
            success=castling_possible()                    ##function that finds out if king does not cross over or end on square attacked by enemy piece
            if(success):
                en_passant_arr=[[False for i in range(8)] for j in range(2)]
                local_white=p.is_white(id_before)
                if(local_white):
                    rook_id=5
                else:
                    rook_id=11
                chess_board[row][column]=id_before          ##setting id of moving piece to clicked square
                chess_board[row_before][column_before]=0    ##setting empty square on previous square of piece
                movement_king_rook()
                if(column==2):
                    castling_name="queenside"
                    chess_board[row_before][0]=0
                    chess_board[row_before][3]=rook_id
                elif(column==6):
                    castling_name="kingside"
                    chess_board[row_before][7]=0
                    chess_board[row_before][5]=rook_id
                txt_movement_label.configure(text=""+piece_name(id_before)+" castled "+castling_name)   ##prints to information window information about the move
                change_players()                ##this function resets variables that signals player has choosen piece and writes on name label that oponnent is on turn
                if(movement_back):
                    copy_save(current_date, turn_number)
                    movement_back = False
                save_turn(current_date, chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr)
                btn_back.configure(state = ACTIVE)
                turn_number += 1
                turns_back = 0
                btn_forward.configure(state = DISABLED)
                turn.set("Turn " + str(turn_number))
            else:

                white_background_all(True,row,column,opt_table)
                already_picked=False
            return

table.mainloop()



