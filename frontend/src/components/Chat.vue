<template>
  <div>
    <input type="file" @change="uploadFile" />
    <p v-if="fileUploaded">📄 Файл загружен!</p>

    <input v-model="message" placeholder="Введите вопрос" />
    <button @click="sendMessage" :disabled="!fileUploaded || loading">
      {{ loading ? "Ждём ответ..." : "Отправить" }}
    </button>

    <p v-if="response">Ответ: {{ response }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      response: '',
      fileUploaded: false,
      loading: false,
    };
  },
  methods: {
   async uploadFile(e) {
  const file = e.target.files[0];
  const form = new FormData();
  form.append("file", file);
  try {
    const res = await axios.post("http://localhost:8000/upload", form);
    if (res.data.status === "Файл загружен") {
      this.fileUploaded = true;
    } else {
      alert("Файл не был принят сервером.");
    }
  } catch (err) {
    alert("Ошибка при загрузке файла");
    console.error(err);
  }
}
,
    async sendMessage() {
      if (!this.message.trim()) return;
      this.loading = true;
      this.response = "";
      try {
        const res = await axios.post("http://localhost:8000/chat", {
          message: this.message,
        });
        this.response = res.data.response;
      } catch (err) {
        this.response = "Ошибка при получении ответа";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>


<style scoped>
.chat {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
  background: #121212;
  color: white;
}

.message {
  background: #f2f2f2;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  color: #000;
}

input {
  width: 80%;
  padding: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
}
</style>
