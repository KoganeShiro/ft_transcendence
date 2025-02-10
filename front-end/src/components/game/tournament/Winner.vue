<template>
    <div>
      <h2>{{ $t("tournament-winner") }}</h2>
        <Avatar :player="winner" />
      <Button class="button" @click="goBack">{{ $t("go-back") }}</Button>
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
    </style>