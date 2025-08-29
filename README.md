# cycheng CRF Evaluation Tool

- A Python 3 tool for evaluating CRF (Conditional Random Field) test results with confusion matrix analysis, precision, recall, and F1-score calculations.
- Generate and display confusion matrices (precision, recall, F1-score, and accuracy) for CRF test results

## Installation

### From Source
```bash
git clone git@github.com:bryanyuan2/cycheng-crf-evaluation-tool.git
cd crf-evaluation-tool
pip install -r requirements.txt
```

### Development Setup
```bash
pip install -r requirements-dev.txt
```

## Usage

### Basic Usage

```python
from crf_evaluator import CRFEvaluator

# Define your label set
labels = ["I-NP", "B-NP", "B-ADJP", "I-ADJP"]

# Create evaluator and load data
evaluator = CRFEvaluator(labels, "path/to/crf_test_result.txt")

# Print confusion matrix and metrics
evaluator.print_confusion_matrix()
evaluator.print_metrics()

# Get metrics programmatically
metrics = evaluator.calculate_metrics()
print(f"Overall accuracy: {metrics['overall']['accuracy']:.4f}")
```

### Command Line Usage

```bash
python3 main.py
```

### Advanced Usage

```python
# Create evaluator without loading data
evaluator = CRFEvaluator(labels)

# Load data manually
evaluator.load_data_from_file("test_results.txt")

# Get 2D confusion matrix
matrix_2d = evaluator.get_confusion_matrix_2d()

# Save prediction analysis
evaluator.save_prediction_analysis("correct.txt", "wrong.txt")

# Get summary statistics
stats = evaluator.get_summary_stats()
```

## File Format

The tool expects CRF++ test result files with tab-separated values:
```
word    POS_tag    actual_label    predicted_label
John    NNP        B-PER          B-PER
Smith   NNP        I-PER          I-PER
...
```

## API Reference

### CRFEvaluator Class

#### Constructor
```python
CRFEvaluator(correct_labels: List[str], file_path: Optional[str] = None)
```

#### Methods
- `load_data_from_file(file_path: str)`: Load CRF test results from file
- `calculate_metrics()`: Calculate precision, recall, F1-score, and accuracy
- `print_confusion_matrix()`: Print formatted confusion matrix
- `print_metrics()`: Print performance metrics
- `get_confusion_matrix_2d()`: Get confusion matrix as 2D array
- `save_prediction_analysis()`: Save correct/incorrect predictions to files
- `get_summary_stats()`: Get summary statistics

## Example Output

```
====
Confusion Matrix
====
        I-NP    B-NP    B-ADJP  I-ADJP   [predicted class]
I-NP    5440    130     3       1
B-NP    420     4563    2       0
B-ADJP  30      47      48      2
I-ADJP  36      7       13      6
[actual class]

====
(Precision, Recall, F1 score)
====
I-NP = (0.917989, 0.975960, 0.946087)
B-NP = (0.961239, 0.915346, 0.937731)
B-ADJP = (0.727273, 0.377953, 0.497409)
I-ADJP = (0.666667, 0.096774, 0.169014)
Accuracy = 0.935709
```

## Requirements

- Python 3.7+

## References

- CRF++: Yet Another CRF toolkit [(https://taku910.github.io/crfpp/)](https://taku910.github.io/crfpp/)