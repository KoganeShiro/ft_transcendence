/**
 * Returns a move for the AI.
 * @param {Array} board - A 3x3 array representing the game board.
 * @param {Object} moves - The object containing arrays of moves for each player.
 * @param {String} currentPlayer - The current player (should be "O" in solo mode).
 * @returns {Object|null} An object with { row, col } for the move, or null if no moves are available.
 */
export function getAIMove(board, moves, currentPlayer) {
    const opponent = currentPlayer === "O" ? "X" : "O";
    const availableMoves = [];
    for (let row = 0; row < board.length; row++) {
      for (let col = 0; col < board[row].length; col++) {
        if (board[row][col] === null) {
          availableMoves.push({ row, col });
        }
      }
    }
    
    if (availableMoves.length === 0) return null;

    const isWinningMove = (board, player, row, col) => {
      board[row][col] = player;
      const win = (
        // Check row
        (board[row][0] === player && board[row][1] === player && board[row][2] === player) ||
        // Check column
        (board[0][col] === player && board[1][col] === player && board[2][col] === player) ||
        // Check diagonals
        (row === col && board[0][0] === player && board[1][1] === player && board[2][2] === player) ||
        (row + col === 2 && board[0][2] === player && board[1][1] === player && board[2][0] === player)
      );
      board[row][col] = null;
      return win;
    };

    // Check if the opponent can win in the next move, and block them
    for (const move of availableMoves) {
      if (isWinningMove(board, opponent, move.row, move.col)) {
        return move;
      }
    }

    // Check if AI can win in the next move
    for (const move of availableMoves) {
      if (isWinningMove(board, currentPlayer, move.row, move.col)) {
        return move;
      }
    }

    // If no winning move, choose a random available move
    const randomIndex = Math.floor(Math.random() * availableMoves.length);
    return availableMoves[randomIndex];
}