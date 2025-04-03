FROM python:3.12 as builder

ARG CDN_DOMAIN_PROD
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG BUCKET_STATIC_FILES
ARG AWS_REGION

COPY /requirements.txt /src/requirements.txt

ENV APP_DIR='/src'
WORKDIR $APP_DIR

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --compile -r requirements.txt

RUN pip install --no-cache-dir django-storages boto3

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

COPY ./ $APP_DIR/.
COPY ./api_core $APP_DIR/api_core
COPY ./apps $APP_DIR/apps
COPY ./utils $APP_DIR/utils
COPY temp.env $APP_DIR/.env 
#acima, comando para trazer a env do secret manager
ENV CDN_DOMAIN_PROD=$CDN_DOMAIN_PROD \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    BUCKET_STATIC_FILES=$BUCKET_STATIC_FILES \
    AWS_REGION=$AWS_REGION

RUN chmod +x $APP_DIR/start_server.sh

EXPOSE 8000
CMD ["./start_server.sh"]