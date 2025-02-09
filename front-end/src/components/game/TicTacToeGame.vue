<template>
  <div class="tic-tac-toe-game">
    <div class="board">
      <!-- use touch handler event -->
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
    <div v-if="gameOver" class="message">
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script>
import { reactive, ref, computed } from "vue";
import defaultXImage from "@/assets/x.svg";
import defaultOImage from "@/assets/o.svg";

export default {
  name: "TicTacToeGame",
  props: {
    useImages: { type: Boolean, default: true },
    xImage: { type: String, default: () => defaultXImage },
    oImage: { type: String, default: () => defaultOImage },
  },
  setup(props) {
    const state = reactive({
      board: [
        [null, null, null],
        [null, null, null],
        [null, null, null],
      ],
      moves: { X: [], O: [] },
      currentPlayer: "X",
      gameOver: false,
      message: "",
    });

    // Computed property: Twinkle the first move if there are 3 moves already
    const twinkleMove = computed(() => {
      return state.moves[state.currentPlayer].length === 3
        ? state.moves[state.currentPlayer][0]
        : null;
    });


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
          state.message = `${state.currentPlayer} Wins!`;
          return true;
        }
      }
      return false;
    }

    function handleCellClick(row, col) {
      if (state.gameOver || state.board[row][col] !== null) return;

      // Remove the oldest move if already 3 moves exist
      if (state.moves[state.currentPlayer].length === 3) {
        const oldMove = state.moves[state.currentPlayer].shift(); 
        state.board[oldMove.row][oldMove.col] = null;
      }

      // Place the new move
      state.board[row][col] = state.currentPlayer;
      state.moves[state.currentPlayer].push({ row, col });

      // Check for winner
      if (checkWinner()) return;

      state.currentPlayer = state.currentPlayer === "X" ? "O" : "X";
    }


    return {
      board: state.board,
      message: state.message,
      handleCellClick,
      twinkleMove,
      useImages: props.useImages,
      xImage: props.xImage,
      oImage: props.oImage,
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
