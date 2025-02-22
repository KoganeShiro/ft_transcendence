<template>
  <div id="app" :class="selectedTheme">
    <TournamentBanner
      v-if="shouldShowBanner"
      :tournamentId="tournamentId"
      message="Tournament created! Join now:"
      :duration="10000"
    />
    <router-view />
    <InvitationPopup />
  </div>
</template>

<script>
import { ref, provide } from 'vue';
import { mapGetters } from 'vuex';
import InvitationPopup from '@/components/Invitation.vue';
import TournamentBanner from '@/components/NotifBanner.vue';

export default {
  name: 'App',
  components: {
    InvitationPopup,
    TournamentBanner,
  },
  setup() {
    const shouldShowBanner = ref(false);
    const tournamentId = ref('');

    const showTournamentBanner = (id) => {
      tournamentId.value = id;
      shouldShowBanner.value = true;
      setTimeout(() => {
        shouldShowBanner.value = false;
      }, 10000); // Hide banner after 10 seconds
    };

    provide('showTournamentBanner', showTournamentBanner);

    return {
      shouldShowBanner,
      tournamentId,
    };
  },
  computed: {
    ...mapGetters(['selectedTheme']),
  },
  watch: {
    selectedTheme(newTheme) {
      document.body.setAttribute('data-theme', newTheme);
    },
  },
  mounted() {
    document.body.setAttribute('data-theme', this.selectedTheme);
  },
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  min-height: 100vh;
}

.footer-link {
  color: #00aaff;
  text-decoration: none;
}

.template {
  text-align: center;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

#app.dark {
  color: #ffffff;
  background-color: #222;
}

#app.light {
  color: #2c3e50;
  background-color: #ffffff;
}

#app.ocean {
  color: #ffffff;
  background-color: #1e3a5f;
}

#app.forest {
  color: #ffffff;
  background-color: #064706;
}

#app.volcano {
  color: #ffffff;
  background-color: #880505;
}

#app.teapot {
  color: #ffffff;
  background-color: #370b5c;
}


/* Define CSS variables for each theme */
:root {
  --header-color: #3333;
  --background-color: #222;
  --text-color: #ffffff;
  --icon-color: #ffffff;
}

[data-theme="light"] {
  --header-color: #D9D9D9;
  --footer-color: #D9D9D9;
  --burger-btn-color: #d1d1d1ec;
  --burger-btn-hover-color: #a5a2a2ec;
  --background-color: #e7e7e7;
  --link-color: #3498db;
  --card-color: #9c9c9a71;
  --text-box-color: #adada8c5;
  --pseudo-sidebar-color: #cecece;
  --pseudo-sidebar-hoover-color: #b4b4ab;
  --sidebar-color: #d3d3d3;
  --sidebar-hoover-color: #e4e3db;
  --side-btn-color: #edeecc;
  --text-color: #000000;
  --icon-color: #000000;
  --attention-btn: #bb1111;
  --back: #630606;
  --game-background-color: #ccc5c5;
  --cell-color: #bdb7b7;
  --cell-hover-color: #4b4a4a;
  --overlay-color: #acacacb4;

  --chat-header-bg: #778592;
  --chat-messages-bg: #e4e4ddf8;
  --msg-send: #bac7d8;
  --msg-receive: #9bdee9;
}

[data-theme="dark"] {
  --header-color: #3a3737;
  --footer-color: #302d2d;
  --burger-btn-color: #313131ec;
  --burger-btn-hover-color: #252424;
  --background-color: #222;
  --link-color: #3498db;
  --card-color: #3b3b3b71;
  --text-box-color: #333;
  --pseudo-sidebar-color: #333;
  --pseudo-sidebar-hoover-color: #5f5f5f;
  --sidebar-color: #333;
  --sidebar-hoover-color: #505050;
  --side-btn-color: #333;
  --text-color: #ffffff;
  --icon-color: #ffffff;
  --attention-btn: #bb1111;
  --back: #630606;
  --game-background-color: #1d1b1b;
  --cell-color: #444;
  --cell-hover-color: #4b4a4a;
  --overlay-color: #202020b4;

  --chat-header-bg: #202020;
  --chat-messages-bg: #3b3b3b71;
  --msg-send: #08203f;
  --msg-receive: #134b53;
}

[data-theme="ocean"] {
  --header-color: #162d44;
  --footer-color: #162d44;
  --burger-btn-color: #122335;
  --burger-btn-hover-color: #05192e;
  --background-color: #1e3a5fe0;
  --link-color: #53ceffe1;
  --card-color: #64646471;
  --text-box-color: #19344e;
  --pseudo-sidebar-color: #285a8b;
  --pseudo-sidebar-hoover-color: #2279d1;
  --sidebar-color: #112b44b4;
  --sidebar-hoover-color: #061b30;
  --side-btn-color: #1d4368;
  --text-color: #ffffff;
  --icon-color: #ffffff;
  --attention-btn: #bb1111;
  --back: #801414;
  --game-background-color: #162d44;
  --cell-color: #162d44;
  --cell-hover-color: #162d44;
  --overlay-color: #162d44;

  --chat-header-bg: #162d44;
  --chat-messages-bg: #0c203af8;
  --msg-send: #0c2e5a;
  --msg-receive: #16555e;

}

[data-theme="forest"] {
  --header-color: #003303;
  --footer-color: #003303;
  --burger-btn-color: #01580dbe;
  --burger-btn-hover-color: #006e05;
  --background-color: #064706;
  --link-color: #ff9900e1;
  --card-color: #64646471;
  --text-box-color: #1f6326c4;
  --pseudo-sidebar-color: #007c25;
  --pseudo-sidebar-hoover-color: #01571b;
  --sidebar-color: #0d361be7;
  --sidebar-hoover-color: rgb(25, 126, 12);
  --side-btn-color: #00932C;
  --text-color: #ffffff;
  --icon-color: #ffffff;
  --attention-btn: #bb1111;
  --back: #802401;
  --game-background-color: #117011bb;
  --cell-color: #267226;
  --cell-hover-color: #0a770a;
  --overlay-color: #123815c4;

  --chat-header-bg: #1e491b;
  --chat-messages-bg: #3b3b3b71;
  --msg-send: #0b632d;
  --msg-receive: #58b44c;
}

[data-theme="volcano"] {
  --header-color: #680505;
  --footer-color: #4d0404;
  --burger-btn-color: #7e0606e3;
  --burger-btn-hover-color: #6b0505;
  --background-color: #880505;
  --link-color: #28c2ff;
  --card-color: #64484871;
  --text-box-color: #4d0404;
  --pseudo-sidebar-color: #521111;
  --pseudo-sidebar-hoover-color: #8f3131;
  --sidebar-color: #5f0606;
  --sidebar-hoover-color: #4d0404;
  --side-btn-color: #661111;
  --text-color: #ffffff;
  --icon-color: #ffffff;
  --attention-btn: #bb1111;
  --back: #802401;
  --game-background-color: #5f0606;
  --cell-color: #420101ea;
  --cell-hover-color: #7c2020;
  --overlay-color: #5e1a1a;

  --chat-header-bg: #491b1b;
  --chat-messages-bg: #4d363671;
  --msg-send: #630b0b;
  --msg-receive: #b44c4c;
}

[data-theme="teapot"] {
  --header-color: #210b5c;
  --footer-color: #530b5c;
  --burger-btn-color: #170b5c;
  --burger-btn-hover-color: #0b1e5c;
  --background-color: #370b5c;
  --link-color: #00bef8;
  --card-color: #64484871;
  --text-box-color: #410569;
  --pseudo-sidebar-color: #113552;
  --pseudo-sidebar-hoover-color: #318f70;
  --sidebar-color: #06165f;
  --sidebar-hoover-color: #47044d;
  --side-btn-color: #11664d;
  --text-color: #ffffff;
  --icon-color: #ffffff;
  --attention-btn: #bb1111;
  --back: #01802b;
  --game-background-color: #06135f;
  --cell-color: #014042ea;
  --cell-hover-color: #012a42ea;
  --overlay-color: #2c0347;

  --chat-header-bg: #2d1b49;
  --chat-messages-bg: #362b3a71;
  --msg-send: #1b0b63;
  --msg-receive: #ab4cb4;
}

body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>