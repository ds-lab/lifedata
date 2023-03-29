FROM node:14

WORKDIR /app

ADD package.json /app/package.json
ADD yarn.lock /app/yarn.lock

RUN yarn install

COPY ./ /app

# Make it configurable if the JS bundles are build during image build.
ARG BUILD_BUNDLE=1
ARG API_URL
ENV REACT_APP_API_URL=${API_URL}

RUN test ${BUILD_BUNDLE} -eq 1 && yarn build || echo "skipping build"
RUN test ${BUILD_BUNDLE} -eq 1 && yarn build-storybook || echo "skipping build"

ENV PORT 3000
EXPOSE 3000

CMD ["yarn", "serve"]
