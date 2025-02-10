<template>
  <div class="confirm-quit-tournament">
    <Card class="confirm-card">
      <h3 class="confirm-title">{{ $t("quit-tournament-title", "Are you sure you want to quit the tournament?") }}</h3>
      <p class="confirm-message">
        {{ $t("quit-tournament-message", "If you quit now, you will lose your progress. Do you wish to continue?") }}
      </p>
      <div class="button-group">
        <Button variant="attention" @click="confirm">{{ $t("yes", "Yes") }}</Button>
        <Button variant="42" @click="cancel">{{ $t("no", "No") }}</Button>
      </div>
    </Card>
  </div>
</template>

<script>
import Card from "@/components/atoms/Card.vue";
import Button from "@/components/atoms/Button.vue";

export default {
  name: "ConfirmQuitTournament",
  components: {
    Card,
    Button,
  },
  methods: {
    confirm() {
      // Emit a "confirm" event to let the parent know the user wants to quit
      this.$emit("confirm");
    },
    cancel() {
      // Emit a "cancel" event to let the parent know the user canceled quitting
      this.$emit("cancel");
    },
  },
};
</script>

  
  <style scoped>
  .confirm-quit-tournament {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.95); /* semi-transparent backdrop */
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1100;
  }
  
  .confirm-card {
    padding: 20px;
    text-align: center;
    max-width: 400px;
    width: 90%;
  }
  
  .button-group {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    gap: 10px;
  }

  @media (max-width: 700px) {
    .card {
      height: 30%;
    }
  }
  </style>
  