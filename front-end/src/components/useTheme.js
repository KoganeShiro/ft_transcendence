import { useStore } from 'vuex';

export function useTheme() {
  const store = useStore();

  const changeTheme = (theme) => {
    store.dispatch('changeTheme', theme);
    document.documentElement.setAttribute('data-theme', theme);
  };

  return {
    changeTheme
  };
}
