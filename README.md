# Selective Editor

## How to use 

```
pip install git+https://github.com/facebookresearch/sam2.git
pip install git+https://github.com/not-lain/selective-editor.git
```

```python
from selective_editor import get_app

app = get_app()
app.launch()
```

## Pipeline

```mermaid
graph TD
    A[Launch app] --> B[upload image];
    C -->|reset mask| F[in case you want to reslect your mask from scratch];
    F --> |initial state| C;
    B -->|click to select image mask| C[you can select included points and for complex objects you can exclude certain areas];
    C -->|inpaint image| D[describe what you want to create and press inpaint];
    D --> E[download final image];
```

## Example

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="assets/baseline.png" style="height: 150px; width: auto;" />
    <img src="assets/segmented.png" style="height: 150px; width: auto;" />
    <img src="assets/red car.png" style="height: 150px; width: auto;" />
</div>