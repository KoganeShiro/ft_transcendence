<template>
  <div class="pong-page">
    <!-- Listen for the custom event here -->
    <PongGame ref="pongGame" @hideMessageIcon="hideMessageIcon" />
    <!-- Clickable message icon -->
    <div v-if="showMessageIcon" class="message-icon" @click="togglePopup">💬</div>
    <!-- Friend Page Popup -->
    <Transition name="popup">
      <div v-if="showPopup" class="friend-popup">
        <div class="popup-content">
          <button class="close-btn" @click="togglePopup">x</button>
          <Friends />
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import PongGame from "@/components/game/pongGame/PongFriend.vue";
import Friends from "@/components/profile/Friends.vue";

export default {
  name: "PongWithFriend",
  components: { PongGame, Friends },
  data() {
    return {
      showPopup: false,
      showMessageIcon: true,
    };
  },
  methods: {
    togglePopup() {
      this.showPopup = !this.showPopup;
    },
    hideMessageIcon() {
      this.showMessageIcon = false;
    }
  },
};
</script>


<style scoped>
.pong-page {
  position: relative;
}

.message-icon {
  position: fixed;
  bottom: 65px;
  right: 65px;
  font-size: 39px;
  cursor: pointer;
  z-index: 10001;
}

.friend-popup {
  position: fixed;
  bottom: 60px;
  right: 20px;
  background: var(--text-box-color);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  z-index: 10001;
}

.popup-content {
  position: relative;
}

.close-btn {
  background: none;
  border: none;
  font-size: 25px;
  cursor: pointer;
  color: var(--icon-color, #333);
  font-weight: bold;
}

.popup-content button {
  position: absolute;
  top: 10px;
  right: 10px;
}

/* Animation styles */
.popup-enter-active,
.popup-leave-active {
  transition: all 0.3s ease;
}

.popup-enter-from,
.popup-leave-to {
  opacity: 0;
  transform: scale(0.5) translate(50%, 50%);
}

.popup-enter-to,
.popup-leave-from {
  opacity: 1;
  transform: scale(1) translate(0, 0);
}
</style>