EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True 
EMAIL_HOST = 'smtp.gmail.com' # service we use for email
EMAIL_HOST_USER = "demo.thoughts03@gmail.com"
EMAIL_HOST_PASSWORD = 'password' # This is the host mail password and we need add here
EMAIL_PORT = 587