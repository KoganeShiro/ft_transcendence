<template>
  <footer class="footer">
    <div class="footer-content">
      <p>&copy; 2025 Transcendental Teapot</p>
      <p>
        <router-link to="/privacy" class="footer-link">
          Legal Notices – Privacy Policy
        </router-link>
      </p>
    </div>
  </footer>
</template>

<script>
export default {};
</script>

<style scoped>
.footer {
  margin-top: 20px;
  background-color: #333;
  padding: 5px 10px;
  color: white;
  font-size: 0.9rem;
  text-align: center;
}

.footer-content {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.footer-content p {
  margin: 0;
}

.footer-link:hover {
  text-decoration: underline;
}

@media (max-width: 600px) {
  .footer-content {
    flex-direction: column;
  }
}
</style>