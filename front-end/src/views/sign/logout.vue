<template>
    <div class="logout-page">
      <HeaderOrganism />
  
      <div class="logout-content">
        <LogoutCard />
      </div>
  
      <FooterOrganism />
    </div>
  </template>
  
  <script>
  import HeaderOrganism from "@/components/header/navbar.vue";
  import FooterOrganism from "@/components/footer.vue";
  import TextAtom from "@/components/atoms/Text.vue";
  import LogoutCard from "@/components/sign/LogoutCard.vue";
  
  export default {
    components: {
        HeaderOrganism,
        FooterOrganism,
        TextAtom,
        LogoutCard,
    },
  };
  </script>
  
  <style scoped>
  .logout-page {
    text-align: center;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .logout-content {
    margin: 0px auto;
    max-width: 800px;
    color: white;
    font-size: 1rem;
    line-height: 4.6;
    width: 100%;
  }
  
  @media (max-width: 700px) {
    .logout-content {
        max-width: 100%;
        margin: 0;
        line-height: 4;
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 1;
    }
  
    .logout-content :deep(.logout-card) {
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
    }
  
    :deep(.logout-card) {
        font-size: 0.9rem;
    }
  
    :deep(input),
    :deep(button) {
        margin: 8px 0;
    }
  }
  
  @media (max-width: 380px) {
    .logout-content {
        line-height: 3.5;
    }
  
    :deep(.logout-card) {
        font-size: 0.85rem;
    }
  }
  </style>