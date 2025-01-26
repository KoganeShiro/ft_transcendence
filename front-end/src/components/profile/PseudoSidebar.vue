<template>
  <nav class="pseudo-sidebar">
    <ul>
      <li
        v-for="(item, index) in menuItems"
        :key="index"
        :class="{ active: activeItem === item.key }"
      >
        <!-- Use router-link for navigation -->
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
      this.$emit("update:activeItem", key); // Emit active item to parent for tracking
    },
  },
};
</script>

<style scoped>
.pseudo-sidebar {
  width: 20%;
  background-color: #333;
  padding: 20px;
  border-right: 1px solid #444;
  height: 100%;
  position: sticky;
  top: 0;
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
  width: 100%;
  display: block;
}

.pseudo-sidebar .active .button-link > ButtonAtom {
  background-color: #4caf50;
  color: white;
}

.pseudo-sidebar ButtonAtom:hover {
  background-color: #555;
}
</style>
