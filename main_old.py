
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from price import calculate_price

if __name__ == "__main__":
    kaina = 45.0
    kiekis = 42
    suma = calculate_price(kaina, kiekis)
    print(f"Rezultatas: {kiekis} m² × {kaina} EUR = {suma} EUR")