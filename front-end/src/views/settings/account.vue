<template>
    <div class="account-page">  
      <div class="account-content">
        <h1> {{ $t("account") }} </h1>
        <p>account stuff</p>
      </div>
      </div>
  </template>
  
  <script>

  </script>


<style scoped>
.account-page {
  text-align: center;
  color: white;
  background-color: #222;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.account-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}
</style>