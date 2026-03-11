$ErrorActionPreference = 'Stop'
$python = 'F:\software\Anaconda\envs\easymocap\python.exe'
$emcRoot = 'C:\Users\Administrator\Documents\GitHub\EZcap_clean'
$env:PATH = 'F:\software\Anaconda\envs\easymocap\Library\bin;' + $env:PATH

$jobs = @(
    @{ Name='cam00'; Cfg='D:\08A4_kgy\configs\hrnet_pare_finetune_keepimg_cam00_full.yml'; Root='D:\08A4_kgy\data\cam00'; Sub='08A4_00'; End='4991' },
    @{ Name='cam01'; Cfg='D:\08A4_kgy\configs\hrnet_pare_finetune_keepimg_cam01_full.yml'; Root='D:\08A4_kgy\data\cam01'; Sub='08A4_01'; End='4819' }
)

foreach ($job in $jobs) {
    $log = "D:\08A4_kgy\$($job.Name)_run.log"
    $err = "D:\08A4_kgy\$($job.Name)_run.err.log"
    "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] start $($job.Name)" | Add-Content -Path $log

    $args = @(
        "$emcRoot\apps\mocap\run.py",
        '--data','config/datasets/svimage.yml',
        '--exp', $job.Cfg,
        '--root', $job.Root,
        '--subs', $job.Sub,
        '--ranges','0',$job.End,'1'
    )

    $proc = Start-Process -FilePath $python -ArgumentList $args -WorkingDirectory $emcRoot -PassThru -Wait -NoNewWindow -RedirectStandardOutput $log -RedirectStandardError $err
    if (Test-Path $err) {
        Get-Content $err | Add-Content -Path $log
        Remove-Item $err -Force -ErrorAction SilentlyContinue
    }
    if ($proc.ExitCode -ne 0) {
        throw "run.py failed for $($job.Name), exit=$($proc.ExitCode)"
    }
    "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] done $($job.Name)" | Add-Content -Path $log
}

$cleanup = Join-Path $emcRoot 'output\sv1p'
if (Test-Path $cleanup) {
    cmd /c rd /s /q "$cleanup"
}
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] all done" | Add-Content -Path 'D:\08A4_kgy\run_all.log'
