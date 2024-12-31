import os
import shutil

from vuer_envs.scripts.util.prune import remove_unused_mesh
from vuer_envs.scripts.util.mjcf_asset_paths_extractor import get_asset_paths_from_mjcf


def move_assets_to_scene(asset_paths, scene_file, scene_root):
    """
    Moves a scene file and associated assets to a new root folder while preserving their structure.

    Args:
    asset_paths (list): List of asset file paths to be moved.
    scene_file (str): Path to the scene file to be moved.
    scene_root (str): Path to the new root folder (e.g., 'scene_0001').

    """
    if not os.path.exists(scene_root):
        os.makedirs(scene_root)

    # Move and rename the scene file to 'mjcf.xml'
    if os.path.isabs(scene_file):
        scene_file_abs = scene_file
    else:
        scene_file_abs = os.path.abspath(scene_file)

    # Rename the scene file to 'mjcf.xml' in the destination
    # scene_destination = os.path.join(scene_root, "scene.mjcf.xml")
    # shutil.copy2(scene_file_abs, scene_destination)
    # print(f"Moved and renamed: {scene_file_abs} -> {scene_destination}")

    # Move each asset
    for asset_path in asset_paths:
        if not os.path.isabs(asset_path):
            asset_path = os.path.abspath(asset_path)

        relative_path = os.path.relpath(asset_path)

        # Create the new destination path under scene_root
        destination_path = os.path.join(scene_root, relative_path)
        destination_dir = os.path.dirname(destination_path)

        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        shutil.copy2(asset_path, destination_path)
        print(f"Moved: {asset_path} -> {destination_path}")


if __name__ == "__main__":

    # Destination folder for the scene and assets
    new_scene_folder = "scene0001"

    # Path to the scene file
    scene_file_path = "../../assets/robocasa_scenes_staging/layout0001-style0001.xml"
    new_scene_file = os.path.join(new_scene_folder, "scene.mjcf.xml")

    remove_unused_mesh(scene_file_path, to=new_scene_file)

    # Dynamically extract the asset file paths from the MJCF scene file
    asset_files = get_asset_paths_from_mjcf(new_scene_file)

    # Move the scene file (as 'mjcf.xml') and associated assets
    move_assets_to_scene(asset_files, new_scene_file, new_scene_folder)