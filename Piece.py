class Piece(): 
    def ConditionFct(self,row,column,vert,horiz):                          ##function returning True if specific coordinates reprezented by starting point [y,x], distance in y axis(vert) and distance in x axis(horiz), are inside of chess board, returns False if not
        if(row+vert>-1 and row+vert<8 and column+horiz>-1 and column+horiz<8):
            return True
        else:
            return False
        
    def is_white(self,id):      ##function to return true if id of chess piece is white, false if it is black
        if id==0:
            pass
        elif id<7:
            return True
        else:
            return False


            
        

