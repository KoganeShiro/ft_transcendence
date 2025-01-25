<template>
  <div class="register-page">
    <HeaderOrganism :showBurgerMenu="false" />

    <div class="register-content">
      <RegisterCard />
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import TextAtom from "@/components/atoms/Text.vue";
import RegisterCard from "@/components/sign/RegisterCard.vue";

export default {
  components: {
      HeaderOrganism,
      FooterOrganism,
      TextAtom,
      RegisterCard,
  },
};
</script>

<style scoped>
.register-page {
  text-align: center;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.register-content {
  margin: 0px auto;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
  width: 100%;
}

@media (max-width: 700px) {
  .register-content {
      max-width: 100%;
      margin: 0;
      line-height: 4;
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 1;
  }

  .register-content :deep(.register-card) {
      width: 100%;
      max-width: 300px;
      margin: 0 auto;
  }

  :deep(.register-card) {
      font-size: 0.9rem;
  }

  :deep(input),
  :deep(button) {
      margin: 5px 0;
  }
}

@media (max-width: 380px) {
  .register-content {
      line-height: 1.5;
  }

  :deep(.register-card) {
      font-size: 0.85rem;
  }
}
</style>