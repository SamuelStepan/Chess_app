from Piece import Piece

class Pawn(Piece):
    def Options(self,row,column,chess_board,white,en_passant_arr):            ##function that will return 2D array reprezenting possible options where to move pawn
        opt_table=[[0 for i in range(8)] for j in range(8)]     ##creating table for possible options to move pawn, 0 for not possible, 1 for possible, 2 for taking enemy piece, 4 for moving to squares ahead, 5 for el passant

        if white:       ##based on pawns color, he can move up or down on chess_board
            dir=1
            index=1
        else:
            dir=-1
            index=0
        
        def HelpFct(vert):                  ##function that computes if before pawn on right or left(depends on vert) is piece and if he can take it
            id=chess_board[row+dir][column+vert]
            if(id==0):
                return 0
            elif(id>6 and white):
                return 2
            elif(id<7 and not white):
                return 2
            return 0

        if((white and row==1) or (not white and row==6)):     ##this signals that pawn had not yet moved, so he can move two squares before him
            if(chess_board[row+2*dir][column]==0):     ##if two squares before pawn in empty, he can move there
                opt_table[row+2*dir][column]=4

        if(super().ConditionFct(row,column,dir,0)):    ##checks if pawn can move ahead one squre
                if(chess_board[row+dir][column]==0):
                    opt_table[row+dir][column]=1
        
        if(super().ConditionFct(row,column,dir,1)):
            opt_table[row+dir][column+1]=HelpFct(1)
        if(super().ConditionFct(row,column,dir,-1)):
            opt_table[row+dir][column-1]=HelpFct(-1)
       
        if((white and row==4) or (not white and row==3)):     ##pawn is in position that he would be able to do en passant move
            for i in [-1,1]:
                if(super().ConditionFct(row,column,dir,i)):     
                    if(en_passant_arr[index][column+i]):        ##enemy pawn moved 2 squares ahead, pawn can do en passant move
                        opt_table[row+dir][column+i]=5

        return opt_table    ##returns results of computing


               





