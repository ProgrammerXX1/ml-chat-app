<template>
  <div class="chat">
    <div v-for="(msg, index) in messages" :key="index" class="message">
      <p><strong>You:</strong> {{ msg.user }}</p>
      <p><strong>Bot:</strong> {{ msg.bot }}</p>
    </div>

    <input
      v-model="userInput"
      @keydown.enter="sendMessage"
      placeholder="Type your message..."
    />
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const userInput = ref('')
const messages = ref<{ user: string; bot: string }[]>([])

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const currentMessage = userInput.value
  userInput.value = ''

  try {
    const res = await axios.post('http://localhost:8000/chat', {
      message: currentMessage,
    })

    messages.value.push({
      user: currentMessage,
      bot: res.data.response,
    })
  } catch (err) {
    messages.value.push({
      user: currentMessage,
      bot: 'Error contacting backend',
    })
  }
}
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
