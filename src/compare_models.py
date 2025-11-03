
import matplotlib.pyplot as plt

# Įvesk čia savo faktinius rezultatus iš ankstesnių paleidimų
ml_accuracy = 0.9   # iš ml_train.py
nn_accuracy = 0.9   # iš nn_train.py

# Sukuriam bar chart
models = ['ML Modelis', 'Neuroninis tinklas']
accuracies = [ml_accuracy, nn_accuracy]

plt.bar(models, accuracies, color=['skyblue', 'lightgreen'])
plt.ylim(0, 1)
plt.title('ML vs NN tikslumo palyginimas')
plt.ylabel('Tikslumas (accuracy)')
plt.xlabel('Modeliai')

# Įrašom reikšmes virš stulpelių
for i, acc in enumerate(accuracies):
    plt.text(i, acc + 0.02, f"{acc:.2f}", ha='center', fontsize=11)

plt.tight_layout()
plt.show()

# Tekstinė išvada
if nn_accuracy > ml_accuracy:
    diff = (nn_accuracy - ml_accuracy) * 100
    print(f"Neuroninis tinklas tikslesnis maždaug {diff:.1f}% nei klasikinis ML modelis.")
elif nn_accuracy < ml_accuracy:
    diff = (ml_accuracy - nn_accuracy) * 100
    print(f"Klasikinis ML modelis tikslesnis maždaug {diff:.1f}% nei neuroninis tinklas.")
else:
    print("Abu modeliai pasiekė tą patį tikslumą.")