# ofo. - Online Freizeit Organisator

## 5-Minute-Setup

```
# clone repo
git clone https://github.com/herzog-ch/online-freizeit-organisator.git

# build a Docker image
docker build -t ofo_django_app_image .

# run a Docker container
docker run -p 8000:8000 -i -t ofo_django_app_image
```

Open Chrome Browser: http://localhost:8000