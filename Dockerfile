FROM node:24-alpine
ENV NODE_ENV=production
ENV PORT=8080
WORKDIR /app
COPY --chown=node:node package.json server.mjs ./
COPY --chown=node:node dist/ ./dist/
USER node
EXPOSE 8080
CMD ["node", "server.mjs"]
