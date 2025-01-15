# Program do przekształceń morfologicznych obrazów binarnych
Zaimplementowane funkcjonalności:
- wczytywanie i zapis obrazów na dysk
- operacje morfologiczne takie jak: dylacja, erozja, otwarcie, zamknięcie z różnymi wielkościami elementu strukturalnego
- operacja hit-or-miss z możliwością wyboru własnego wzoru elementu strukturalnego (szary = cokolwiek, biały = 1, czarny = 0)
- łączenie kilku przekształconych obrazów w jeden (operacja logiczna OR)
- możliwość cofania i historia dokonanych przekształceń
- zamiana obrazu kolorowego na binarny przy użyciu segmentacji

## Użycie
```bash
git clone https://github.com/KwiatkM/TEM
cd TEM
pip install -r requirements.txt
python app.py
```

# Przykłady
![Binary image processing example](example1.png)
![Image conversion form color to binary example](example2.png)
