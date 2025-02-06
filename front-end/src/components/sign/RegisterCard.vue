<template>
  <div class="register-container">
    <Card class="register-card">
      <h3 class="register-title">{{ $t("welcome") }}</h3>
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
        <TextField
          id="confirm-password"
          v-model="confirmPassword"
          type="password"
          :label="$t('confirmPassword')"
          :placeholder="$t('confirmPassword')"
        />
      </InputGroup>
      
      <ButtonGroup class="button-group">
        <Button
          variant="primary"
          class="register-button"
          @click="onRegister"
        >
          {{ $t("register") }}
        </Button>
        <Button
          variant="42"
          class="register-button"
          @click="on42register"
        >
          {{ $t("register-42") }}
        </Button>
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
import defaultProfile from "@/assets/profile.png";

export default {
  name: "Register",
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
      confirmPassword: "",
    };
  },
  methods: {
    async onRegister() {
      if (this.username.trim() === "" || this.password.trim() === "" || this.confirmPassword.trim() === "") {
        alert("Please fill in all fields!");
        return;
      }
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      console.log("Password:", this.password);
      console.log("Lowercase:", /[a-z]/.test(this.password));
      console.log("Uppercase:", /[A-Z]/.test(this.password));
      console.log("Digit:", /\d/.test(this.password));
      console.log("Special character:", /[@$!%*?&]/.test(this.password));
      console.log("Length >= 8:", this.password.length >= 8);
      console.log("Regex test:", regex.test(this.password));

      if (!regex.test(this.password)) {
        alert("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.");
        return;
      }

      // Build payload for POST request
      const payload = {
        "username": this.username,
        "password": this.password,
        // "cover_photo": defaultProfile,
      };
      console.log("Payload:", payload);

      try {
        const response = await axios.post('https://localhost:1443/api/register/', payload, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log("Registration successful:", response.data);
        this.$router.push("/login");
      } catch (error) {
        console.error("Registration failed:", error);
        alert("Registration failed. Please try again.");
      }
    },
    on42register() {
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
  width: 500px;
  border-radius: 12px;
  background-color: #252525;
  color: var(--text-color);
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

/* You might want to style the disabled state differently */
.register-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-group {
  width: 95%;
  margin-bottom: 10%;
}

.button-group {
  display: flex;
  gap: 10px;
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
