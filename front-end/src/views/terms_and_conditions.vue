<template>
    <div class="terms-page">
      <HeaderOrganism />
  
      <div class="terms-content">
        <h1>Terms and Conditions</h1>
        <p>Here, you can add your legal notices and privacy policy text.</p>
      </div>
  
      <FooterOrganism />
    </div>
  </template>
  
  <script>
  import HeaderOrganism from "@/components/header/navbar.vue";
  import FooterOrganism from "@/components/header/navbar.vue";
  
  export default {
    components: {
      HeaderOrganism,
      FooterOrganism,
    },
  };
  </script>
  
  <style scoped>
  .terms-page {
    text-align: center;
    color: white;
    background-color: #222;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .terms-content {
    margin: 50px auto;
    padding: 20px;
    max-width: 800px;
    color: white;
    font-size: 1rem;
    line-height: 1.6;
  }
  </style>
  