<template>
  <div class="profile-page">
    <HeaderOrganism />

    <div class="profile-content">
      <h1>profile</h1>
      <p>
        add pseudo-sidebar component
        add stats component
        add history component (10 last one)
        friends table + add friends components
      </p>
      <AvatarAtom 
        pseudo="JohnDoe"
        :showPseudo="true"
        pseudoPosition="top"
      />
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import AvatarAtom from "@/components/atoms/avatar.vue";

export default {
  components: {
    HeaderOrganism,
    FooterOrganism,
    AvatarAtom,
  },
};
</script>

<style scoped>
.profile-page {
  text-align: center;
  color: white;
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.profile-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}
</style>