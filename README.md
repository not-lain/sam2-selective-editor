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

## Example

```mermaid
graph TD
    A[Launch app] -->|upload image| B[<img src='https://github.com/not-lain/selective-editor/blob/update-readme/assets/baseline.png?raw=true' width='40' height='40'/>]
    B -->|click to select image mask| C[<img src='https://github.com/not-lain/selective-editor/blob/update-readme/assets/segmented.png?raw=true' width='40' height='40'/>]
    C -->|inpaint image| D[<img src='https://github.com/not-lain/selective-editor/blob/update-readme/assets/red%20car.png?raw=true' width='40' height='40'/>]
```