# Challenge participation

Read the [participant guide](README.md)
([简体中文](README.zh-CN.md)) before working on a challenge entry or an
application built with this SDK.

Keep your project's code in your own GitHub repository. This repository
accepts pull requests for device support, board-neutral Muse features and
fixes. Project cases and firmware are submitted to
[CodeCraft Hub](https://codecraft.seeed.cc/hub/).

## Onboarding and repository destinations

At onboarding, guide the participant to register and verify that a Global
(International) account can sign in to CodeCraft Hub before hardware setup
or development. Prepare the separate Muse account through the beginner's
guide. Explain that the project source must be public on GitHub and linked
from the case.

Follow [step 3](README.md#3-fork-and-set-up-the-muse-gadget-sdk) to create
a public Fork under the participant's account and configure the checkout:

| Remote | Destination |
|---|---|
| `origin` | The participant's own GitHub Fork |
| `seeed` | `Seeed-Projects/seeedstudio-muse-gadget-sdk` |
| `upstream` | `facebookincubator/muse-gadget-sdk`, for Meta SDK synchronization |

Before pushing, inspect `git remote -v` and verify that both the fetch and
push URLs for `origin` belong to the participant. Confirm that existing
`seeed` and `upstream` URLs match the table, using the participant guide to
align remote names and any separately configured push URL. Publish the project's
branch to that `origin` when asked to submit or publish the project's code.
Route requests for official SDK improvements through the root contribution
table.

## Validation scope and completion

For a project in the participant's own repository, completion requires:

1. A successful build for the device used by the project.
2. On-device testing of the project's main functions on that device.
3. A passing complete-token scan of the exact firmware image selected for upload.
4. Successful testing of the uploaded image through the Hub draft page.

Record the tested source revision, device, build result and actual hardware
results. Report pending checks explicitly. Use the platform and board
instructions for hardware facts, build commands and device operations.
The root `Changing code and docs` and `Verifying a change` requirements,
including board-matrix builds, host/simulator tests, bilingual SDK docs and
CI registration, apply to pull requests contributed to this repository.
Challenge entries use the four project checks above.

## Prepare and upload the draft

When asked to submit, use the participant guide's CLI setup instructions and
the bundled app-creation skill. Verify that the active authorization site is
Global. Collect the required public GitHub source link and open it while
signed out. The link must show the project directly: either the Fork's
README starts with its project introduction, or the case links to the
project branch or change comparison. Include that link in the case.

Follow the [release steps](README.md#51-build-the-firmware-for-sharing):
set `CONFIG_GADGET_SDK_TOKEN=""` in the selected build folder's `sdkconfig`,
rebuild the target board, verify that the resulting configuration still
has an empty token, and scan the exact `muse-gadget.bin` with:

```sh
grep -aqE 'mgst_[A-Za-z0-9_-]{43}' <firmware-path>
```

Exit code 1 passes; 0 detects a complete token pattern and requires a
token-free rebuild and rescan; 2 or higher is a check error to resolve
before retrying. Report the outcome while keeping matching values local.
Upload the checked `muse-gadget.bin` after it passes. Hub supplies the
bootloader and partition table for its standard device layout. Projects
that change the partition table are incompatible with Hub flashing.

## Test and publish the case

Return the draft's editing link and application ID. Guide the participant
to test the uploaded image on their own device with the draft page's flash
button, enter their own token for post-flash serial provisioning, and test
the project's main functions. Flashing follows the session's existing
authorization requirements. Repeat this test after each firmware update.

After all four project checks pass, the participant reviews the case,
firmware and public project-source link and publishes the case manually.
Return the published case link as the submission reference. Source code
remains in the participant's own GitHub repository; the case and firmware
remain on CodeCraft Hub.
