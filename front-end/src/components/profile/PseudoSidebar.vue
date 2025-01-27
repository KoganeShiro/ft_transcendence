<template>
  <nav class="pseudo-sidebar">
    <ul>
      <li
        v-for="(item, index) in menuItems"
        :key="index"
        :class="{ active: activeItem === item.key }"
      >
        <router-link
          :to="item.route"
          class="button-link"
          @click="handleClick(item.key)"
        >
          <ButtonAtom variant="sidebar">
            {{ item.label }}
          </ButtonAtom>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  components: {
    ButtonAtom,
  },
  props: {
    menuItems: {
      type: Array,
      required: true,
    },
    activeItem: {
      type: String,
      default: "",
    },
  },
  emits: ["update:activeItem"],
  methods: {
    handleClick(key) {
      this.$emit("update:activeItem", key);
    },
  },
};
</script>

<style scoped>
.pseudo-sidebar {
  /* width: auto; */
  padding: 20px;
  position: sticky;
}

.pseudo-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.pseudo-sidebar li {
  margin: 10px 0;
}

.button-link {
  text-decoration: none;
}

.pseudo-sidebar .button-link {
  display: block;
  width: 100%;
}

/* Responsive Design */
@media (max-width: 768px) {
  .pseudo-sidebar ul {
    display: flex;
    flex-direction: row; /* Display items in a row */
    justify-content: center; /* Center items horizontally */
  }

  .pseudo-sidebar li {
    margin: 0 10px; /* Add horizontal spacing between items */
  }
}
</style>