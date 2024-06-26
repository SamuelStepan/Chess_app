from Piece import Piece

class Knight(Piece):
    def Options(self,row,column,chess_board,white):            ##function that will return 2D array reprezenting possible options where to move knight
        opt_table=[[0 for i in range(8)] for j in range(8)]     ##creating table for possible options to move knight, 0 for not possible, 1 for possible, 2 for taking enemy piece
        
        def HelpFct(vert,horiz):                                ##help function to find out if it is possible to move knight to specific coordinates
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

        ##calling HelpFct for each direction(if possible) and saving it to 2D array opt_table
        help_var=[[1,2],[-1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,1],[-2,-1]]        ##array witch holds array with 2 parametres, each representing a specific move that can knight do[y,x]
        for i in range(8):      ##bishop has 4 possible directions to move
            move=help_var[i]     ##loading specific move
            if(super().ConditionFct(row,column,move[0],move[1])):         ##checking out if specific coordinates are in chess_board
                opt_table[row+move[0]][column+move[1]]=HelpFct(move[0],move[1])       ##calling help function for each direction(if possible) and saving result to 2D array opt_table
        
        return opt_table    ##returns results of computing


               


