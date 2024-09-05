<template>
  <div class="overflow-x-auto w-full mt-6">
    <h1 class="text-[20px] text-[#ffffff] mb-2">Training data list</h1>
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-[#F0F3F4]">
        <tr>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            Video Name
          </th>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            Frames List
          </th>

          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            Re-train Model
          </th>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            Accuracy
          </th>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            Performance Matrix
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="(item, index) in data" :key="index">
          <td
            class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
          >
            {{ item.name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            <NuxtLink
              :to="{
                path: 'training',
                query: { param: item.slug, ctype: 'training' },
              }"
              class="text-red-700 border-2 border-orange-500 py-1 px-3"
            >
              Training Frame List
            </NuxtLink>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            <button class="text-red-700 border-2 border-orange-500 py-1 px-3">Train</button>
          </td>
          <td
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            Accuracy {}
          </td>
          <td
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            Matrix {}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
definePageMeta({ layout: "default" });
// const data = [{ Video: "mlops.mp4", Frames: "List", Delete: "Delete" }];

const data = ref<any[]>([]);
const status = ref(false);
const fetchImages = async (): Promise<void> => {
  try {
    const response = await fetch("http://localhost:8020/video-frames", {
      method: "GET",
    });
    const res = await response.json();
    const resArray: string[] = res.frames;
    console.log(resArray);
    data.value.push(...resArray);

    // skip.value += limit;
  } catch (error) {
    console.error("Error fetching images:", error);
  }
};
const processVideo = async (name: string): Promise<void> => {
  try {
    if (name == null || name == "") return;

    status.value = true;
    const response = await fetch(
      "http://localhost:8020/find-abnormal-case/" + name,
      {
        method: "GET",
      }
    );
    const res = await response.json();
    console.log(res);
    status.value = false;
    fetchImages();
  } catch (error) {
    console.error("Error fetching images:", error);
  }
};
onMounted(() => {
  fetchImages();
});
</script>
