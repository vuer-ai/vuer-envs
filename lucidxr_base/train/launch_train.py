from params_proto.hyper import Sweep

machines = [
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=3),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=0),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=1),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=2),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=3),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=4),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=5),
]

if __name__ == "__main__":
    import jaynes
    from ml_logger.job import instr
    from ACT.train import main

    machine = machines[0]

    jaynes.config()
    jaynes.run(main, dataset_prefix=[
        "lucidxr/lucidxr/datasets/lucidxr/poc/demos/pnp/data/universal_robots_ur5e/2025/01/18/23.48.11", ],
               vision_type="render_depth",
               local_load=False,
               load_checkpoint=None,
               camera_names=["table_pov", "overhead"],)

    # jaynes.execute()
    jaynes.listen(3000)
