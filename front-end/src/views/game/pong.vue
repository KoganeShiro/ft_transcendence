<template>
    <div class="pong-page">
      <HeaderOrganism />
  
      <div class="pong-content">
        <h1>pong</h1>
        <p>pong stuff</p>
      </div>
  
      <FooterOrganism />
    </div>
  </template>
  
  <script>
  import HeaderOrganism from "@/components/header/navbar.vue";
  import FooterOrganism from "@/components/footer.vue";
  
  export default {
    components: {
      HeaderOrganism,
      FooterOrganism,
    },
  };
  </script>


<style scoped>
.pong-page {
  text-align: center;
  color: white;
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.pong-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}
</style>