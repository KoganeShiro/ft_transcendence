<template>
  <div class="avatar" :class="{ 'pseudo-top': pseudoPosition === 'top' }">
    <template v-if="link">
      <a :href="link" target="_blank" rel="noopener noreferrer">
        <div class="avatar-image">
          <img :src="avatarImage" :alt="pseudo" />
        </div>
        <span v-if="showPseudo" class="pseudo">{{ pseudo }}</span>
      </a>
    </template>
    <template v-else>
      <div class="avatar-image">
        <img :src="avatarImage" :alt="pseudo" />
      </div>
      <span v-if="showPseudo" class="pseudo">{{ pseudo }}</span>
    </template>
  </div>
</template>

<script>
import defaultAvatar from '@/assets/profile.png';

export default {
  name: 'AvatarAtom',
  props: {
    imageUrl: {
      type: String,
      default: ''
    },
    pseudo: {
      type: String,
      default: 'Username42'
    },
    showPseudo: {
      type: Boolean,
      default: true
    },
    pseudoPosition: {
      type: String,
      default: 'bottom',
      validator: (value) => ['top', 'bottom', 'right'].includes(value)
    },
    link: {
      type: String,
      default: ''
    }
  },
  computed: {
    avatarImage() {
      return (this.imageUrl || defaultAvatar);
    }
  }
}
</script>

<style scoped>
.avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar a {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: inherit;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.avatar a:hover {
  transform: translateY(-10px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.avatar-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.avatar-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pseudo {
  margin-top: 10px;
  font-weight: bold;
}

.pseudo-top {
  flex-direction: column-reverse;
}

.pseudo-top .pseudo {
  margin-top: 0;
  margin-bottom: 10px;
}

.pseudo-right {
  flex-direction: row;
}
</style>