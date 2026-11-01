# Deployment Runbook

This runbook describes how an authorized team member deploys a release candidate to the university VM. Local installation, dependency installation, and starting the application for development are documented in [Setup and run](setup.md); those instructions are intentionally not repeated here.

## Environments

| Environment | Purpose | Where it runs | Configuration |
| ----------- | ------- | ------------- | ------------- |
| Development | Build, run, and check changes while developing. | A team member's machine. | Local development configuration. See [Setup and run](setup.md). |
| Integration | Run automated repository and product-code checks. | GitHub Actions. | CI configuration and test dependencies. CI does not deploy to the university network. |
| Staging | Validate the release candidate in a production-like environment before promotion. | A separate deployment on the team university VM. | Staging-specific configuration and secrets; a dedicated port. |
| Production | Serve the product to the customer. | A separate deployment on the same team university VM. | Production-specific configuration and secrets; a different port from staging. |

Staging and production share the VM, but they are separate deployments on separate ports, with separate configuration and separate secrets. Staging verification must not write production data. The customer accesses production from the university network at the VM's IPv4 address; the product is not intended to be publicly reachable from the internet.

## Access and prerequisites

Deployment is manual and must be performed from a machine connected to the university network. GitHub Actions cannot deploy to the university VM.

Before deploying, confirm all of the following:

- The team VM has been provisioned or recreated through the university portal and its access password has been set.
- The deploying machine is connected to the university network.
- PowerShell, and PuTTY's `plink` command-line SSH client are installed and available in `PATH`.
- The repository is on the intended release-candidate commit, with a clean working tree and all required CI checks passing.
- The local private configuration files required by the deployment scripts are present. The deployment scripts' comments or usage instructions are the source of truth for their exact variable names and file formats.
- The previous production release's commit or tag has been recorded, so it can be restored if verification fails.

## Configuration and secrets

[`../.env.example`](../.env.example) documents the shape of the application's configuration. It contains placeholders only; it is not a production configuration file.

The deployment process uses private local configuration files named `.env`, `staging.env`, and `prod.env` when required by the checked-in deployment scripts. Keep these files on the authorized operator's machine or in another approved private location. Do not commit them, paste them into an issue or pull request, or copy their values into this runbook. Install runtime configuration and secrets on the VM outside the Git working tree, with separate values for staging and production.

Before committing any deployment-related change, verify that these local files are ignored and are not tracked:

```powershell
git check-ignore -v .env staging.env prod.env
git ls-files --error-unmatch .env staging.env prod.env
```

The second command is expected to fail because these files must not be tracked. If it prints a tracked path, stop and remove the file from version control without publishing its contents. If any secret has already been committed, rotate it; deleting it in a later commit is not sufficient.

Do not put a real VM IPv4 address, host name, password, token, or secret in this runbook or any other repository file. Use `<university-vm-ipv4>` or environment variables in commands and documentation. Submit the actual staging and production addresses only in the private Moodle submission.

## First-time SSH host-key verification

The first SSH connection from a Windows user profile may cause Plink to display the VM's SSH host-key fingerprint and ask whether it should be trusted. This is a host key, not an application TLS certificate.

1. Obtain the expected SSH host-key fingerprint from a trusted university VM portal or administrator channel.
2. From PowerShell on the campus-connected machine, connect interactively using the deployment username and the VM host value stored in the private configuration. For example, use the form `plink -ssh <deployment-user>@<university-vm-ipv4>` with the actual values supplied privately.
3. Compare the displayed fingerprint with the trusted value. Accept it only when they match.
4. Once the key has been cached for the current Windows user, end the interactive attempt at the authentication prompt if no sign-in is needed. Run the deployment scripts only after host-key trust has been established.

Do not blindly accept an unfamiliar fingerprint. If a previously trusted host key changes, stop and verify the change with the university administrator before continuing. Do not work around a host-key error by disabling verification.

## Prepare the candidate

From the repository root, record the exact candidate commit and verify that the working tree is clean:

```powershell
git status --short
git rev-parse HEAD
git log -1 --oneline
```

Use the commit SHA as the identity of the candidate for both deployments. Do not change the code between staging and production. If the candidate changes after staging verification, deploy and verify the new commit on staging before promoting it.

## Deploy to staging

1. Confirm the candidate commit has passed the required CI checks.
2. Confirm the private staging configuration is selected. Do not use production secrets or production data for staging.
3. Run the staging deployment script included in the repository branch. Copy its exact checked-in path and invocation into the command block below before merging this runbook; do not invent an invocation or expose secret values.

```powershell
.\scripts\deploy_to_staging.bat <deployment commit hash>
```

4. Read the script's output and confirm the target is staging, the configured staging port is used, and the remote deployment corresponds to the recorded candidate commit.
5. From a campus-connected machine, open the staging deployment using the private staging address/configuration. Run the staging checks required by the applicable quality-requirement tests. Confirm that the staging test does not alter production data.
6. Do not promote the candidate if deployment or staging verification fails. Record the failure, restore the last known-good staging commit if necessary, fix the cause, and re-run staging verification.

## Promote the same commit to production

Proceed only after the staging deployment of the candidate commit has passed verification.

1. Confirm the commit SHA deployed to staging is the intended release candidate.
2. Select the private production configuration and production-specific secrets. Confirm that production uses its separate port and configuration.
3. Run the production deployment script included in the repository branch. Copy its exact checked-in path and invocation into the command block below before merging this runbook.

```powershell
.\scripts\deploy_to_prod.bat <deployment commit hash>
```

4. Confirm from script output or the deployed version information that production now runs the same commit SHA that was verified on staging.
5. From a campus-connected machine, perform the core task on production: choose a problem kind, generate an exercise, connect to the exercise from VS Code, and verify the fix. Check the customer-facing production instance, not a local development server.
6. Record the production commit and verification outcome with the release. Put the real staging and production addresses in the private Moodle submission only.

## Verify a deployment

For each production deployment, record and check the following:

- The candidate commit SHA.
- The production deployment completed without script or service errors.
- The application can be opened from the university network.
- A learner can choose a problem kind and generate an exercise.
- The learner can connect to the exercise in VS Code using the product's supported workflow.
- Official verification returns the expected pass/fail result for the exercise.
- The instance being checked is production, and the checked commit matches the deployment record.

Record the evidence in the relevant release/report artifacts. Do not place real addresses or secret values in the public repository.

## Rollback

Rollback if production deployment fails or the production core-task verification does not pass.

1. Stop further promotion and record the failed candidate commit and the failure observed.
2. Identify the previous known-good production commit or release tag recorded before the deployment.
3. Use the same production deployment mechanism and production configuration to redeploy that previous commit.
4. From a campus-connected machine, repeat the production core-task verification against the restored version.
5. Record the restored commit and the verification result with the release report. Keep the failed candidate available for diagnosis; do not overwrite or delete the deployment evidence.

If the checked-in scripts do not support selecting a prior commit safely, stop and add a reviewed rollback path to the scripts before relying on them for production recovery. Do not improvise a destructive reset or remove the known-good deployment before the new version has passed verification.

## Deployment record

For every release, record at least:

| Item | Value to record |
| ---- | --------------- |
| Candidate commit | Full commit SHA; no secret data. |
| Staging deployment | Date/time, commit SHA, check performed, pass/fail, evidence link. |
| Production deployment | Date/time, commit SHA, core-task verification result, evidence link. |
| Rollback | Previous commit restored, reason, and verification result; or `None`. |
| Public-address handling | Confirm real staging and production addresses are present only in the private Moodle submission, not the repository. |
