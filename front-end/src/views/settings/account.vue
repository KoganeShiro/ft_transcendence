<template>
  <div class="account-card" v-if="!loading">
    <div class="header">
      <h1>{{ $t("account") }}</h1>
    </div>
    <div class="avatar-section">
      <AvatarAtom 
        :pseudo="user.name" 
        :showPseudo="false" 
      />
    </div>
    <div class="form-section">
      <div class="field">
        <label>{{ $t("username") }}</label>
        <EditableTextField 
          v-model="user.name" 
          :modifiable="true" 
          placeholder="Enter your username" 
        />
      </div>
      <div class="field">
        <label>{{ $t("email") }}</label>
        <EditableTextField 
          v-model="user.mail" 
          :modifiable="true" 
          placeholder="Enter your email" 
        />
      </div>
      <div class="field">
        <label>{{ $t("password") }}</label>
        <EditableTextField 
          v-model="user.password" 
          :modifiable="true" 
          placeholder="Enter new password" 
        />
      </div>
    </div>
    <div class="button-section">
      <ButtonAtom 
        variant="attention" 
        @click="removeAccount"
        :width="'80%'"
        :fontSize="'1.2rem'"
      >
        {{ $t("delete-account") }}
      </ButtonAtom>
    </div>
  </div>
  <div v-else class="loading">
    <p>{{ $t("loading") }}...</p>
  </div>
</template>

<script>
import axios from "axios";
import AvatarAtom from "@/components/atoms/Avatar.vue";
import EditableTextField from "@/components/atoms/ModifyInformations.vue";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  name: "AccountCard",
  components: {
    AvatarAtom,
    EditableTextField,
    ButtonAtom,
  },
  data() {
    return {
      user: {
        name: "",
        mail: "",
        password: "",
        avatar: "",
      },
      loading: false,
    };
  },
  methods: {
    initAccount() {
      this.loading = true;
      axios.get("/api/account")
        .then(response => {
          const data = response.data;
          // this.user.name = data.name;
          this.user.name = "username42";
          this.user.mail = data.mail;
          this.user.avatar = data.avatar || "/assets/profile.png";
          this.user.password = "*************";
        })
        .catch(error => {
          console.error("Error fetching account data:", error);
          // Optionally, handle errors here (e.g., show an error message)
        })
        .finally(() => {
          this.loading = false;
        });
    },
    saveProfile() {
      axios.patch("/api/account", {
        name: this.user.name,
        mail: this.user.mail,
        password: this.user.password,
      })
      .then(response => {
        alert(this.$t("profile_saved_successfully"));
        // Optionally update local state based on response.
      })
      .catch(error => {
        console.error("Error saving profile:", error);
        alert(this.$t("error_saving_profile"));
      });
    },
    removeAccount() {
      if (confirm(this.$t("delete-account-msg"))) {
        axios.delete("/api/account")
          .then(response => {
            alert(this.$t("account_deleted_successfully"));
            // Optionally, redirect the user or update the UI accordingly.
          })
          .catch(error => {
            console.error("Error deleting account:", error);
            alert(this.$t("error_deleting_account"));
          });
      }
    },
  },
  mounted() {
    this.initAccount();
  },
};
</script>

<style scoped>
.account-card {
  max-width: 500px;
  margin: 40px auto;
  background: var(--card-color);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.header h1 {
  margin-bottom: 20px;
  font-size: 2rem;
  border-bottom: 1px solid #44444434;
  padding-bottom: 10px;
  color: var(--text-color);
}

.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 25px;
}

.form-section {
  margin-bottom: 30px;
}

.field {
  margin-bottom: 20px;
  text-align: left;
}

.field label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: var(--text-color);
  font-size: 0.9rem;
}

.button-section {
  display: flex;
  flex-direction: column;
  padding: 10px;
  gap: 15px;
  align-items: center;
}

.loading {
  text-align: center;
  color: var(--text-color);
  font-size: 1.5rem;
  margin-top: 100px;
}
</style>
