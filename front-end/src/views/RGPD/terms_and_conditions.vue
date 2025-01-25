<template>
  <div class="terms-page">
    <HeaderOrganism />

    <main class="terms-content">
      <h1 class="terms-title">{{ t('terms.title') }}</h1>
      <p class="last-updated">{{ t('terms.lastUpdated') }}</p>

      <!-- Should change the text by the language -->
      <router-link to="/privacy" class="footer-link">
        <TextAtom class="privacy-link">Privacy Policy</TextAtom>
      </router-link>

      <section
        v-for="section in rawTermsSections"
        :key="section.title"
        class="terms-section"
      >
        <h2 class="section-title">{{ section.title }}</h2>
        <div class="section-content">
          <p
            v-for="(content, idx) in section.content"
            :key="idx"
            class="content-paragraph"
          >
            {{ content }}
          </p>
        </div>
      </section>
    </main>

    <FooterOrganism />
  </div>
</template>


<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import TextAtom from "@/components/atoms/Text.vue";
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  components: {
    HeaderOrganism,
    FooterOrganism,
    TextAtom,
  },
  setup() {
    const { t, messages, locale } = useI18n();
    const rawTermsSections = computed(() => {
      const allMessages = messages.value;
      const currentLocaleMessages = allMessages[locale.value];
      return currentLocaleMessages?.terms?.sections || [];
    });

    return {
      t,
      rawTermsSections
    };
  }
};
</script>


<style scoped>
.terms-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-family: "Arial", sans-serif;
}

.terms-content {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.terms-title {
  font-size: 2rem;
  margin-bottom: 10px;
  text-align: center;
}

.last-updated {
  font-style: italic;
  text-align: center;
  margin-bottom: 30px;
}

.terms-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.section-content .content-paragraph {
  font-size: 1rem;
  line-height: 1.8;
  margin-bottom: 10px;
  text-align: justify;
}

</style>
