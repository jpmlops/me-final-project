<template>
  <div v-if="images.length > 0" class="grid grid-cols-6 gap-x-8 gap-y-4">
    <div v-for="image in images" :key="image" class="relative">
      <img :src="`${baseurl}${queryParam}/${image}`" :alt="`Image ${image}`" />
      <button
        class="absolute bottom-2 right-2 bg-blue-500 text-white text-[12px] px-2 py-2 rounded shadow-md hover:bg-blue-600"
        @click="moveFile(image, queryParam)"
      >
        Use for Training
      </button>
      <p v-if="uploading" class="pt-3">Uploading...</p>
      <!-- <p v-if="uploadResponse" class="pt-3 absolute top-2 right-2">{{ uploadResponse }}</p>-->
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
definePageMeta({ layout: "default" });

const images = ref<string[]>([]);
const skip = ref<number>(0);
const limit = 20;
// const isLoading = ref(false);
const uploading = ref(false);
const uploadResponse = ref("");
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

async function moveFile(imageName: string, queryParam: string) {
  if (!imageName) {
    uploadResponse.value = "Please select a file first.";
    return;
  }

  const formData = {
    imagename: imageName,
    subfolder: queryParam,
    source_folder: "abnormal",
    destination_folder: "training",
  };

  uploading.value = true;
  uploadResponse.value = "";

  try {
    const response = await fetch(`http://localhost:8020/move_file`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();
    uploadResponse.value = result.message || "Moved successful!";
    fetchImages();
  } catch (error) {
    uploadResponse.value = "Moved failed!";
  } finally {
    uploading.value = false;
  }
}
</script>

<style scoped>
/* Add your styles here */
</style>
