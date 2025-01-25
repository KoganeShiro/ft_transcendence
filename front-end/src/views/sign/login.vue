<template>
  <div class="login-page">
    <HeaderOrganism :showBurgerMenu="false" />

    <div class="login-content">
      <LoginCard />
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import TextAtom from "@/components/atoms/Text.vue";
import LoginCard from "@/components/sign/LoginCard.vue";

export default {
  components: {
      HeaderOrganism,
      FooterOrganism,
      TextAtom,
      LoginCard,
  },
};
</script>

<style scoped>
.login-page {
  text-align: center;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.login-content {
  margin: 0px auto;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 5.6;
  width: 100%;
}

@media (max-width: 700px) {
  .login-content {
      max-width: 100%;
      margin: 0;
      line-height: 4;
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 1;
  }

  .login-content :deep(.login-card) {
      width: 100%;
      max-width: 300px;
      margin: 0 auto;
  }

  :deep(.login-card) {
      font-size: 0.9rem;
  }

  :deep(input),
  :deep(button) {
      margin: 8px 0;
  }
}

@media (max-width: 380px) {
  .login-content {
      line-height: 3.5;
  }

  :deep(.login-card) {
      font-size: 0.85rem;
  }
}
</style>