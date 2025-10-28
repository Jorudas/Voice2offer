
import whisper

# Pakraunamas modelis
model = whisper.load_model("large-v3")   # buvęs "base" -> "large-v3"

# Nurodome tavo garso failo vietą (su dvigubais backslash)
audio_path = r"C:\1 JORUDAS\DOC Jorudas\AI\PROJEKTAI\Voice2offer\src\data\audio2.wav"

# Atpažįstame kalbą
result = model.transcribe(audio_path, language="lt")

print("Atpažintas tekstas:")
print(result["text"])