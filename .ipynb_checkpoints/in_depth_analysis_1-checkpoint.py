import matplotlib.pyplot as plt
import pandas as pd

for i, (pred, gold1, gold2) in enumerate(zip(silver_data_list, annotator1_results, annotator2_results)):
    if pred != gold1 and pred != gold2:
        print(f"Index {i}: Silver = {pred}, Annotator 1 = {gold1}, Annotator 2 = {gold2}")

# Load results
df = pd.read_csv("results.csv", sep=";")  # Try semicolon


# Count occurrences of each class in gold and silver
gold_counts = df['labels1'].value_counts().sort_index()
silver_counts = df['labels2'].value_counts().sort_index()

# Combine into a DataFrame
comparison_df = pd.DataFrame({
    'Gold': gold_counts,
    'Silver': silver_counts
}).fillna(0).astype(int)

# Plot side-by-side bar chart
ax = comparison_df.plot(kind='bar', figsize=(6, 6), width=0.8)
plt.title("Class Distribution: Gold vs Silver")
plt.xlabel("Class Label")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("class_distribution.png", dpi=300)
plt.show()

# Assumes labels1 = gold, labels2 = silver
df = pd.read_csv("results.csv", sep=";")  # Or your working version

# Missed ORG
missed_org = df[(df['labels1'] == 'ORG') & (df['labels2'] != 'ORG')]

# Hallucinated ORG (predicted ORG where it shouldn't be)
hallucinated_org = df[(df['labels1'] != 'ORG') & (df['labels2'] == 'ORG')]

# Misclassified ORG (could be either direction)
misclassified_org = df[(df['labels1'] == 'ORG') & (df['labels2'] != 'ORG')]

# Drop rows with missing labels
df_clean = df.dropna(subset=['labels1', 'labels2'])

# Extract gold and silver labels
y_true = df_clean['labels1']
y_pred = df_clean['labels2']

# Get consistent set of labels
labels = sorted(set(y_true) | set(y_pred))

# Now safely compute and display the confusion matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

cm = confusion_matrix(y_true, y_pred, labels=labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(xticks_rotation=45, cmap='Reds')
plt.title("Confusion Matrix: Silver vs Gold")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=300)
plt.show()
