<template>
  <div class="winner-popup">
    <Card class="cards">
      <div class="content">
    <h1>{{ $t("winner") }}</h1>
    <Avatar :showPseudo="false" />
    <p>{{ winner.name }}</p>
    <button class="btn"  @click="dismissPopup">{{ $t("continue") }}</button>
  </div>
  </Card>
  </div>
</template>

<script>
import Button from "@/components/atoms/Button.vue";
import Card from "@/components/atoms/Card.vue";
import Avatar from "@/components/atoms/Avatar.vue";

export default {
  components: { Button, Card, Avatar },
  name: "WinnerPopup",
  props: {
    winner: {
      type: Object,
      required: true
    }
  },
  methods: {
    dismissPopup() {
      this.$emit("dismiss");
    }
  }
};
</script>

<style scoped>

.cards {
  padding: 20px;
  text-align: center;
  height: 500px;
  margin-left: 30px;
  margin-right: 30px;
}

.winner-popup {
  margin-top: 100px;
  justify-content: center;
  align-items: center;
}

.content {
  display: flex;
  margin-top: 100px;
  padding: 20px;
  flex-direction: column;
  text-align: center;
}

.btn {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 13px;
  color: var(--text-color);
  background-color: var(--burger-btn-color);
  border: none;
  border-radius: 10px;
  font-size: 1.3em;
  cursor: pointer;
  font-weight: bold;
}

.btn:hover {
  background-color: var(--burger-btn-hover-color);
  transition: all 0.3s ease;
  transform: scale(1.05);
}

p {
  font-size: 1.5em;
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  padding: 10px;
  text-align: center;
}

</style>