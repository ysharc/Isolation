"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    y, x = game.get_player_location(player)
    y2, x2 = game.get_player_location(game.get_opponent(player))

    #Move away from opponent as far as possible
    if len(game.get_blank_spaces()) > 30:
        return float((y2 - y)**2 + (x2 - x)**2) 
    else:
        #In the final stages maximize your winning chances
        return float(len(game.get_legal_moves(player)) -
                     len(game.get_legal_moves(game.get_opponent(player))))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    distance = float((h - y)**2 + (w - x)**2)

    #Fill up the center blocks first and then roam the area around it
    if len(game.get_blank_spaces()) > 20:
        return -distance
    else:
        return distance

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    y, x = game.get_player_location(player)
    y2, x2 = game.get_player_location(game.get_opponent(player))
    w, h = game.width / 2., game.height / 2.

    #The maximum manhattan distance between player and player if 14 and 
    #player and center is 6 
    return (float(abs(y-y2) + abs(x-x2))/14.0) + (float(abs(y-h) + abs(x-w))/6.0)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #For each of the legal moves, calculate the value and choose the max move
        #If no legal moves are available return the default (-1, -1)
        return max(game.get_legal_moves(),
                   key=lambda move: self.helper_minimax(game.forecast_move(move), depth - 1, False),
                   default=(-1, -1))

    def helper_minimax(self, game, depth, max_player=True):
        """
        Performs depth limited minimax search
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        max_player : boolean
            Specifies if the current player is trying to maximize or not

        Returns
        -------
        float
            The best value of the game nodes found in the current search

        Notes
        -----
            i) Modified version of AIMA pseduocode for minimax
               https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves(game.active_player)
        if depth <= 0 or not legal_moves:
            player = game.active_player if max_player else game.inactive_player
            #When the game is passed to the minimax function, we're playing as
            #the active and maximizing player.
            return self.score(game, player)
        if max_player:
            # Equivalent to max_value function in AIMA book
            best_value = float("-inf")
            for move in legal_moves:
                value = self.helper_minimax(game.forecast_move(move), depth - 1, False)
                best_value = max(value, best_value)
            return best_value
        else:
            # Equivalent to min_value function in AIMA book
            best_value = float("inf")
            for move in legal_moves:
                value = self.helper_minimax(game.forecast_move(move), depth - 1, True)
                best_value = min(value, best_value)
            return best_value

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        #Iterative Deepening
        for depth in range(1000):
            try:
                move = self.alphabeta(game, depth)  #Depth Limited Search
                #Any move other than (-1, -1) is better, Do not forfeit even if you know you're losing
                if move != (-1, -1):
                    best_move = move
            except SearchTimeout:
                return best_move
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        try:
            #AlphaBeta pruning performed in helper_alphabeta
            return self.helper_alphabeta(game, alpha, beta, depth, True)[0]
        except SearchTimeout:
            return (-1, -1)

    def helper_alphabeta(self, game, alpha, beta, depth, max_player=True):
        """
        Depth limited alpha-beta pruning search.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        max_player : boolean
            Specifies if the current player is trying to maximize or not

        Returns
        -------
        ((int, int), float)
            The move with the best value and it's corresponding value

        Notes
        -----
            i) Modified version of the AIMA pseudocode for alpha beta pruning
               https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
        if depth <= 0 or not legal_moves:
            #When the game is passed to the alphabeta function, we're playing as
            #the active and maximizing player.
            if max_player:
                return (-1, -1), self.score(game, game.active_player)
            else:
                return (-1, -1), self.score(game, game.inactive_player)

        best_move = legal_moves[0]

        if max_player:
            #Equivalent to max_value in AIMA pseudocode
            max_value = float("-inf")
            for move in legal_moves:
                value = self.helper_alphabeta(game.forecast_move(move),
                                              alpha, beta, depth - 1, False)[1]
                max_value = max(value, max_value)
                if value >= beta:
                    #Need not search any further because the min player won't
                    #allow us to reach this node
                    best_move = move
                    break
                if max_value > alpha:   # A new best move is found and alpha is updated
                    best_move = move
                    alpha = max_value

            return best_move, max_value

        else:
            #Equivalent to max_value in AIMA pseduocode
            min_value = float("inf")
            for move in legal_moves:
                value = self.helper_alphabeta(game.forecast_move(move),
                                              alpha, beta, depth - 1, True)[1]
                min_value = min(value, min_value)
                if value <= alpha:
                    #Need not search any further because the max player won't
                    #allow us to reach this node
                    best_move = move
                    break
                if min_value < beta:    # A new best move is found and beta is updated
                    best_move = move
                    beta = min_value

            return best_move, min_value
