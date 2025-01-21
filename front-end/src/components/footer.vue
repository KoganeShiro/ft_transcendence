<template>
  <footer class="footer">
    <p>Copyright © 2025 &lt;nom de la team&gt;</p>
    <p>
      <router-link to="/terms-and-conditions" class="footer-link">
        Mentions légales – Politique de confidentialité
      </router-link>
    </p>
  </footer>
</template>

<script>
export default {};
</script>

<style scoped>
.footer {
  background-color: #333;
  padding: 10px 20px;
  color: white;
  font-size: 0.9rem;
  text-align: center;
}

.footer-link {
  color: #00aaff;
  text-decoration: none;
}

.footer-link:hover {
  text-decoration: underline;
}
</style>
