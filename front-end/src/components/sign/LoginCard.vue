<template>
  <div class="login-container">
    <Card class="login-card">
      <h3 class="login-title">{{ $t("welcome-back") }}</h3>
      <InputGroup class="input-group">
        <TextField
          id="username"
          v-model="username"
          :label="$t('username')"
          :placeholder="$t('enter-username')"
        />
        <TextField
          id="password"
          v-model="password"
          type="password"
          :label="$t('password')"
          :placeholder="$t('enter-password')"
        />
      </InputGroup>
      <ButtonGroup class="button-group">
        <Button variant="primary" class="login-button" @click="onLogin">{{ $t("login") }}</Button>
        <Button variant="42" class="login-button" @click="on42Login">{{ $t("login-42") }}</Button>
      </ButtonGroup>
    </Card>
  </div>
</template>

<script>
import axios from 'axios';
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
  data() {
    return {
      username: "",
      password: "",
      loading: false,
    };
  },
  methods: {
    async onLogin() {
      if (this.loading) return;
      this.loading = true;

      const payload = {
        username: this.username,
        password: this.password,
      };

      try {
        const response = await axios.post('/api/login/', payload, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log("Login successful:", response.data);
        // Handle token storage and redirection
        // document.cookie = `access=${response.data.access}; path=/`;
        // document.cookie = `refresh=${response.data.refresh}; path=/`;
        this.$router.push("/profile");
      } catch (error) {
        console.error("Login failed:", error);
        alert("Login failed. Please try again.");
      } finally {
        this.loading = false;
      }
    },
    async on42Login() {
      if (this.loading) return;
      this.loading = true;

      try {
        // const response = await axios.get('/api/auth/login42/');
        // console.log("42 Login successful:", response.data);

        window.location.href = "/api/auth/login42/";

        // Handle token storage and redirection
        // document.cookie = `access=${response.data.access}; path=/`;
        // document.cookie = `refresh=${response.data.refresh}; path=/`;
        // this.$router.push("/profile");
      } catch (error) {
        console.error("42 Login failed:", error);
        alert("42 Login failed. Please try again.");
      } finally {
        this.loading = false;
      }
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
  width: 500px;
  border-radius: 12px;
  color: var(--text-color);
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
