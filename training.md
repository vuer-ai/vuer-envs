# Training Pipeline

## Environments exist in 

```lucidxr_base/tasks/ur5_basic.py```

## To generate images:

Run ```lucidxr_base/specs/test_augment_render.py``` with the proper arguments

## To generate hdf5 files for training:

Run ```lucidxr_base/specs/dataset_convert_remote.py``` with the proper arguments

## Download the hdf5 files 

Upload them to the proper location

### Add the following to .ssh/config file:
```markdown
Host escher
  HostName escher.csail.mit.edu
  RequestTTY yes
  Port 22
  User ubuntu
  IdentityFile ~/.ssh/csail-openstack
  LocalForward 7379 localhost:6379
```

### Run the following
```bash
rsync -a --info=progress2 escher:"runs-new/<dataset_prefix>/*hdf5" temp/
rsync -a --info=progress2 temp/*hdf5 geyang@tig-slurm.csail.mit.edu:/data/scratch/geyang/yajjy_demo/<unique_dataset_name>/
```

Replace the h5py.File paths in ```ACT/utils.py``` with the proper dataset name

## To train the model:

Run ```lucidxr_base/train/launch_train.py``` with the proper arguments

## To unroll the model:

Run ```lucidxr_base/specs/test_default_unroll.py``` with the proper arguments