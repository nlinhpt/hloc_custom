import argparse
import collections.abc as collections
from pathlib import Path
from typing import List, Optional, Union

from . import logger
from .utils.io import list_h5_names
from .utils.parsers import parse_image_lists


def main(
    output: Path,
    image_list: Optional[Union[Path, List[str]]] = None,
    features: Optional[Path] = None,
    overlap: int = 10,
):
    window_size = overlap # Number of subsequent frames to pair with each image
    
    # ==================================================
    # Read image names
    # ==================================================
    if image_list is not None:
        if isinstance(image_list, (str, Path)):
            names = parse_image_lists(image_list)
        elif isinstance(image_list, collections.Iterable):
            names = list(image_list)
        else:
            raise ValueError(f"Unknown image list type: {image_list}")
    elif features is not None:
        names = list_h5_names(features)
    else:
        raise ValueError("Provide image_list or features.")

    # ==================================================
    # Generate sequential pairs
    # ==================================================
    pairs = []
    num_images = len(names)

    for i in range(num_images):
        start_j = i + 1
        end_j = min(i + window_size + 1, num_images)
        for j in range(start_j, end_j):
            pairs.append((names[i], names[j]))

    # ==================================================
    # Save pairs
    # ==================================================
    logger.info(
        f"Found {len(pairs)} sequential pairs (window_size={window_size})"
    )

    with open(output, "w") as f:
        f.write("\n".join(" ".join([i, j]) for i, j in pairs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--image_list", type=Path)
    parser.add_argument("--features", type=Path)
    parser.add_argument("--overlap", type=int, default=5) # change window size here
    
    args = parser.parse_args()
    main(**args.__dict__)