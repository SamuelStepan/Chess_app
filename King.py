from Piece import Piece 
class King(Piece):
    def Options(self,row,column,chess_board,white,castling):            ##function that will return 2D array representing possible options where to move king
        opt_table=[[0 for i in range(8)] for j in range(8)]     ##creating table for possible options to move king, 0 for not possible, 1 for possible, 2 for taking enemy piece, 3 for castling
        
        def HelpFct(vert,horiz):                                ##help function to find out if it is possible to move king to specific coordinates
            id=chess_board[row+vert][column+horiz]
            if id==0:
                return 1
            elif white:
                if id>6:
                    return 2
            else:
                if id<7:
                    return 2
            return 0

        
        all_dir=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]       ##array that has 8 elements,each represents one direction
        for i in range(8):
            dir=all_dir[i]      ##variable representing one direction                                      
            if(super().ConditionFct(row,column,dir[0],dir[1])):                ##checking out if the movement in specific direction is inside of chess board
                opt_table[row+dir[0]][column+dir[1]]=HelpFct(dir[0],dir[1])            ##calling help function for each direction(if possible) and saving result to 2D array opt_table
        
        if(white):
            base_row=0
            index=0
        else:
            base_row=7
            index=1
        if(castling[index][0] or castling[index][1]):
            empty=[True,True]
            for i in range(1,6):
                if(i!=4):
                    if(i<4 and chess_board[base_row][i]!=0):
                        empty[0]=False
                    elif(i>4 and chess_board[base_row][i]!=0):
                        empty[1]=False
            if(castling[index][0] and empty[0]):
                opt_table[base_row][2]=3
            if(castling[index][1] and empty[1]):
                opt_table[base_row][6]=3
        return opt_table    ##returns results of computing
        
        




