<template>
  <div class="chat-container">
    <h2 class="chat-title">🤖 ЧатБек</h2>

    <div class="upload-section">
      <label class="custom-file-upload">
        <input type="file" @change="uploadFile" />
        📁 Выберите файл
      </label>
      <p v-if="fileUploaded" class="status">📄 Файл успешно загружен</p>
    </div>

    <div class="chat-box">
      <div class="messages">
        <div v-for="(msg, index) in messages" :key="index" class="message">
          <p><strong>You:</strong> {{ msg.question }}</p>
          <p><strong>Bot:</strong> {{ msg.answer }}</p>
        </div>
      </div>

      <div v-if="loading" class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>

      <div class="input-section">
        <input v-model="message" placeholder="Введите вопрос" />
        <button @click="sendMessage" :disabled="loading || !message.trim()">
          {{ loading ? "Ждём ответ..." : "Отправить" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      message: "",
      response: "",
      fileUploaded: false,
      loading: false,
      progress: 0,
      messages: [],
    };
  },
  methods: {
    async uploadFile(e) {
      const file = e.target.files[0];
      if (!file) return;
      if (file.size > 5 * 1024 * 1024) {
        alert("Файл слишком большой, максимум 5 МБ");
        return;
      }
      const form = new FormData();
      form.append("file", file);
      try {
        const res = await axios.post("http://localhost:8000/upload", form);
        if (res.data.status === "Файл загружен") {
          this.fileUploaded = true;
        } else {
          alert("Ошибка: сервер не принял файл.");
        }
      } catch (err) {
        console.error("Ошибка загрузки файла:", err);
        alert("Ошибка при загрузке файла");
      }
    },

    async sendMessage() {
      if (!this.message.trim()) return;
      this.loading = true;
      this.progress = 0;
      const progressInterval = setInterval(() => {
        if (this.progress < 90) {
          this.progress += 1;
        }
      }, 100);

      try {
        const res = await axios.post("http://localhost:8000/chat", {
          message: this.message,
        });
        clearInterval(progressInterval);
        this.progress = 100;
        this.messages.push({ question: this.message, answer: res.data.response });
        this.message = "";
      } catch (err) {
        clearInterval(progressInterval);
        console.error("Ошибка запроса:", err);
        alert("Ошибка при запросе к серверу");
      } finally {
        setTimeout(() => {
          this.progress = 0;
          this.loading = false;
        }, 300);
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 1rem;
  background-color: #1e1e1e;
  border-radius: 8px;
  color: white;
  font-family: sans-serif;
}
.chat-title {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #3b82f6;
}
.upload-section {
  margin-bottom: 1rem;
  text-align: center;
}
.custom-file-upload {
  display: inline-block;
  padding: 0.5rem 1rem;
  cursor: pointer;
  background-color: #2563eb;
  color: white;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
.custom-file-upload:hover {
  background-color: #1d4ed8;
}
.custom-file-upload input {
  display: none;
}
.status {
  margin-top: 0.5rem;
  color: #6ee7b7;
}
.chat-box {
  border-top: 1px solid #333;
  padding-top: 1rem;
}
.messages {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1rem;
}
.message {
  margin-bottom: 1rem;
  background-color: #2c2c2c;
  padding: 0.5rem;
  border-radius: 4px;
}
.input-section {
  display: flex;
  gap: 0.5rem;
  flex-direction: column;
}
input[type="file"] {
  color: white;
}
input[type="text"], input[v-model] {
  flex: 1;
  padding: 0.5rem;
  border-radius: 4px;
  border: none;
}
button {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #3b82f6;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #555;
  cursor: not-allowed;
}
.progress-bar-container {
  height: 8px;
  background-color: #333;
  border-radius: 4px;
  margin-bottom: 1rem;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background-color: #3b82f6;
  width: 0%;
  transition: width 0.3s ease;
}


</style>
