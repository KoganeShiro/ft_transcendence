<template>
  <teleport to="body">
    <div v-if="showPopup" class="invitation-overlay">
      <div class="invitation-popup">
        <h3>Match Invitation</h3>
        <p>{{ inviterName }} has challenged you to a match!</p>
        <div class="button-group">
          <button @click="accept" class="accept-btn">Accept</button>
          <button @click="decline" class="decline-btn">Decline</button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const store = useStore();
    const router = useRouter();

    const isInGame = computed(() => store.state.game.isInGame);
    const invitationShown = computed(() => store.state.invitations?.showInvitation ?? false);

    const showPopup = computed(() => invitationShown.value && !isInGame.value);

    const inviterName = computed(() => store.state.invitations?.invitationData?.inviterName ?? 'Unknown Player');
    const matchId = computed(() => store.state.invitations?.invitationData?.matchId ?? null);

    const accept = () => {
      if (matchId.value) {
        store.dispatch('invitations/hideInvitation');
        router.push(`/match/${matchId.value}`);
      }
    };

    const decline = () => {
      store.dispatch('invitations/hideInvitation');
    };

    return { showPopup, inviterName, accept, decline };
  }
};
</script>


  <!-- <script>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const store = useStore();
    const router = useRouter();

    // Temporary override for testing
    const show = computed(() => true); // Force show popup
    const inviterName = computed(() => "Test Player");
    const matchId = computed(() => "test-match-123");

    const accept = () => {
      console.log("Accepted match:", matchId.value);
      router.push(`/match/${matchId.value}`);
    };

    const decline = () => {
      console.log("Declined match");
    };

    // Auto-show when component mounts
    onMounted(() => {
      console.log("Popup should be visible now");
    });

    return { show, inviterName, accept, decline };
  }
};
</script> -->

  
  <style scoped>
  .invitation-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    color: white;
  }
  
  .invitation-popup {
    background: rgba(77, 76, 76, 0.568);
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .button-group {
    margin-top: 1rem;
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
  
  .accept-btn, .decline-btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .accept-btn {
    background: #4CAF50;
    color: white;
    font-weight: bold;
  }
  
  .decline-btn {
    background: #f44336;
    color: white;
    font-weight: bold;
  }
  </style>
  