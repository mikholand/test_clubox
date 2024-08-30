<template>
  <div class="flex flex-col justify-center items-center h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white">
    <div v-if="isLoading" class="loading-spinner">
        <h1 class="text-2xl font-bold mb-6">Загрузка...</h1>
    </div>
    <div v-else>
      <h1 v-if="user" class="text-2xl font-bold mb-6">{{ greetingMessage }}</h1>
      <form @submit.prevent="submitForm" class="bg-white text-black p-8 rounded-lg shadow-lg w-300 max-w-md">
        <label for="birthdate" class="block text-lg font-semibold mb-4">Введите вашу дату рождения:</label>
        <div class="mb-6">
          <div class="picker-group">
            <VueScrollPicker :options="days" v-model="currentDay" />
            <VueScrollPicker :options="months" v-model="currentMonth" option-label="name" option-value="value" />
            <VueScrollPicker :options="years" v-model="currentYear" />
          </div>
        </div>
        <button 
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 ease-in-out"
        >
          Отправить
        </button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, computed, onMounted, defineComponent } from 'vue';
import type { PropType } from 'vue';
import type { VueScrollPickerOption } from 'vue-scroll-picker';
import '@vuepic/vue-datepicker/dist/main.css';
import axios from 'axios';
import { useRouter } from 'vue-router';

import { useWebApp } from 'vue-tg'

export default defineComponent({
  props: {
    options: {
      type: Array as PropType<VueScrollPickerOption[]>,
      default: () => [],
    },
  },
  setup() {
    const router = useRouter();
    const userId = useWebApp().initDataUnsafe.user.id;
    const fromEdit = router.currentRoute.value.query.fromEdit;

    const date = ref<Date | null>(null);
    const user = ref<{ first_name: string; last_name: string; birthdate: string } | null>(null);
    const isLoading = ref(true);

    const currentYear = ref<number>(2000);
    const currentMonth = ref<number>(1);
    const currentDay = ref<number>(1);


    const greetingMessage = computed(() => {
      if (user.value) {
        if (user.value.last_name) {
          return `Привет, ${user.value.first_name} ${user.value.last_name}!`;
        }
        return `Привет, ${user.value.first_name}!`;
      }
    });

    onMounted(async () => {
      console.log("fromEdit:", fromEdit);

      if (userId) {
        try {
          const response = await axios.get(`/api/user_data/${userId}`);
          console.log("Response data:", response.data);
          user.value = response.data;

          if (fromEdit && user.value && user.value.birthdate) {
            const [year, month, day] = user.value.birthdate.split('-').map(Number);
            currentYear.value = year;
            currentMonth.value = month;
            currentDay.value = day;
          }
        } catch (error) {
          alert("Error");
          console.error("Ошибка при получении данных пользователя:", error);
        }
      }

      if (!fromEdit && user.value && user.value.birthdate) {
        router.push(`/profile/${userId}`);
        return;
      }

      isLoading.value = false;
    });

    const submitForm = async () => {
      try {
        const formattedMonth = currentMonth.value.toString().padStart(2, '0');
        const formattedDay = currentDay.value.toString().padStart(2, '0');
        const birthdate = `${currentYear.value}-${formattedMonth}-${formattedDay}`;
        await axios.post('/api/save_birthdate/', {
          user_id: userId,
          birthdate: birthdate
        });
        router.push(`/profile/${userId}`); // Редирект на страницу профиля
      } catch (error) {
        console.error("Ошибка при отправке даты:", error);
      }
    };

    const years = computed(() => {
      const currYear = new Date().getFullYear();
      const lastYear = 1920;
      return Array.from({ length: currYear - lastYear + 1 }, (_, index) => lastYear + index);
    });

    const months = computed(() => [
      { value: 1, name: 'Январь' },
      { value: 2, name: 'Февраль' },
      { value: 3, name: 'Март' },
      { value: 4, name: 'Апрель' },
      { value: 5, name: 'Май' },
      { value: 6, name: 'Июнь' },
      { value: 7, name: 'Июль' },
      { value: 8, name: 'Август' },
      { value: 9, name: 'Сентябрь' },
      { value: 10, name: 'Октябрь' },
      { value: 11, name: 'Ноябрь' },
      { value: 12, name: 'Декабрь' }
    ]);

    const days = computed(() => {
      const lastDay = new Date(currentYear.value, currentMonth.value, 0).getDate();
      return Array.from({ length: lastDay }, (_, index) => index + 1);
    });

    return {
      date,
      user,
      greetingMessage,
      isLoading,
      submitForm,
      currentYear,
      currentMonth,
      currentDay,
      years,
      months,
      days
    };
  },
});
</script>


<style scoped>
.picker-group {
  display: flex;
}
</style>