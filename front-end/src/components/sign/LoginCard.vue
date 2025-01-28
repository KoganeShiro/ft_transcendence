<template>
  <div class="login-container">
    <Card class="login-card">
      <h3 class="login-title">{{ $t("welcome-back") }}</h3>
      <InputGroup class="input-group">
        <TextField
          id="username"
          :label="$t('username')"
          :placeholder="$t('enter-username')"
        />
        <TextField
          id="password"
          :label="$t('password')"
          :placeholder="$t('enter-password')"
        />
      </InputGroup>
      <!--
      If login success, token in cookie (auth et refresh)
        when auth token expired, should send refresh token to get a new auth token
      if error, show error
      -->
      <ButtonGroup class="button-group">
        <Button variant="primary" class="login-button" @click="onLogin" >{{ $t("login") }}</Button>
        <Button variant="42" class="login-button" @click="onLogin">{{ $t("login-42") }}</Button>
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
    onLogin() {
      // check if the username/mail and password is ok
      this.$router.push("/profile");
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  width: 100%;
  border-radius: 12px;
  background-color: #252525;
  color: #ffffff;
}

.login-title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
}

.login-button {
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
  .login-card {
    max-width: 60%;
  }

  .login-title {
    font-size: 24px;
  }
}
</style>
