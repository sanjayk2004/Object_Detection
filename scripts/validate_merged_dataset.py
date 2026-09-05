"""
validate_merged_dataset.py
Validates the merged 8-class dataset: checks for missing files, invalid
class ids, out-of-range coordinates, empty labels, and reports class
distribution per split and overall.
"""

import os

DATASET_DIR = "dataset"
SPLITS = ["train", "valid", "test"]
NUM_CLASSES = 7
CLASS_NAMES = ["person", "bottle", "cellphone", "laptop", "chair", "pen", "pencil"]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def main():
    issues = []
    overall_class_counts = {i: 0 for i in range(NUM_CLASSES)}
    split_stats = {}

    for split in SPLITS:
        img_dir = os.path.join(DATASET_DIR, split, "images")
        lbl_dir = os.path.join(DATASET_DIR, split, "labels")

        if not os.path.exists(img_dir) or not os.path.exists(lbl_dir):
            issues.append(f"[{split}] missing images/ or labels/ folder entirely")
            continue

        img_files = {os.path.splitext(f)[0]: f for f in os.listdir(img_dir)}
        lbl_files = {os.path.splitext(f)[0]: f for f in os.listdir(lbl_dir) if f.endswith(".txt")}

        images_without_labels = set(img_files) - set(lbl_files)
        labels_without_images = set(lbl_files) - set(img_files)

        empty_labels = 0
        class_counts = {i: 0 for i in range(NUM_CLASSES)}
        total_annotations = 0

        for idx, (base, lbl_file) in enumerate(lbl_files.items()):
            if idx % 2000 == 0:
                print(f"  [{split}] checked {idx}/{len(lbl_files)} label files...")
            path = os.path.join(lbl_dir, lbl_file)
            with open(path, "r") as f:
                lines = [l.strip() for l in f if l.strip()]

            if not lines:
                empty_labels += 1
                continue

            for line in lines:
                parts = line.split()
                if len(parts) != 5:
                    issues.append(f"[{split}] {lbl_file}: malformed line (expected 5 values): '{line}'")
                    continue

                cls_id = int(parts[0])
                if cls_id < 0 or cls_id >= NUM_CLASSES:
                    issues.append(f"[{split}] {lbl_file}: invalid class id {cls_id}")
                    continue

                coords = [float(p) for p in parts[1:]]
                if any(c < 0 or c > 1 for c in coords):
                    issues.append(f"[{split}] {lbl_file}: coordinate out of [0,1] range: {coords}")
                    continue

                class_counts[cls_id] += 1
                overall_class_counts[cls_id] += 1
                total_annotations += 1

        split_stats[split] = {
            "images": len(img_files),
            "labels": len(lbl_files),
            "annotations": total_annotations,
            "empty_labels": empty_labels,
            "images_without_labels": len(images_without_labels),
            "labels_without_images": len(labels_without_images),
            "class_counts": class_counts,
        }

        if images_without_labels:
            issues.append(f"[{split}] {len(images_without_labels)} images have no matching label file")
        if labels_without_images:
            issues.append(f"[{split}] {len(labels_without_images)} labels have no matching image file")

    print("=" * 70)
    print("MERGED DATASET VALIDATION REPORT")
    print("=" * 70)

    for split in SPLITS:
        if split not in split_stats:
            continue
        s = split_stats[split]
        print(f"\n--- {split.upper()} ---")
        print(f"Images: {s['images']}")
        print(f"Labels: {s['labels']}")
        print(f"Annotations: {s['annotations']}")
        print(f"Empty label files: {s['empty_labels']}")
        print(f"Images without labels: {s['images_without_labels']}")
        print(f"Labels without images: {s['labels_without_images']}")

    print("\n" + "=" * 70)
    print("CLASS DISTRIBUTION (all splits combined)")
    print("=" * 70)
    for i in range(NUM_CLASSES):
        print(f"  {i} ({CLASS_NAMES[i]:<10}): {overall_class_counts[i]}")

    print("\n" + "=" * 70)
    print(f"TOTAL ISSUES FOUND: {len(issues)}")
    print("=" * 70)
    if issues:
        for issue in issues[:50]:
            print(f"  - {issue}")
        if len(issues) > 50:
            print(f"  ... and {len(issues) - 50} more issues (truncated)")
    else:
        print("No issues found. Dataset looks structurally valid.")


if __name__ == "__main__":
    main()