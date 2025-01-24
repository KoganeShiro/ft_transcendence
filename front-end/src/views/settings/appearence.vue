<template>
    <div class="appearence-page">
      <HeaderOrganism />
  
      <div class="appearence-content">
        <h1>appearence</h1>
        <p>appearence stuff</p>
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
.appearence-page {
  text-align: center;
  color: white;
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.appearence-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}
</style>