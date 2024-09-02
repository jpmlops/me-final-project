<template>
  <div v-if="images.length > 0" class="grid grid-cols-6 gap-x-8 gap-y-4">
    <div v-for="image in images" :key="image" class="relative"> 
      <img :src="`${baseurl}${queryParam}/${image}`" :alt="`Image ${image}`" />
      <button class="absolute bottom-2 right-2 bg-blue-500 text-white text-[12px] px-2 py-2 rounded shadow-md hover:bg-blue-600">
     Use for Training
    </button>
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
const ctype = route.query.ctype;
console.log(ctype, ">>>");
const baseurl =
  ctype == "true"
    ? "http://localhost:8020/frames/"
    : "http://localhost:8020/abnormal/";
const fetchImages = async (): Promise<void> => {
  try {
    const response = await fetch(
      `http://localhost:8020/frames-list/${queryParam}?type=${ctype?.toString()}`,
      {
        method: "GET",
      }
    );
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
