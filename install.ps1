# Cai skill thiet ke cau duong bo VN cho Claude Code / Codex / Gemini (Windows).
# Dung Junction nen khong doi hoi quyen Administrator.
#   .\install.ps1                              -> cai moi skill
#   .\install.ps1 -Only cau-11823,duong-4054   -> cai co ban nay (tuong lai co nhieu mang)
#   .\install.ps1 -List                        -> liet ke skill co trong repo
#   .\install.ps1 -Uninstall [-Only ten]       -> go lien ket (khong -Only = go het; repo giu nguyen)
param(
    [switch]$Uninstall,
    [switch]$List,
    [string[]]$Only = @()
)

$RepoDir = $PSScriptRoot
$Targets = @(
    (Join-Path $env:USERPROFILE ".claude\skills"),
    (Join-Path $env:USERPROFILE ".agents\skills")
)

$All = @(Get-ChildItem -Path "$RepoDir\skills" -Directory | Select-Object -ExpandProperty Name)

if ($List) {
    Write-Host "Skill co trong repo:"
    $All | ForEach-Object { Write-Host "  $_" }
    exit 0
}

if ($Only.Count -eq 0) {
    $Skills = $All
} else {
    foreach ($n in $Only) {
        if ($All -notcontains $n) {
            Write-Error "Khong thay skills/$n. Skill co trong repo:"
            $All | ForEach-Object { Write-Host "  $_" }
            exit 1
        }
    }
    $Skills = $Only
}

foreach ($Target in $Targets) {
    if ($Uninstall) {
        if (-not (Test-Path $Target)) { continue }
        foreach ($name in $Skills) {
            $LinkPath = Join-Path $Target $name
            $Existing = Get-Item $LinkPath -Force -ErrorAction SilentlyContinue
            if (-not $Existing) { continue }
            if (-not ($Existing.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                Write-Warning "BO QUA $name -> $LinkPath (khong phai junction; khong xoa)"
                continue
            }
            # Chi xoa lien ket, khong de Remove-Item -Recurse di theo junction vao repo
            $Existing.Delete()
            Write-Host "Unlinked $name <- $LinkPath"
        }
        continue
    }
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    foreach ($name in $Skills) {
        $Src = Join-Path "$RepoDir\skills" $name
        $LinkPath = Join-Path $Target $name
        $Existing = Get-Item $LinkPath -Force -ErrorAction SilentlyContinue
        if ($Existing -and -not ($Existing.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            Write-Warning "BO QUA $name -> $LinkPath (ton tai ban khac lien ket; xoa thu cong neu muon ghi de)"
            continue
        }
        if ($Existing) { $Existing.Delete() }  # chi xoa junction cu, khong xoa noi dung
        New-Item -ItemType Junction -Path $LinkPath -Target $Src | Out-Null
        Write-Host "Linked $name -> $LinkPath"
    }
}

if (-not $Uninstall) {
    # Kiem tra Python - skill chay scripts/bridge_calc.py; Windows mac dinh CHUA co Python san
    $Py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $Py) { $Py = Get-Command py -ErrorAction SilentlyContinue }
    if ($Py) {
        Write-Host ("Python: " + (& $Py.Source --version 2>&1))
    } else {
        Write-Warning "May nay chua co Python - skill can Python 3.10+ de chay bridge_calc.py."
        Write-Warning "Cai dat:  winget install Python.Python.3.12   (mo lai Terminal sau khi cai)"
    }
}
if ($Uninstall) {
    Write-Host "Xong. Chi xoa lien ket, repo va noi dung giu nguyen."
} else {
    Write-Host "Xong. Mo lai session agent de no nhan skill moi."
}
