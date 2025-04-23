import yaml
import requests
import soundfile as sf
from IPython.display import Audio, display
import io

class VoiceChanger:
    def __init__(self, config_path="configs/voice_changer_config.yaml"):
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        api_key = config.get("api_key")
        if api_key:
            if "headers" not in config:
                config["headers"] = {}
            config["headers"]["Authorization"] = f"Bearer {api_key}"
        
        return config

    def change_voice(self, input_audio_path):
        url = self.config["api_url"]
        headers = self.config.get("headers", {})
        payload = self.config.get("payload", {})

        with open(input_audio_path, "rb") as audio_file:
            files = {"clip": audio_file}
            response = requests.post(url, data=payload, files=files, headers=headers)
        
        if response.status_code != 200:
            raise RuntimeError(f"Voice change failed: {response.status_code} — {response.text}")
        
        return response.content

    def save_audio(self, audio_changed, output_audio_path):
        with open(output_audio_path, "wb") as f:
            f.write(audio_changed)

    def play_audio(self, audio_path):
        audio, samplerate = sf.read(audio_path)
        display(Audio(audio, rate=samplerate))


    def run_pipeline(self, input_audio_path, output_audio_path):
        audio_changed = self.change_voice(input_audio_path)
        self.save_audio(audio_changed, output_audio_path)
        print("✅ Voice transformation successful.")
        self.play_audio(output_audio_path)

        
