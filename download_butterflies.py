from pathlib import Path
import json,hashlib,urllib.request,shutil
root=Path(__file__).resolve().parent
source=json.loads((root/"data/butterfly_source.json").read_text())
target=root/"data/butterfly.zip"
if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==source["archive_sha256"]:
    print("Архив уже загружен и проверен.")
else:
    temporary=target.with_suffix(".zip.part")
    print("Загрузка архива около 237 МБ...")
    with urllib.request.urlopen(source["download_url"],timeout=180) as response, temporary.open("wb") as out:
        shutil.copyfileobj(response,out)
    digest=hashlib.sha256(temporary.read_bytes()).hexdigest()
    if digest!=source["archive_sha256"]:
        raise RuntimeError("Kaggle вернул другую версию архива. Проверьте набор; файл .part сохранён.")
    temporary.replace(target)
    print("Архив загружен, SHA-256 совпала.")
