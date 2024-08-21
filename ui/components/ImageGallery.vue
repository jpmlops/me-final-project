<template> 
  <div v-if="images.length > 0" class="grid grid-cols-12 gap-x-8 gap-y-4">
    <div v-for="image in images" :key="image">
      <img
        :src="`http://localhost:8020/frames/${queryParam}/${image}`"
        :alt="`Image ${image}`"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
definePageMeta({ layout: "default" });

const images = ref<string[]>([]);
const skip = ref<number>(0);
const limit = 20;
const route = useRoute();
const queryParam = route.query.param;
console.log(queryParam, ">>> queryParam");
const fetchImages = async (): Promise<void> => {
  try {
    const response = await fetch(`http://localhost:8020/frames-list/${queryParam}`, {
      method: "GET",
    });
    const res = await response.json();
    const newImages: string[] = res.frames;
    console.log(newImages);
    images.value.push(...newImages);
    console.log("img", images.value[0]);
    // skip.value += limit;
  } catch (error) {
    console.error("Error fetching images:", error);
  }
};

// const loadMore = async () => {
//   await fetchImages();
// };

onMounted(() => {
  fetchImages();
});
</script>

<style scoped>
/* Add your styles here */
</style>
