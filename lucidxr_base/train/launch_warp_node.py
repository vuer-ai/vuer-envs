"""


from zaku import TaskQ
queue = TaskQ(name="lucidsim:eval-worker-queue-1", uri="http://escher.csail.mit.edu:8100")
queue.clear_queue()

for i in range(10):
    deps = {"$kill": True}
    queue.add(deps)

queue.clear_queue()

"""

from ml_logger.job import instr

machines = [
    # dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=0),
    # dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=1),
    # dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=2),
    # dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=3),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=0),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=1),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=2),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=3),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=4),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=5),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=6),
    dict(ip="isola-v100-2.csail.mit.edu", gpu_id=7),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=0),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=1),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=2),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=3),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=0),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=1),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=2),
    # dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=3),
]

if __name__ == "__main__":
    import jaynes
    from lucidsim.traj_samplers.worker_nodes.warp_node import entrypoint

    for machine in machines:
        host = machine["ip"]
        visible_devices = f'{machine["gpu_id"]}'

        envs = f"CUDA_VISIBLE_DEVICES={visible_devices} MUJOCO_EGL_DEVICE_ID={visible_devices}"
        jaynes.config(
            launch=dict(ip=host),
            runner=dict(
                envs=envs,
                # shell="screen -dm /bin/bash --norc",
            ),
        )

        thunk = instr(entrypoint)
        jaynes.add(thunk)

    jaynes.execute()
    jaynes.listen()
