param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$Region = 'asia-southeast1'
)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
  & gcloud run deploy pickmytech --source . --project $ProjectId --region $Region --allow-unauthenticated --min-instances 0 --max-instances 2 --memory 256Mi --cpu 1 --concurrency 80 --timeout 30 --quiet
  if ($LASTEXITCODE -ne 0) { throw 'Cloud Run deployment failed.' }
} finally { Pop-Location }
