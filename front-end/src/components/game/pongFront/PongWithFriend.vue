<template>
  <div class="pong-page">
    <!-- Parent only renders the game component -->
    <PongGame
      ref="pongGame"
    />
  </div>
</template>

<script>
import PongGame from "@/components/game/pongGame/PongFriend.vue";

export default {
  name: "PongWithFriend",
  components: { PongGame },
};
</script>

<style scoped>
.pong-page {
  color: #fff;
  position: relative;
}
</style>
