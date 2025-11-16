# Deterministic vs. Randomized Quicksort (Python)

This repository contains Python implementations of deterministic and randomized Quicksort, along with a detailed APA-style report analyzing their design, implementation, and time complexity. Benchmarking utilities and instructions for running the code are also included.

## Repository Contents

- `quicksort.py` — Implementation of deterministic and randomized Quicksort, plus benchmarking tools.
- `Quicksort_Report.docx` — Full APA-style report.
- `README.md` — Instructions and summary.

## How to Run the Code

Clone the repository:

```
git clone <your_repository_url>
cd <repository_name>
```

Run benchmark (default 10,000 elements):

```
python quicksort.py
```

Custom size:

```
python quicksort.py --size 50000
```

## Benchmark Details

Script generates:
- Random array
- Sorted array
- Reverse-sorted array

Then runs:
- Deterministic Quicksort
- Randomized Quicksort

Outputs time + correctness.

## Findings Summary

### Deterministic Quicksort
- Pivot = last element  
- Fast on random arrays  
- Worst-case Θ(n²) on sorted/reverse-sorted  
- Input sensitive  

### Randomized Quicksort
- Random pivot  
- Expected Θ(n log n) for all inputs  
- Avoids worst-case behavior  
- Stable in practice  

## Full Report
See **Quicksort_Report.docx** for full APA analysis.

