import { useStore } from 'vuex';

export function useTheme() {
  const store = useStore();

  const changeTheme = (theme) => {
    const validThemes = ['light', 'dark', 'ocean', 'forest', 'volcano', 'teapot'];
    const selectedTheme = validThemes.includes(theme.toLowerCase()) ? theme : 'dark';
    store.dispatch('changeTheme', selectedTheme);
    document.documentElement.setAttribute('data-theme', selectedTheme);
    localStorage.setItem('theme', selectedTheme);
  };

  return {
    changeTheme
  };
}