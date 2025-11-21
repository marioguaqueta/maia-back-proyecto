# HerdNet Model Information

## Overview

This project uses **HerdNet**, a specialized deep learning architecture for detecting and counting animals in aerial imagery.

## About HerdNet

HerdNet is based on the research paper:

> **Delplanque, A., Foucher, S., Lejeune, P., & Linchant, J. (2023)**  
> *From crowd to herd counting: How to precisely detect and count African mammals using aerial imagery and deep learning?*  
> ISPRS Journal of Photogrammetry and Remote Sensing, 197, 167-180.  
> DOI: https://doi.org/10.1016/j.isprsjprs.2023.01.025

**GitHub Repository:** https://github.com/Alexandre-Delplanque/HerdNet

## Model Architecture

HerdNet is specifically designed for:
- **Multi-species detection** in aerial imagery
- **Object counting** with density estimation
- **High-resolution images** with automatic patching
- **Wildlife and livestock** monitoring from UAV/drone imagery

### Key Features

1. **Density-based Detection**: Uses Focal Inverse Distance Transform (FIDT) for precise localization
2. **Multi-scale Processing**: Handles images of varying sizes through patching
3. **Class-specific Counting**: Can distinguish between different animal species
4. **Aerial Imagery Optimization**: Trained on UAV nadir (top-down) imagery

## Model File Format

Your `herdnet_model.pth` file should contain:

```python
{
    'model': <state_dict>,          # Model weights
    'num_classes': <int>,           # Number of animal classes
    'down_ratio': <int>,            # Downsampling ratio (typically 2)
    'classes': {                    # Optional: Species labels
        0: 'no_animal',
        1: 'species_1',
        2: 'species_2',
        ...
    },
    'mean': [0.485, 0.456, 0.406], # Optional: Normalization mean
    'std': [0.229, 0.224, 0.225]    # Optional: Normalization std
}
```

## Training Your Own Model

If you want to train your own HerdNet model, refer to the official repository:

1. **Prepare your dataset** in CSV format with point annotations
2. **Create patches** from high-resolution images
3. **Train HerdNet** using the provided training scripts
4. **Export the model** with the correct format

See the [HerdNet documentation](https://github.com/Alexandre-Delplanque/HerdNet) for detailed training instructions.

## Supported Animal Classes

Default classes (adjust based on your trained model):

| Class ID | Animal Type   | Description                    |
|----------|---------------|--------------------------------|
| 0        | no_animal     | No animal detected             |
| 1        | cattle        | Cattle/Cows                    |
| 2        | horse         | Horses                         |
| 3        | sheep         | Sheep                          |
| 4        | goat          | Goats                          |
| 5        | pig           | Pigs                           |
| 6        | dog           | Dogs                           |
| 7        | cat           | Cats                           |
| 8        | wildlife      | Wild animals                   |
| 9        | bird          | Birds                          |
| 10       | other_animal  | Other types of animals         |

**Note:** Update the `ANIMAL_CLASSES` dictionary in `app.py` to match your specific model's output classes.

## Model Performance

HerdNet achieves:
- High precision in animal detection from aerial imagery
- Accurate counting even in crowded scenes
- Species-specific classification
- Robust performance across different lighting and terrain conditions

## Citation

If you use this code or the HerdNet model in your research, please cite:

```bibtex
@article{delplanque2023herdnet,
    title = {From crowd to herd counting: How to precisely detect and count African mammals using aerial imagery and deep learning?},
    journal = {ISPRS Journal of Photogrammetry and Remote Sensing},
    volume = {197},
    pages = {167-180},
    year = {2023},
    issn = {0924-2716},
    doi = {https://doi.org/10.1016/j.isprsjprs.2023.01.025},
    author = {Alexandre Delplanque and Samuel Foucher and Philippe Lejeune and Julie Linchant and Jérôme Théau}
}
```

## License

HerdNet is released under the MIT License. See the [LICENSE](https://github.com/Alexandre-Delplanque/HerdNet/blob/main/LICENSE.md) for details.

## Additional Resources

- **GitHub:** https://github.com/Alexandre-Delplanque/HerdNet
- **Colab Demo:** Available in the repository
- **Documentation:** See the HerdNet repository for detailed API documentation
- **Paper:** https://doi.org/10.1016/j.isprsjprs.2023.01.025

