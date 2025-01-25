<template>
    <div class="logout-container">
      <Card class="logout-card">
        <h3 class="logout-title">Oh no 🥺</h3>
        <h3 class="logout-title">
            are you sure you want to logout ?
        </h3>
        <Button variant="attention" class="logout-button" @click="onlogout" >Yes, logout</Button>
        <Button variant="42" class="logout-button" @click="ongoback">No, i miss clicked</Button>
      </Card>
    </div>
  </template>
  
  <script>
  import Card from "@/components/atoms/Card.vue";
  import TextField from "@/components/atoms/TextField.vue";
  import Button from "@/components/atoms/Button.vue";
  import ButtonGroup from "@/components/atoms/ButtonGroup.vue";
  import InputGroup from "@/components/atoms/TextFieldGroup.vue";
  
  export default {
    components: {
      Card,
      TextField,
      Button,
      InputGroup,
      ButtonGroup,
    },
    methods: {
      onlogout() {
        this.$router.push("/");
      },
      ongoback() {
        this.$router.push("/profile");
      },
    },
  };
  </script>
  
  <style scoped>
  .logout-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .logout-card {
    width: 100%;
    border-radius: 12px;
    background-color: #252525;
    color: #ffffff;
  }
  
  .logout-title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    line-height: 1;
  }
  
  .logout-button {
    margin-top: 3%;
    width: 100%;
    font-size: 20px;
    padding: 15px 0;
    border-radius: 8px;
  }
  
  .input-group {
    width: 95%;
    margin-bottom: 10%;
  }
  
  @media (max-width: 700px) {
    .logout-card {
      max-width: 60%;
    }
  
    .logout-title {
      font-size: 24px;
    }
  }
  </style>
  