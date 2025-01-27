<template>
    <div class="register-container">
      <Card class="register-card">
        <h3 class="register-title">Welcome</h3>
        <InputGroup class="input-group">
          <TextField
            id="username"
            label="Username"
            placeholder="Enter your username"
          />
          <TextField
            id="mail"
            label="E-mail"
            placeholder="Enter you e-mail"
          />
          <TextField
            id="password"
            label="Password"
            placeholder="Enter your password"
          />
          <TextField
            id="confirm-password"
            label="Confirm Password"
            placeholder="Confirm your password"
          />
        </InputGroup>
        <ButtonGroup class="button-group">
          <!-- Send a POST Request with the informations in json format
                Send back error or not -->
          <Button variant="primary" class="register-button" @click="onregister" >Register</Button>
          <Button variant="42" class="register-button" @click="on42register">Register with 42</Button>
        </ButtonGroup>
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
      onregister() {
        /* should have input in the TextField, check if
        the username and password are valid, then register
        Return login page if successful
        */
        this.$router.push("/login");
      },
      on42register() {
        // If register with 42, should have a 42 API to register
        // and return account page
        this.$router.push("/profile");
      }
    },
  };
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .register-card {
    width: 100%;
    border-radius: 12px;
    background-color: #252525;
    color: #ffffff;
  }
  
  .register-title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    line-height: 1;
  }
  
  .register-button {
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
    .register-card {
      max-width: 60%;
    }
  
    .register-title {
      font-size: 24px;
    }
  }
  </style>
  