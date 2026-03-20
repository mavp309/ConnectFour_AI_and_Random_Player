import numpy as np
import math
import time
#import copy
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        if(player_number==1):
            self.opponent_number=2
        else:
            self.opponent_number=1
    def get_valid_moves(self,board):
        v_moves=[]
        for c in range(0,7):
            for r in range (5,-1,-1):
                if board[r,c]==0:
                    v_moves.append([r,c]);
                    break;
        #print(v_moves)
        return v_moves
    def try_move(self,move,board,player_number):
       #newboard= board.copy()
       #print(newboard)
       #print(move)
       #print(type(newboard))
       #print(type(board))
       board[move[0],move[1]]=player_number
       
       return board
    def undo(self,move,board):
        board[move[0],move[1]]=0
    
    def game_completed(self,board,player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int8)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int8))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))
	
    def is_term(self,board):
        if self.game_completed(board,self.player_number) or self.game_completed(board,self.opponent_number) or not any(0 in board[:, col] for col in range(board.shape[1])):
            return True
        return False

    def alpha_beta(self,board,alpha,beta,depth,player,start_time,limit):
        if time.time() -start_time> limit:
            return 0
        if (depth==0 or self.is_term(board)):
            if self.is_term(board):
                if self.game_completed(board,self.player_number):
                    return 100000000
                elif self.game_completed(board,self.opponent_number):
                    return -100000000
                else:
                    return 0
            else:
               return self.evaluation_function(board)
        moves=self.get_valid_moves(board)
        if player==self.player_number:
            v= -math.inf
            #if moves!=None:
            for m in moves:
                self.try_move(m,board,self.player_number)
                v=max(v,self.alpha_beta(board,alpha,beta,depth-1,self.opponent_number,start_time,limit))
                self.undo(m,board)
                if v>=beta:
                    return v
                alpha=max(alpha,v)
            return v
        else:
            v=math.inf
            for m in moves:
                self.try_move(m,board,self.opponent_number)
                v=min(v,self.alpha_beta(board,alpha,beta,depth-1,self.player_number,start_time,limit))
                self.undo(m,board)
                if v<=alpha:
                    return v
                beta=min(beta,v)
            return v
            
    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        start_time=time.time()
        limit=0.07
        best_move=None
        depth=1
        moves=self.get_valid_moves(board)
        if moves:
            best_move=moves[0]
        while(True):
            if time.time() - start_time>limit:
                break
            best_score=-math.inf
            alpha=-math.inf
            beta=math.inf
            c_best_move=None
            for m in moves:
                self.try_move(m,board,self.player_number)
                score=self.alpha_beta(board,alpha,beta,depth-1,self.opponent_number,start_time,limit)
                self.undo(m,board)
                if score> best_score:
                    best_score=score
                    c_best_move=m
                alpha=max(alpha,best_score)
                
            if (best_move==None and moves):
                best_move=moves[0]
                if time.time() - start_time>limit:
                    break
            if time.time()-start_time<=limit and c_best_move!=None:
                best_move=c_best_move
            
            depth+=1
             #if depth==5:
             #   break
        print(depth)
        return best_move[1]
        #raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        start_time=time.time()
        limit=4.8
        best_move=None
        depth=1
        moves=self.get_valid_moves(board)
        if moves:
            best_move=moves[0]
        while(True):
            if time.time() - start_time>limit:
                break
            best_score=-math.inf
            alpha=-math.inf
           
            c_best_move=None
            for m in moves:
                self.try_move(m,board,self.player_number)
                score=self.maxa(board,alpha,depth-1,self.opponent_number,start_time,limit)
                self.undo(m,board)
                if score> best_score:
                    best_score=score
                    c_best_move=m
                alpha=max(alpha,best_score)
                
            if (best_move==None and moves):
                best_move=moves[0]
                if time.time() - start_time>limit:
                    break
            if time.time()-start_time<=limit and c_best_move!=None:
                best_move=c_best_move
            
            depth+=1
             #if depth==5:
             #   break
        print(depth)
        return best_move[1]
        
        #raise NotImplementedError('Whoops I don\'t know what to do')
    def maxa(self,board,val,depth,player,start_time,limit):
        if time.time() -start_time> limit:
            return 0
        if (depth==0 or self.is_term(board)):
            if self.is_term(board):
                if self.game_completed(board,self.player_number):
                    return 100000000
                elif self.game_completed(board,self.opponent_number):
                    return -100000000
                else:
                    return 0
            else:
               return self.evaluation_function(board)
        moves=self.get_valid_moves(board)
        if player==self.player_number:
            v= -math.inf
            #if moves!=None:
            for m in moves:
                self.try_move(m,board,self.player_number)
                v=max(v,self.maxa(board,val,depth-1,self.opponent_number,start_time,limit))
                self.undo(m,board)
                v=max(val,v)
            return v
        else:
            v=0
            for m in moves:
                self.try_move(m,board,self.opponent_number)
                v+=self.maxa(board,val,depth-1,self.player_number,start_time,limit)
                self.undo(m,board)
            v=v/len(moves)
            return v



    def extract_blocks(self,board):
        blocks=[]
        for r in range(6):
            for c in range(4):
                b=[board[r,c],board[r,c+1],board[r,c+2],board[r,c+3]]
                blocks.append(b)
        for c in range(7):
            for r in range(3):
                b=[board[r,c],board[r+1,c],board[r+2,c],board[r+3,c]]
                blocks.append(b)
        for r in range(3):
            for c in range(4):
                b=[board[r,c],board[r+1,c+1],board[r+2,c+2],board[r+3,c+3]]
                blocks.append(b)
        for r in range(3,6):
            for c in range(4):
                b=[board[r,c],board[r-1,c+1],board[r-2,c+2],board[r-3,c+3]]
                blocks.append(b)
        return blocks

    def score_block(self,block): 
        score=0
        ai=block.count(self.player_number)
        opp=block.count(self.opponent_number)
        empty=block.count(0)
        if(ai==4):
            score+=10000
        elif(ai==3):
            score+=500
        elif(ai==2):
            score+=250
        elif(ai==1):
            score+=250
        if opp==4 :
            score-=10000
        elif opp==3:
            score-=100
            if empty==1:
                score-=1000
        elif opp==2:
            if empty==1:
                score-=200
            if empty==2:
                score-=250
            else :
                score-=50

        return score

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        score=0
        all_blocks=self.extract_blocks(board)
        for b in all_blocks:
            score+=self.score_block(b)
        return score

 
class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

