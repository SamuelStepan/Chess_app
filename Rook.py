from Piece import Piece

class Rook(Piece):
    def Options(self,row,column,chess_board,white):            ##function that will return 2D array reprezenting possible options where to move rook
        opt_table=[[0 for i in range(8)] for j in range(8)]     ##creating table for possible options to move rook, 0 for not possible, 1 for possible, 2 for taking enemy piece
        
        def HelpFct(vert,horiz):                                ##help function to find out if it is possible to move rook to specific coordinates
            id=chess_board[row+vert][column+horiz]
            if id==0:
                return 1,True
            elif white:
                if id>6:
                    return 2,False
            else:
                if id<7:
                    return 2,False
            return 0,False

        ##calling HelpFct for each direction(if possible) and saving it to 2D array opt_table
        help_var=[[0,1],[0,-1],[1,0],[-1,0]]        ##array witch holds array with 2 parametres, each representing a specific direction[y,x]
        for i in range(4):      ##rook has 4 possible directions to move
            j=1                 ##j will represent number of squares to move in specific direction
            dir=help_var[i]     ##loading specific direction
            not_end=True        ##bool variable representing if in specific direction does not stand some piece
            while(super().ConditionFct(row,column,dir[0]*j,dir[1]*j) and not_end):         ##checking out if specific coordinates(given by direction and number of moves) are in chess_board and if some piece does not stand in the way
                opt_table[row+dir[0]*j][column+dir[1]*j], not_end=HelpFct(dir[0]*j,dir[1]*j)       ##calling help function for specific coordinates and saving first part of result to 2D array opt_table, second part to variable not_end      
                j+=1    ##incrementing j by one
        
        ##finish castling fucntion

        return opt_table    ##returns results of computing


               


