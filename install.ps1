# Cai dat skill cau duong bo VN cho Claude Code / Codex / Gemini (Windows).
# Dung Junction nen khong doi hoi quyen Administrator.
# Chay: .\install.ps1   (hoac .\install.ps1 -Uninstall de go)
param([switch]$Uninstall)

$RepoDir = $PSScriptRoot
$Targets = @(
    (Join-Path $env:USERPROFILE ".claude\skills"),
    (Join-Path $env:USERPROFILE ".agents\skills")
)

foreach ($Target in $Targets) {
    if ($Uninstall) {
        if (-not (Test-Path $Target)) { continue }
        Get-ChildItem -Path "$RepoDir\skills" -Directory | ForEach-Object {
            $LinkPath = Join-Path $Target $_.Name
            $Existing = Get-Item $LinkPath -Force -ErrorAction SilentlyContinue
            if (-not $Existing) { return }
            if (-not ($Existing.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                Write-Warning "BO QUA $($_.Name) -> $LinkPath (khong phai junction; khong xoa)"
                return
            }
            # Chi xoa lien ket, khong de Remove-Item -Recurse di theo junction vao repo
            $Existing.Delete()
            Write-Host "Unlinked $($_.Name) <- $LinkPath"
        }
        continue
    }
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    Get-ChildItem -Path "$RepoDir\skills" -Directory | ForEach-Object {
        $LinkPath = Join-Path $Target $_.Name
        $Existing = Get-Item $LinkPath -Force -ErrorAction SilentlyContinue
        if ($Existing -and -not ($Existing.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            Write-Warning "BO QUA $($_.Name) -> $LinkPath (ton tai ban khac symlink; xoa thu cong neu muon ghi de)"
            return
        }
        if ($Existing) { $Existing.Delete() }  # chi xoa junction cu, khong xoa noi dung
        New-Item -ItemType Junction -Path $LinkPath -Target $_.FullName | Out-Null
        Write-Host "Linked $($_.Name) -> $LinkPath"
    }
}
Write-Host "Xong. Mo lai session agent de no nhan skill moi."
