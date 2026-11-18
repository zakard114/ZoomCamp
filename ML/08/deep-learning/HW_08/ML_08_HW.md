# ML Zoomcamp 2026 — Homework 8: Neural Networks and Deep Learning

Notebook: [`ML_HW08.ipynb`](./ML_HW08.ipynb)

---

## Form answers

| # | Answer |
|---|--------|
| 1 | **nn.BCEWithLogitsLoss()** |
| 2 | **20073473** |
| 3 | **0.81** |
| 4 | **0.139** |
| 5 | **0.575** |
| 6 | **0.72** |

---

## Setup

Ran locally on CPU with this folder's `.venv` (`torch==2.9.0+cpu`, `torchvision==0.24.0+cpu`). Seed `42` before the datasets, loaders, model, and optimizer. `num_workers=0`. `torch.set_num_threads(2)`.

- Data: `data/` from `straight-curly-data/data.zip` (800 train, 201 held-out). `ImageFolder` maps `curly=0`, `straight=1`.
- Histories: `history_baseline.json`, `history_augmented.json` (four lists each).
- Kernel: this folder `.venv`. Do not use `!pip` / `!wget`.

---

## Dataset

Fixed archive. Do not make another random split. Do not augment the held-out images.

| Split | Curly | Straight | Total |
| --- | ---: | ---: | ---: |
| Train | 410 | 390 | 800 |
| Held-out evaluation | 103 | 98 | 201 |

Shared evaluation transform: resize to 200×200 (bilinear), `ToTensor`, ImageNet normalize.

```python
len(train_dataset), len(evaluation_dataset), train_dataset.class_to_idx
```

**Output:**

```text
800 201 {'curly': 0, 'straight': 1}
```

---

## Q1 — Loss and output contract

**Question:** Which loss matches a model that returns one logit?

- `nn.MSELoss()`
- `nn.BCEWithLogitsLoss()`
- `nn.CrossEntropyLoss()`
- `nn.CosineEmbeddingLoss()`

```python
dummy_logits = model(torch.zeros((2, 3, 200, 200), device=device))
print(tuple(dummy_logits.shape))
print(type(criterion).__name__)
```

**Output:**

```text
(2, 1)
BCEWithLogitsLoss
```

**Answer:** **nn.BCEWithLogitsLoss()**

---

## Q2 — Parameter count

**Question:** Total trainable parameters, biases included.

- `896`
- `11214912`
- `15896912`
- `20073473`

```python
sum(p.numel() for p in model.parameters())
```

**Output:**

```text
20073473
```

**Answer:** **20073473**

---

## Q3 — Baseline accuracy

**Question:** Train 10 epochs with the baseline transform. Median of `train_accuracy`, two decimal places.

```python
history_baseline = run_phase(model, train_loader, evaluation_loader, optimizer)
round(float(np.median(history_baseline["train_accuracy"])), 2)
```

**Output:**

```text
Median of train accuracy: 0.81
```

Train accuracies: 0.645, 0.7175, 0.755, 0.79125, 0.80875, 0.8075, 0.83625, 0.885, 0.91, 0.93875.

**Answer:** **0.81**

---

## Q4 — Baseline loss

**Question:** Population standard deviation of `train_loss` (`np.std(..., ddof=0)`), three decimal places.

```python
round(float(np.std(history_baseline["train_loss"], ddof=0)), 3)
```

**Output:**

```text
Population std of train loss: 0.139
```

**Answer:** **0.139**

---

## Q5 — Augmented evaluation loss

**Question:** Keep the same model and optimizer. Train 10 more epochs with rotation 50 (nearest), `RandomResizedCrop`, and horizontal flip. Mean of `evaluation_loss`, three decimal places.

```python
history_augmented = run_phase(model, train_loader_aug, evaluation_loader, optimizer)
round(float(np.mean(history_augmented["evaluation_loss"])), 3)
```

The second loader uses `manual_seed(43)`. The held-out loader is unchanged.

**Output:**

```text
Mean of evaluation loss: 0.575
```

**Answer:** **0.575**

---

## Q6 — Augmented evaluation accuracy

**Question:** Mean of the last five `evaluation_accuracy` values (augmented epochs 6–10), two decimal places.

```python
round(float(np.mean(history_augmented["evaluation_accuracy"][-5:])), 2)
```

Last five: 0.7015, 0.7413, 0.7114, 0.7363, 0.7313.

**Output:**

```text
Mean of last five evaluation accuracies: 0.72
```

**Answer:** **0.72**

---

## Learning in Public

Share a short post with `#mlzoomcamp` (no secrets). Submit the post link with the homework.

**Post link:**

---

Numeric answers use the precision stated in each question. The grader allows absolute error 0.05 on the accuracy questions and 0.02 on the loss questions.
