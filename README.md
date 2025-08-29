# cycheng CRF Evaluation Tool

A Python 3 tool for evaluating CRF (Conditional Random Field) test results with confusion matrix analysis, precision, recall, and F1-score calculations.

## Features

- **Confusion Matrix Analysis**: Generate and display confusion matrices for CRF test results
- **Performance Metrics**: Calculate precision, recall, F1-score, and accuracy for each label
- **Unit Testing Support**: Comprehensive test suite with high code coverage
- **Prediction Analysis**: Save correct and incorrect predictions to separate files
- **Python 3 Compatible**: Modern Python 3 codebase with type hints
- **Clean Architecture**: Well-structured, modular design for easy maintenance

## Installation

### From Source
```bash
git clone <repository-url>
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

## Migration from v1.x

The new version provides a cleaner API. Here's how to migrate:

### Old Code (v1.x)
```python
from crf_confusion_matrix_class import crf_confusion_matrix_class

test = crf_confusion_matrix_class(correct_label_pool, filename)
test.confusion_matrix_print_func()
```

### New Code (v2.x)
```python
from crf_evaluator import CRFEvaluator

evaluator = CRFEvaluator(correct_label_pool, filename)
evaluator.print_confusion_matrix()
evaluator.print_metrics()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Requirements

- Python 3.7+
- No external dependencies for core functionality

## License

MIT License

## References

- CRF++: Yet Another CRF toolkit [(https://taku910.github.io/crfpp/)](https://taku910.github.io/crfpp/)

## Changelog

### v2.0.0 (Vibe Coding w/ Copilot+Claude4)
- Complete rewrite for Python 3
- Added comprehensive unit tests
- Improved error handling and validation
- Added type hints
- Cleaner, more maintainable architecture
- Better documentation

### v1.x
- Original Python 2 implementation