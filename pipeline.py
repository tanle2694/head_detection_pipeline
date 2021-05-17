import kfp.dsl as dsl
from utils import use_k8s_secret
from kubernetes import client as k8s_client


@dsl.pipeline(
    name="Head Detection Pipeline",
    description=""
)
def pipeline(git_repo,
             branch="master",
             rev='HEAD',
             git_secret="git-creds"):
    src_vol_op = dsl.VolumeOp(
        name="Git_source_pvc",
        resource_name="git-pvc",
        size='50Mi',
        modes=dsl.VOLUME_MODE_RWM
    )

    gitsync_step = dsl.ContainerOp(
        name="Git-sync",
        image="k8s.gcr.io/git-sync/git-sync:v3.3.0",
        arguments=["--ssh",
                   f"--repo={git_repo}",
                   "--root=/tmp/src",
                   "--dest=pipeline_source",
                   "--depth=1",
                   f"--rev={rev}",
                   f"--branch={branch}",
                   "--one-time"
                   ],
        pvolumes={"/tmp/src": src_vol_op.volume}
    )

    gitsync_step.add_volume(k8s_client.V1Volume(
        name='git-cred-volume',
        secret=k8s_client.V1SecretVolumeSource(secret_name=git_secret))
        ).add_volume_mount(k8s_client.V1VolumeMount(mount_path="/etc/git-secret",
                                                   name="git-cred-volume"))
    gitsync_step.execution_options.caching_strategy.max_cache_staleness = "P0D"

    step1 = dsl.ContainerOp(
        name="step1",
        image="python:3.8",
        command=["python"],
        arguments=["/tmp/src/pipeline_source/step1.py", "--arg1", "input_arg1", "--arg2", "input_arg2"],
        pvolumes={"/tmp/src": src_vol_op.volume.after(gitsync_step)}
    ).add_env_variable(k8s_client.V1EnvVar(name="PYTHONPATH", value="/tmp/src/pipeline_source"))
    step1.execution_options.caching_strategy.max_cache_staleness = "P0D"

    step2 = dsl.ContainerOp(
        name="step2",
        image="python:3.8",
        command=["python"],
        arguments=["/tmp/src/pipeline_source/step2.py", "--arg1", "input_arg1", "--arg2", "input_arg2"],
        pvolumes={"/tmp/src": src_vol_op.volume.after(step1)}
    ).add_env_variable(k8s_client.V1EnvVar(name="PYTHONPATH", value="/tmp/src/pipeline_source"))
    step2.execution_options.caching_strategy.max_cache_staleness = "P0D"

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(pipeline, __file__ + ".yaml")

#git@github.com:tanle2694/head_detection_pipeline.git