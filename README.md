# Image_Proc_Metrics
## This is to evaluate how good the segmentation is for binary images
### The metrics.py calculates the following metrics
### accuracy, precision, sensitivity, specificity, mcc, dice, jaccard

## The code also plots the overlapped ground truth and segmented image and draws contours
### 0 = black = not segmented and 255 = white = segmented

# Run the following
```bash 
pip install --upgrade pip
pip install Pillow
rm metrics.csv && touch metrics.csv
mkdir -p Overlapped
python metrics.py
```
