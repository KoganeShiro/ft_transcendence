<template>
    <div class="template">
    <HeaderOrganism />
    <div class="container">
      <h2> {{ $t("waiting-players") }}... </h2>
      <Card class="card">
        <div class="players-grid">
          <TextField
          class="player-name"
            v-for="(player, index) in playerNames"
            :key="index"
            :placeholder="`${$t('player')} ${index + 1}`"
            v-model="playerNames[index]"
            :disabled="!isCreator"
          />
          <!--
           Text box component (that will be used in account)
           Show the player name in the text box
           Show in a blakc overlay "waiting for players" in the remaining text box
           Maybe show the player in a different color
           Maybe show the creator with a crown icon
           Maybe show the players icon inside the text box
            -->
        </div>
  
        <ButtonAtom
          v-if="isCreator"
          class="start-button"
          variant="42"
          fontSize="18px"
          @click="startTournament"
        >
          {{ $t("start-tournament") }}
        </ButtonAtom>
      </Card>
    </div>
    <FooterOrganism />
    </div>
  </template>
  
  <script>
  import { useRouter, useRoute } from "vue-router";
  import Card from "@/components/atoms/Card.vue";
  import TextField from "@/components/atoms/TextField.vue";
  import ButtonAtom from "@/components/atoms/Button.vue";
  import HeaderOrganism from "@/components/header/navbar.vue";
    import FooterOrganism from "@/components/footer.vue";
  
  export default {
    components: {
      Card,
      TextField,
      ButtonAtom,
        HeaderOrganism,
        FooterOrganism,
    },
    data() {
      return {
        playerNames: [],
        isCreator: false,
      };
    },
    setup() {
      const router = useRouter();
      const route = useRoute();
  
      return { router, route };
    },
    created() {
      this.isCreator = this.route.query.isCreator === "true";
      const count = Number(this.route.query.playerCount) || 4;
      this.playerNames = Array(count).fill("");
    },
    methods: {
      startTournament() {
        alert("Tournament Started!");
        // this.router.push("/matchmaking");
        //since it will be a single elimination tournament, if a player loose,
        //what will they do ?
      },
    },
  };
  </script>
  
  
  <style scoped>
  .container {
    margin-top: -50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    color: white;
  }
  
  .card {
    height: 150px;
    width: 550px;
    background: #333;
    border-radius: 10px;
  }
  
  .players-grid {
    margin-top: 10px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .start-button {
    margin-top: 65px;
    padding: 10px;
  }
  .player-name {
    width: 230px;
  }

  @media (max-width: 768px) {
    .card {
      width: 300px;
      height: 300px;
    }
    .players-grid {
      grid-template-columns: 1fr;
    }
    .player-name {
      width: 280px;
    }
    .start-button {
      margin-top: 75px;
    }
  }
  </style>
  