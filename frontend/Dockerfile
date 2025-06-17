FROM node:18

WORKDIR /app

# Копируем только нужные файлы
COPY package.json ./
COPY package-lock.json ./

# Устанавливаем зависимости без optional
RUN npm install --omit=optional

# Копируем весь код
COPY . .

# Запускаем Vite dev-сервер
CMD ["npm", "run", "dev"]
