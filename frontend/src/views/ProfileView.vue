<template>
  <div class="flex flex-col justify-center items-center h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white">
    <div v-if="isLoading" class="loading-spinner">
        <h1 class="text-2xl font-bold mb-6">Загрузка...</h1>
    </div>
    <div v-else>
      <h1 class="text-2xl font-bold mb-6">Профиль пользователя</h1>
      <div v-if="profile" class="bg-white text-black p-6 rounded-lg shadow-md w-80">
          <div class="text-center">
            <img v-if="profile.user.photo"
              :src="profile.user.photo"
              class="mx-auto w-24 rounded-full shadow-lg mb-5"
              alt="Avatar" />
            <img v-else
              src="https://i.pinimg.com/originals/fc/04/73/fc047347b17f7df7ff288d78c8c281cf.png"
              class="mx-auto w-24 rounded-full shadow-lg mb-5"
              alt="Avatar" />
          </div>
          <p class="text-lg mb-2"><span class="font-semibold">Имя:</span> {{ profile.user.first_name }}</p>
          <p class="text-lg mb-2" v-if="profile.user.last_name" ><span class="font-semibold">Фамилия:</span> {{ profile.user.last_name }}</p>
          <p class="text-lg mb-2" v-if="profile.user.username"><span class="font-semibold">Юзернейм:</span> {{ profile.user.username }}</p>
          <p class="text-lg mb-2" v-else><span class="font-semibold">Юзернейм:</span> отсутствует</p>
          <p class="text-lg mb-2"><span class="font-semibold">День рождения:</span> {{ birthdate }}</p>
          <p class="text-lg mb-4">{{ timeLeft }}</p>
          <button  
              v-if="isOwner" 
              @click="changeBirthdate"
              class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 ease-in-out mb-3"
          >
              Изменить дату рождения
          </button>
          <button 
              v-else 
              @click="openTelegramBot"
              class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 ease-in-out mb-3"
          >
              Перейти в бот
          </button>
          <button 
              @click="shareProfile"
              class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 ease-in-out"
          >
              Поделиться данными
          </button>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useWebApp, useWebAppViewport } from 'vue-tg'

const route = useRoute();
const router = useRouter();
const profile = ref<{ user: { user_id: number, first_name: string; last_name: string; username: string; birthdate: string; photo: string }, time_left: number } | null>(null);
const birthdate = ref('');
const timeLeft = ref('');
const currentUserId = useWebApp().initDataUnsafe.user.id.toString();
const isOwner = ref(false);
const isLoading = ref(true);

useWebAppViewport().expand();

onMounted(async () => {
  const userId = route.params.user_id;
  try {
    const response = await axios.get(`/api/profile/${userId}`);
    profile.value = response.data;
    calculateTimeLeft(response.data.time_left);

    if (profile.value && profile.value.user.birthdate) {
      const [year, month, day] = profile.value.user.birthdate.split('-').map(Number);
      const formattedMonth = month.toString().padStart(2, '0');
      const formattedDay = day.toString().padStart(2, '0');
      birthdate.value = `${formattedDay}.${formattedMonth}.${year}`
    }

    if (userId === currentUserId) {
      isOwner.value = true;
    }

    isLoading.value = false;
  } catch (error) {
    console.error("Ошибка при загрузке профиля:", error);
  }
});

function calculateTimeLeft(totalMinutesLeft: number) {
  const offsetMinutes = new Date().getTimezoneOffset();
  const totalMinutesLeftTimeZone = totalMinutesLeft + offsetMinutes;
  const days = Math.floor(totalMinutesLeftTimeZone / (24 * 60));
  const hours = Math.floor((totalMinutesLeftTimeZone % (24 * 60)) / 60);
  const minutes = Math.floor(totalMinutesLeftTimeZone % 60);

  const parts = [];
  if (days > 0) parts.push(`${days} дней`);
  if (hours >= 0) parts.push(`${hours} часов`);
  if (minutes >= 0) parts.push(`${minutes} минут`);

  timeLeft.value = `До следующего дня рождения осталось: ${parts.join(', ')}`;
}

const changeBirthdate = () => {
  router.replace({ path: `/`, query: { fromEdit: 'true' } });
};

const shareProfile = () => {
  const userId = route.params.user_id;
  const profileUrl = `https://t.me/mikholand_bot/profiles?startapp=${userId}`;
  const message = `Посмотри мой профиль!`;

  const tgUrl = `https://t.me/share/url?url=${encodeURIComponent(profileUrl)}&text=${encodeURIComponent(message)}`
  window.open(tgUrl, '_blank');
};

function openTelegramBot() {
    window.open(`https://t.me/mikholand_bot?start`);
}
</script>


<style scoped>
</style>
