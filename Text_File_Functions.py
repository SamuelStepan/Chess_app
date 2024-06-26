import os

##function that saves variable to given file
def save_data_to_file(data, txt_file):    
    if(hasattr(data, "__iter__")):
        data_length = len(data)
        for it_index, iterable in enumerate(data):
            if(hasattr(iterable, "__iter__")):
                iterable_length = len(iterable)
                for el_index, element in enumerate(iterable):
                    txt_file.write(str(element))  
                    if(el_index != iterable_length -1): txt_file.write(" ")
                if(it_index != data_length - 1): txt_file.write(",")
            else:
                txt_file.write(str(iterable))
                if(it_index != data_length -1): txt_file.write(" ")
    else: txt_file.write(str(data))
    txt_file.write("\n")
        
##help fucntion that returns True if given string is "True" and False if given string is "False
def is_bool(str):
    if(str == "True"):
        return True
    elif(str == "False"):
        return False
            
##function that loads variable from given file
def load_data_from_file(type, txt_file, opt_line = False):
    array = []
    if(not opt_line): line = txt_file.readline().replace("\n", "")
    else: line = opt_line 
    if("," in line): 
        rows = line.split(",")
        for row in rows:
            array.append(list(map(type,row.split(" "))))
    elif(" " in line):
        arr = line.split(" ")
        for element in arr:
            array.append(type(element))
    else:
        array = type(line)
    return array

##function that saves all data of one turn to specific file
def save_turn(file_name, chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr):
    with open("saves/" + file_name, "a") as txt_file:
        save_data_to_file(chess_board, txt_file)
        save_data_to_file(WK_position, txt_file)
        save_data_to_file(BK_position, txt_file)
        save_data_to_file(white_on_turn, txt_file)
        save_data_to_file(castling, txt_file)
        save_data_to_file(en_passant_arr, txt_file)

##function that loads all data of specific turn from specific file
def load_turn(file_name, turn_number):
    with open("saves/" + file_name, "r") as txt_file:
        for line_number, line in enumerate(txt_file):
            if(line_number == turn_number * 6):
                copy_chess_board = load_data_from_file(int, txt_file, line.replace("\n",""))
                copy_WK_position = load_data_from_file(int, txt_file)
                copy_BK_position = load_data_from_file(int, txt_file)
                copy_white_on_turn = load_data_from_file(is_bool, txt_file)
                copy_castling = load_data_from_file(is_bool, txt_file)
                copy_en_passant_arr = load_data_from_file(is_bool, txt_file)
                return copy_chess_board, copy_WK_position, copy_BK_position, copy_white_on_turn, copy_castling, copy_en_passant_arr
        

##function that coppies data of turns from one file to new one
def copy_save(original_file_name, turns):
    with open("saves/" + original_file_name, "r") as original_file:
        copy_file = open("saves/temp_copy.txt", "w")
        for line_number, line in enumerate(original_file):
            if(line_number == (turns + 1) * 6):
                break
            copy_file.write(line)
        copy_file.close()
    os.remove("saves/" + original_file_name)
    os.rename("saves/temp_copy.txt", "saves/" + original_file_name)

#chess_board = [[0, 0],[0, 0]]
#WK_position=[1,4]
#BK_position=[7,4]
#white_on_turn = False
#castling=[[True, False],[True,True]] 
#en_passant_arr=[[False for i in range(8)] for j in range(2)]

#for i in range(3):
#    save_turn("test.txt", chess_board, WK_position, BK_position, white_on_turn, castling, en_passant_arr)
#copy_save("test.txt", 0)



#with open("saves/text1.txt", "r") as txt_file:
#    test_chess_board = load_data_from_file(bool, txt_file)
#print(test_chess_board)
