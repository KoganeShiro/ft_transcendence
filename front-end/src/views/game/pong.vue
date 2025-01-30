<template>
  <HeaderOrganism />
  <div class="pong-page">
    <div :class="['mobile-hide', { 'hide-heading': mode === 'tournament' }]">
      <h1>Pong - {{ mode }} mode</h1>
    </div>
    <PongFront :mode="mode" />
  </div>
  <FooterOrganism />
</template>

<script>
import { useRoute } from "vue-router";
import { ref, computed } from "vue";
import PongFront from "@/components/game/PongFront.vue";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";

export default {
  components: {
    PongFront,
    HeaderOrganism,
    FooterOrganism,
  },
  setup() {
  const route = useRoute();
    
  let mode = computed(() => {
    console.log("Route params:", route.params);
    return route.params.mode;
  });
  return { mode };
},
};
</script>


<style scoped>
.pong-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 85.5vh;
  overflow: hidden;
}

@media screen and (max-width: 768px) {
  .mobile-hide {
    display: none;
  }
}

.hide-heading {
  display: none;
}

</style>
