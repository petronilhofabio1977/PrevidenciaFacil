FROM node:20-alpine

WORKDIR /app

# Copiar arquivos de configuração primeiro
COPY frontend/package*.json ./

# Instalar dependências
RUN npm install

# Copiar o resto do código
COPY frontend/ .

# Expor porta
EXPOSE 3000

# Rodar em modo desenvolvimento (sem build)
CMD ["npm", "run", "dev"]
