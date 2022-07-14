text = "C:/Users/leekh/Downloads/val/99.jpg"

a = text.split('\\')[-1]
b = text.replace('/','\\', 100)
print(b)