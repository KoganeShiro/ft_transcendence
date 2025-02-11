<template>
  <div class="modal-overlay" @click.self="closePopup">
    <div class="modal">
      <h1>{{ $t("loss") }}</h1>
      <!-- Loser's avatar and name -->
      <AvatarAtom 
        :pseudo="loserName" 
        :imageUrl="loserImage" 
        :showPseudo="true" 
        pseudoPosition="bottom" 
      />
      <router-link class="return-link" to="/game-choice">{{ $t("go-back") }}</router-link>
    </div>
  </div>
</template>

<script>
import AvatarAtom from "@/components/atoms/Avatar.vue";

export default {
  name: "LoserPopup",
  components: {
    AvatarAtom,
  },
  props: {
    loserName: {
      type: String,
      required: true,
    },
    loserImage: {
      type: String,
      required: true,
    },
  },
  methods: {
    closePopup() {
      this.$router.push("/game-choice");
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal {
  background: var(--card-color);
  padding: 20px;
  border-radius: 8px;
  position: relative;
  text-align: center;
  width: 90%;
  max-width: 400px;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
}

.return-link {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
}

.return-link:hover {
  opacity: 0.9;
}
</style>