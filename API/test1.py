import requests

url = "https://dog.ceo/api/breeds/image/random"

res = requests.get(url)

print("=" * 100)
print("=" * 100)
print(f">>>>>>>>>>>>>>>>>>>{res.json()["message"]}<<<<<<<<<<<<<<<<<<")  # Link da imagem
print(f">>>>>>>>>>>>>>>>>>>{res.json()["message"]}<<<<<<<<<<<<<<<<<<")  # Link da imagem
print(f">>>>>>>>>>>>>>>>>>>{res.json()["message"]}<<<<<<<<<<<<<<<<<<")  # Link da imagem
print(f">>>>>>>>>>>>>>>>>>>{res.json()["message"]}<<<<<<<<<<<<<<<<<<")  # Link da imagem
print(f">>>>>>>>>>>>>>>>>>>{res.json()["message"]}<<<<<<<<<<<<<<<<<<")  # Link da imagem
print("=" * 100)
print("=" * 100)
