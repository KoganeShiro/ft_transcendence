<template>
  <div class="match">
    <TextBox :modelValue="match.player1" :modifiable="false" class="player player1" />
    <div class="vs-container">
      <span class="vs">VS</span>
    </div>
    <TextBox :modelValue="match.player2" :modifiable="false" class="player player2" />
  </div>
</template>

<script>
import TextBox from "@/components/atoms/ModifyInformations.vue";
export default {
  name: "MatchItem",
  components: { TextBox },
  props: {
    match: { type: Object, required: true }
  }
};
</script>

<style scoped>
.match {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-radius: 12px;
  background: linear-gradient(var(--card-color), var(--card-color-light));
  box-shadow: 3px 3px 6px var(--sidebar-color), -3px -3px 6px var(--sidebar-color);
  transition: all 0.3s ease;
}

.match:hover {
  transform: translateY(-3px);
}

.player {
  flex: 1;
  max-width: 45%;
}

.player1 {
  text-align: right;
}

.player2 {
  text-align: left;
}

.vs-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(145deg, #ff6b6bb6, #ff8e8eab);
  margin-right: 10px;
}

.vs {
  font-weight: bold;
  font-size: 1.4em;
  color: #ffffff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

@media (max-width: 600px) {
  .vs-container {
  margin-right: 7px;
}
}

</style>
