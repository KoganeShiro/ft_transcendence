<template>
    <div>
      <h2>{{ $t("tournament-winner") }}</h2>
        <Avatar :showPseudo="false" />
        <p>{{ winner }}</p>
      <Button class="button" @click="goBack">{{ $t("go-back") }}</Button>
      <!-- <router-link class="return-link" to="/game-choice">{{ $t("go-back") }}</router-link> -->
    </div>
  </template>
  
  <script>
    import Button from "@/components/atoms/Button.vue";
    import Avatar from "@/components/atoms/Avatar.vue";

  export default {
    name: "TournamentWinner",
    components: {
      Button,
        Avatar,
    },
    props: ['winner'],
    methods: {
      goBack() {
        this.$emit('goBack');
      }
    }
  };
  </script>

    <style scoped>
    .button {
      margin-top: 30px;
      padding: 15px;
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