import { useI18n } from 'vue-i18n'

export function useLanguage() {
  const { locale } = useI18n({ useScope: 'global' })

  const changeLanguage = (lang) => {
    // console.log("Changing language to", lang)
    locale.value = lang
  }

  return {
    changeLanguage
  }
}