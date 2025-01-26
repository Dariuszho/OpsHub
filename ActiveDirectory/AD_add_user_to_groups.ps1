<#
.DESCRIPTION
Short script to add users as member within group by SamAccountName name.
#>

Import-Module ActiveDirectory

$user = Read-Host "Insert the SamAccountName of User "

$sam = Get-ADUser -Filter "SamAccountName -eq '$user'"

$user_name = $sam.SamAccountName

Write-Host "The user name is $user_name, please confirm (Y/N)" -ForegroundColor Blue

$answer_input = Read-Host

if ($answer_input -eq "Y") {
    Write-Host = "Continuing with task.." -ForegroundColor Green
}

else {
    Write-Host "Please recheck the ADUser..." -ForegroundColor Red
    Exit
}

$groups = ((Read-Host -Prompt "Insert the Name of Group or Groups with comma ") -Split ',').Trim()

foreach ($group in $groups) {

    Add-ADGroupMember -Identity $group -Members $sam

    $u_g = (Get-ADGroupMember -Identity $group | Where-Object Name -match $sam.Name).Name

    # To use with VSCode or ISE not suporting right-to-left language
    $user_ingroup = $u_g[-1.. - $u_g.Length] -join ''

    Write-Host "Added $user_ingroup to $group" -ForegroundColor Yellow

}