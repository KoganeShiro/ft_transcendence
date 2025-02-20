<template>
  <div class="tic-tac-toe-game">
    <div class="board">
      <div class="row" v-for="(row, rowIndex) in board" :key="'row-' + rowIndex">
        <div
          class="cell"
          v-for="(cell, colIndex) in row"
          :key="'cell-' + rowIndex + '-' + colIndex"
          @click="handleCellClick(rowIndex, colIndex)"
          :class="{ twinkle: twinkleMove && twinkleMove.row === rowIndex && twinkleMove.col === colIndex }"
        >
          <template v-if="cell === 'X'">
            <img v-if="useImages && xImage" :src="xImage" alt="X" class="symbol" />
            <span v-else class="text-symbol x-symbol">X</span>
          </template>
          <template v-else-if="cell === 'O'">
            <img v-if="useImages && oImage" :src="oImage" alt="O" class="symbol" />
            <span v-else class="text-symbol o-symbol">O</span>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed } from "vue";
import defaultXImage from "@/assets/x.svg";
import defaultOImage from "@/assets/o.svg";
// Import the AI module which provides the getAIMove function.
import { getAIMove } from "@/components/game/TttAI.js";
import { getProfile, getAI, postGameResult, patchGameStats } from "@/components/game/ttt_api_call.js";
// console.log("getProfile", getProfile);

export default {
  name: "TicTacToeGame",
  props: {
    mode: {
      type: String,
      default: "local", // "solo" means play against computer; otherwise guest (local) two-player mode.
    },
    useImages: { type: Boolean, default: true },
    xImage: { type: String, default: () => defaultXImage },
    oImage: { type: String, default: () => defaultOImage },
  },

  /*
  * Need to know how many moves each players has made.
  * Need to know who win
  */

  setup(props, { emit }) {
    // Game state
    const state = reactive({
      board: [
        [null, null, null],
        [null, null, null],
        [null, null, null],
      ],
      // Record moves for each player (max. 3)
      moves: { X: [], O: [] },
      currentPlayer: "X",
      gameOver: false,
      message: "",
      myMoves: 0,
      AIMoves: 0,
      winner: '',
    });

    // Computed property to show a "twinkle" effect when 3 moves exist.
    const twinkleMove = computed(() => {
      return state.moves[state.currentPlayer].length === 3
        ? state.moves[state.currentPlayer][0]
        : null;
    });

    /**
     * Modified click handler with an extra optional parameter.
     * @param {number} row - Row index.
     * @param {number} col - Column index.
     * @param {boolean} [isAI=false] - Indicates if the move is initiated by the AI.
     */
    function handleCellClick(row, col, isAI = false) {
      // Do nothing if game is over or the cell is not empty.
      if (state.gameOver || state.board[row][col] !== null) return;

      // In solo mode, block human clicks if it's the AI's turn.
      if (props.mode === "solo" && state.currentPlayer === "O" && !isAI) return;

      // Remove the oldest move if already 3 moves exist.
      if (state.moves[state.currentPlayer].length === 3) {
        const oldMove = state.moves[state.currentPlayer].shift();
        state.board[oldMove.row][oldMove.col] = null;
      }

      // Place the new move.
      state.board[row][col] = state.currentPlayer;
      state.moves[state.currentPlayer].push({ row, col });

      if (state.currentPlayer === "X") {
        state.myMoves++;
      } else {
        state.AIMoves++;
      }

      // Check for a winner.
      if (checkWinner()) return;

      // Switch player.
      state.currentPlayer = state.currentPlayer === "X" ? "O" : "X";

      // In solo mode, if it's now the AI's turn, schedule the AI move.
      if (props.mode === "solo" && state.currentPlayer === "O" && !state.gameOver) {
        // This log explains why the AI is making its move:
        // console.log("AI move triggered because it's now AI's turn in solo mode.");
        setTimeout(() => {
          const aiMove = getAIMove(state.board, state.moves, state.currentPlayer);
          if (aiMove) {
            // Pass true for the isAI flag so that this move isn’t blocked.
            handleCellClick(aiMove.row, aiMove.col, true);
          }
        }, 500);
      }
    }

    async function calling_api(a) {
      try {
        const userProfile = await getProfile();
        const aiProfile = await getAI();

        // console.log("User profile: ", userProfile.id);
        // console.log("AI profile: ", aiProfile.id);

        // Overwrite the winner with the respective profile id based on the winning symbol.
        if (state.board[a.row][a.col] === "X") {
          state.winner = userProfile.id;
        } else {
          state.winner = aiProfile.id;
        }

        // console.log("Winner: ", state.winner);
        // console.log("AI moves: ", state.AIMoves);
        // console.log("Player moves: ", state.myMoves);

        // Post the game result
        await postGameResult(userProfile.id, aiProfile.id, state.winner, state.myMoves, state.AIMoves);

        let moves_nb;
        if (state.myMoves <= 5) {
          moves_nb = 5;
        } else if (state.myMoves <= 10) {
          moves_nb = 10;
        } else {
          moves_nb = 15;
        }
        // console.log("moves_nb: ", moves_nb);

        // Patch game statistics based on the winner
        if (state.winner === userProfile.id) {
          await patchGameStats(1, `win_${moves_nb}`);
        } else {
          await patchGameStats(0, `loss_${moves_nb}`);
        }
      } catch (error) {
        console.error("Error handling game result:", error);
      }
    }

    // Function to check for a winning pattern.
    function checkWinner() {
      const winPatterns = [
        // Rows
        [{ row: 0, col: 0 }, { row: 0, col: 1 }, { row: 0, col: 2 }],
        [{ row: 1, col: 0 }, { row: 1, col: 1 }, { row: 1, col: 2 }],
        [{ row: 2, col: 0 }, { row: 2, col: 1 }, { row: 2, col: 2 }],
        // Columns
        [{ row: 0, col: 0 }, { row: 1, col: 0 }, { row: 2, col: 0 }],
        [{ row: 0, col: 1 }, { row: 1, col: 1 }, { row: 2, col: 1 }],
        [{ row: 0, col: 2 }, { row: 1, col: 2 }, { row: 2, col: 2 }],
        // Diagonals
        [{ row: 0, col: 0 }, { row: 1, col: 1 }, { row: 2, col: 2 }],
        [{ row: 0, col: 2 }, { row: 1, col: 1 }, { row: 2, col: 0 }],
      ];

      for (const pattern of winPatterns) {
        const [a, b, c] = pattern;
        if (
          state.board[a.row][a.col] &&
          state.board[a.row][a.col] === state.board[b.row][b.col] &&
          state.board[a.row][a.col] === state.board[c.row][c.col]
        ) {
          state.gameOver = true;
          state.message = `${state.board[a.row][a.col]} Wins!`;

          if (props.mode === "solo") {
            calling_api(a);
          }

          emit('game-ended', state.board[a.row][a.col]);
          return true;
        }
      }
      return false;
    }

    return {
      board: state.board,
      message: state.message,
      gameOver: state.gameOver,
      handleCellClick,
      twinkleMove,
      useImages: props.useImages,
      xImage: props.xImage,
      oImage: props.oImage,
      myMoves: state.myMoves,
      AIMoves: state.AIMoves,
      winner: state.winner,
    };
  },
};
</script>

<style scoped>
.tic-tac-toe-game {
  margin-bottom: 100px;
  padding: 20px;
  max-width: 500px;
  /* background: #333; */
  background: var(--game-background-color);
  border-radius: 8px;
  color: var(--text-color);
}

.board {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.row {
  display: flex;
}

.cell {
  width: 100px;
  height: 100px;
  margin: 2px;
  border-radius: 3px;
  background: var(--cell-color);
  border: 2px solid #555;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.cell:hover {
  background: var(--cell-hover-color);
  transform: scale(1.03);
}

.symbol {
  max-width: 100%;
  max-height: 100%;
}

.text-symbol {
  font-size: 3rem;
  font-weight: bold;
  user-select: none;
}

.x-symbol {
  color: #e74c3c;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
}

.o-symbol {
  color: #3498db;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
}

/* Twinkle effect */
.twinkle {
  animation: twinkleEffect 0.5s alternate infinite;
}

@keyframes twinkleEffect {
  0% { opacity: 1; }
  100% { opacity: 0.3; }
}
</style>