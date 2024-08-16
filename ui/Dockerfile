FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18 AS runtime
WORKDIR /app
COPY --from=build /app/.nuxt ./.nuxt
COPY --from=build /app/.output ./.output
COPY --from=build /app/assets ./assets
ENV HOST 0.0.0.0
EXPOSE 3000
CMD [ "node", ".output/server/index.mjs"]