from django.apps import AppConfig
from keras.models import load_model
import os

class WarfarinConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "warfarin"
    def ready(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        model_name = "model_20200228-02.h5"
        model_path = os.path.join(current_dir, model_name)

        WarfarinConfig.model = load_model(model_path)
