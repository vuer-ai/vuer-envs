import os
import shutil
import yaml

from vuer_envs.scripts.util.mjcf_asset_paths_extractor import get_asset_paths_from_mjcf
from vuer_envs.scripts.util.prune import remove_unused_mesh
from vuer_envs.scripts.util.s3_file_upload_utils import upload_to_s3, upload_files_to_s3
from vuer_envs.scripts.util.working_directory_context_manager import WorkDir


def move_to(asset_paths: list, scene_root: str) -> list:
    """
    Moves a scene file and associated assets to a new root folder while preserving their structure.

    Args:
        asset_paths (list): List of asset file paths to be moved. Paths can be absolute or relative.
        scene_file (str): Path to the scene file to be moved. Can be absolute or relative.
        scene_root (str): Path to the new root folder (e.g., 'scene_0001'). Will be created if it doesn't exist.

    Returns:
        list: List of all files moved to their new locations.
    """
    os.makedirs(scene_root, exist_ok=True)

    # Rename the scene file to 'mjcf.xml' in the destination
    # scene_destination = os.path.join(scene_root, "scene.mjcf.xml")
    # shutil.copy2(scene_file_abs, scene_destination)
    # print(f"Moved and renamed: {scene_file_abs} -> {scene_destination}")

    moved_files = []

    # Move each asset
    for asset_path in asset_paths:
        if not os.path.isabs(asset_path):
            asset_path = os.path.abspath(asset_path)

        relative_path = os.path.relpath(asset_path)

        # Create the new destination path under scene_root
        destination_path = os.path.join(scene_root, relative_path)
        destination_dir = os.path.dirname(destination_path)

        # Ensure the destination directory exists
        os.makedirs(destination_dir, exist_ok=True)

        shutil.copy2(asset_path, destination_path)
        print(f"Moved: {asset_path} -> {destination_path}")

        moved_files.append(destination_path)

    return moved_files


if __name__ == "__main__":
    from params_proto import ParamsProto

    class Args(ParamsProto):
        wd = "../../assets"

        scene_name = "layout0001-style0001"
        entrypoint_name = "scene.vuer.yml"

        # Path to the scene file
        source_scene = f"robocasa_scenes_staging/{scene_name}.xml"

        # S3 target parths
        s3_bucket = "vuer-hub-production"
        s3_prefix = "robocasa-scenes"
        s3_entrypoint = f"{s3_prefix}/{entrypoint_name}"

        # Destination folder for the scene and assets
        local_prefix = f"outputs/{scene_name}"
        clean_mjcf = f"{local_prefix}/scene.mjcf.xml"
        local_asset_list = f"{local_prefix}/scene_files.txt"
        local_scene_file = f"{local_prefix}/{entrypoint_name}"

    # Clean the MJCF scene file by removing unused mesh elements, and
    # save to a new location
    remove_unused_mesh(Args.source_scene, to=Args.clean_mjcf)

    # Dynamically extract the asset file paths from the MJCF scene file
    source_list = get_asset_paths_from_mjcf(Args.clean_mjcf)

    with WorkDir(Args.wd):
        # Move the scene file (as 'mjcf.xml') and associated assets
        staged_list = move_to(source_list, Args.local_prefix)

        s3_list = upload_files_to_s3(
            [Args.clean_mjcf, *staged_list],
            Args.s3_bucket,
            Args.s3_prefix,
        )

        # Write the S3 file list to scene_files.txt
        with open(Args.local_asset_list, "w") as f:
            f.write("\n".join(s3_list))

        # Save the scene data in YAML format
        scene_data = {
            "tag": "Scene",
            "children": [
                {
                    "tag": "MuJoCo",
                    "src": s3_list[0],
                    "assets": s3_list,
                }
            ],
        }

        with open(Args.local_scene_file, "w") as f:
            yaml.dump(scene_data, f)  # noqa: F821

        s3_list = upload_to_s3(Args.local_scene_file, Args.s3_bucket, Args.s3_entrypoint)
