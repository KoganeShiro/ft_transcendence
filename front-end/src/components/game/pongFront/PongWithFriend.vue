<template>
  <div class="pong-page">
    <PongGame ref="pongGame" @gameEnded="handleGameEnded" />
  </div>
  <!-- incorporate the friend component -->
</template>

<script>
import PongGame from "@/components/game/pongGame/PongFriend.vue";

export default {
  name: "PongWithFriend",
  components: { PongGame},

  method:
  {
    async handleGameEnded(winner) {
      if (this.requestSent) return;
      this.requestSent = true;
      try {
        const response = await API.get('/api/profile/');
        const { username, cover_photo } = response.data;
        console.log("handleGameEnded: winner =", winner);
        if (winner === "Player 1") {
          this.winnerName = username;
          this.winnerImage = cover_photo;
          this.showWinner = true;
        } else {
          this.loserName = username;
          this.loserImage = cover_photo;
          this.showLoser = true;
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },

  },
};
</script>

<style scoped>
.pong-page {
  color: #fff;
  position: relative;
}
</style>
