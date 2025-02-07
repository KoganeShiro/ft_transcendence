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
      loading: false, // Add loading flag
    };
  },
  methods: {
    formValid() {
      // All fields must be non-empty.
      console.log(this.username.trim() !== "" &&
        this.password.trim() !== "" &&
        this.confirmPassword.trim() !== "");
      return (
        this.username.trim() !== "" &&
        this.password.trim() !== "" &&
        this.confirmPassword.trim() !== ""
      );
    },
    async onRegister() {
      if (this.loading) return;
      this.loading = true;

      if (!this.formValid()) {
        alert("Please fill in all fields!");
        this.loading = false;
        return;
      }
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match!");
        this.loading = false;
        return;
      }
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?;&=.<>:|\- /+()#])[A-Za-z\d@$!%*;?&=.<>:|\-/+()#]{8,}$/;
      if (!regex.test(this.password)) {
        alert("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.");
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
        //make a better error message if the user already exist
        alert("Registration failed. Please try again.");
      } finally {
        this.loading = false;
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
