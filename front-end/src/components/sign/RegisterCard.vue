<template>
  <div class="register-container">
    <Card class="register-card">
      <h3 class="register-title">{{ $t("welcome") }}</h3>
      <InputGroup class="input-group">
        <!-- Bind the input fields with v-model -->
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
      
      <!-- Terms and Services Checkbox -->
      <div class="terms-container">
        <input type="checkbox" id="terms" v-model="acceptedTerms" />
        <label for="terms">
          {{ $t("iAgreeTo") }}
          <router-link to="/terms" class="terms-link">
            {{ $t("terms-service") }}
          </router-link>
        </label>
      </div>
      
      <!--
      Expected POST request:
      POST https://localhost:1443/api/register/
      Content-Type: application/json

      { "username": "user1", "password": "Pass1234!", "cover_photo": null }
      -->
      
      <ButtonGroup class="button-group">
        <!-- Registration button: disabled until the form is valid -->
        <Button
          variant="primary"
          class="register-button"
          @click="onRegister"
          :disabled="!formValid()"
        >
          {{ $t("register") }}
        </Button>
        <Button
          variant="42"
          class="register-button"
          @click="on42register"
          :disabled="!acceptedTerms"
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
      acceptedTerms: false, // Checkbox value
      loading: false,
    };
  },
  methods: {
    formValid() {
      // All fields must be non-empty and the terms must be accepted.
      const valid =
        this.username.trim() !== "" &&
        this.password.trim() !== "" &&
        this.confirmPassword.trim() !== "" &&
        this.acceptedTerms;
      return valid;
    },
    goodPassword(password) {
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?;&=.<>:|\-\/+()#])[A-Za-z\d@$!%*?;&=.<>:|\-\/+()#]{8,}$/;
      return regex.test(password);
    },
    async onRegister() {
      if (this.loading) return;
      this.loading = true;

      if (!this.formValid()) {
        alert("Please fill in all fields and accept the Terms and Services!");
        this.loading = false;
        return;
      }
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match!");
        this.loading = false;
        return;
      }
      if (!this.goodPassword(this.password)) {
        alert(
          "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        );
        this.loading = false;
        return;
      }

      // Build payload for POST request
      const payload = {
        username: this.username,
        password: this.password,
        // cover_photo: defaultProfile,
      };

      try {
        const response = await axios.post('/api/register/', payload, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log("Registration successful:", response.data);
        this.$router.push("/login");
      } catch (error) {
        console.error("Registration failed:", error);
        alert("Registration failed. Please try again.");
      } finally {
        this.loading = false;
      }
    },
    async on42register() {
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
  padding: 20px;
}

.register-title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  line-height: 1;
  margin-bottom: 20px;
}

.input-group {
  width: 95%;
  margin-bottom: 10%;
}

/* Terms container styling */
.terms-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px;
  color: #ccc;
}

.terms-container input[type="checkbox"] {
  margin-right: 8px;
}

.terms-link {
  color: var(--primary-color, #36A2EB);
  text-decoration: underline;
}

.button-group {
  display: flex;
  gap: 10px;
}

.register-button {
  margin-top: 3%;
  width: 100%;
  font-size: 20px;
  padding: 15px 0;
  border-radius: 8px;
}

/* Style disabled state */
.register-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
