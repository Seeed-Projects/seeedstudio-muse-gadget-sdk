# SenseCraft × Muse Gadgets Challenge

[简体中文](README.zh-CN.md)

Build a project with Muse and a supported Seeed device. **Publish its source
code in a public GitHub repository** and include a project source link in the
project case you publish on SenseCraft's CodeCraft Hub. Keep your project's
code in your own GitHub repository. This repository accepts pull requests
for device support, board-neutral Muse features and fixes.

## 1. Sign up and prepare your Global account

1. Complete the [challenge registration form](https://forms.gle/tB2rQxda7AXeesbY8).
2. Register or sign in with a **Global (International) account** and confirm
   you can sign in to [CodeCraft Hub](https://codecraft.seeed.cc/hub/).
3. Complete this account check before ordering hardware or developing your
   project. Participants with an existing Global account can use it directly;
   participants with a China-site account should first confirm their access
   to the Global site.

CodeCraft Hub uses the Global site. The China site provides SenseCraft Data.
The same Global site must be selected when authorizing SenseCraft CLI later.
See the CLI's [account and authorization guide](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/guides/getting-started/setting-up/#complete-user-authorization).

Your Muse account connects the device to Muse and is prepared in step 3.

## 2. Prepare your hardware

Choose a challenge device and a USB cable that carries data. Use the
configuration files maintained in this Seeed SDK:

| Device | SDK support | Configuration |
|---|---|---|
| reTerminal E1001 | Supported | [sdkconfig.reterminal-e1001](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.reterminal-e1001) |
| reTerminal E1002 | Supported | [sdkconfig.reterminal-e1002](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.reterminal-e1002) |
| SenseCAP Watcher | Supported | [sdkconfig.muse-sensecap-watcher](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.muse-sensecap-watcher) |
| SenseCAP Indicator | Supported | [sdkconfig.sensecap-indicator](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.sensecap-indicator) |
| reTerminal Sticky | Experimental support | [sdkconfig.reterminal-sticky](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.reterminal-sticky) |
| XIAO ESP32-S3 1.47 Touch Display | Supported | [sdkconfig.muse-seeed-xiao-s3-147](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.muse-seeed-xiao-s3-147) |

The board helpers combine these configurations with the SDK defaults. Follow
the [device-specific build and installation commands](../README.md#option-c-build-it-yourself)
for your board. The [device guide](../esp32/devices/README.md) records feature
support and hardware validation, including the limits of the experimental
Sticky port.

## 3. Fork and set up the Muse Gadget SDK

### Start from your own Fork

1. Open the [Seeed SDK repository](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk)
   on GitHub and select **Fork** to create a public copy under your own
   account.
2. Clone your Fork and add Seeed as a separate remote. Replace
   `YOUR_GITHUB_USERNAME` with your account name; use your Fork's actual URL
   if you chose a different repository name:

   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git
   cd seeedstudio-muse-gadget-sdk
   git remote add seeed https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk.git
   git remote -v
   ```

### Set up an existing checkout

Create your public Fork on GitHub, then run `git remote -v` in the existing
checkout. When `origin` points to Seeed and `seeed` has not been configured,
rename that remote and add your Fork as `origin`:

```sh
git remote rename origin seeed
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git
git remote -v
```

When `seeed` already exists, keep it and set `origin` to your Fork with
`git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git`.
When `origin` already points to your Fork, verify its fetch and push URLs.

For a separately configured push URL, point it to your Fork with
`git remote set-url --push origin https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git`.
If an existing remote named `upstream` points to Seeed and `seeed` is not
configured, rename it with `git remote rename upstream seeed`.

Use these remote names throughout development:

| Remote | Repository |
|---|---|
| `origin` | Your own GitHub Fork; the destination for your project branches |
| `seeed` | `Seeed-Projects/seeedstudio-muse-gadget-sdk`, the Seeed SDK |
| `upstream` | `facebookincubator/muse-gadget-sdk`, reserved for Meta SDK synchronization |

Verify that `origin`'s fetch and push URLs belong to your account before
pushing project code. Publish your project branch to `origin`.

### Sync Seeed fixes

To merge the latest Seeed fixes into your project branch, run:

```sh
git fetch seeed
git merge seeed/main
```

### Configure your device

Continue from your Fork checkout with the
[beginner's guide](../README.md#step-1-get-your-sdk-token) to prepare your
Muse account and SDK token, install the firmware and pair the device in the
Muse app.

For AI-assisted setup, start your coding agent in your Fork checkout and ask
it to read the [root instructions](../AGENTS.md),
[challenge instructions](AGENTS.md) and this guide. Tell it which device you
have; it can then follow that device's setup instructions. Configure account
credentials locally through the setup tools and device settings.

## 4. Develop and test your project

Describe the intended project to your coding agent and follow the SDK's
[application development guidance](../AGENTS.md#building-apps-and-demos).
Reuse the existing device support and verify the project on your hardware.

Record the device, build configuration, SDK revision, build result and
on-device results, and take photos or record a short video showing the
project working. Prepare the firmware for sharing in step 5 and test that
uploaded image on your device from the Hub draft in step 6.

Publish the project's source code in your own public GitHub repository or
public fork. Include the source changes used to build the demonstrated
project and instructions for building and running it.

## 5. Prepare the project case and SenseCraft CLI

### 5.1. Build the firmware for sharing

**Rebuild the application with an empty SDK token before uploading it.**
The token entered during the beginner's guide is for your own device build;
the shared image receives each user's token over serial after flashing.
This is the same setup method used by the Hub and the
[Seeed web flasher](../web-flasher/README.md#the-sdk-token).

Hub supplies the bootloader and partition table for the selected device.
**Hub flashing supports that device's standard partition layout. Projects
that change the partition table cannot be flashed through Hub.** Keep the
SDK's original partition layout for the device when preparing a Hub image.

1. From `esp32/`, find your board's
   [build configuration folder](../README.md#4-add-your-sdk-token). Open
   its `sdkconfig`, for example `build-reterminal-sticky/sdkconfig`, and
   set the token to an empty string:

   ```ini
   CONFIG_GADGET_SDK_TOKEN=""
   ```

2. Save the configuration and run your board's build command again. For
   reTerminal Sticky:

   ```sh
   tools/board.sh reterminal-sticky build
   ```

   Use the [build command for your device](../README.md#option-c-build-it-yourself).
   The SDK supports an empty token; a `No SDK token` warning is expected
   while the build completes. After rebuilding, confirm the token remains
   empty in that build folder's `sdkconfig`.

3. Select **only `muse-gadget.bin` from that rebuilt directory** for the
   Hub firmware upload. For Sticky, this is
   `esp32/build-reterminal-sticky/muse-gadget.bin`, relative to the repository
   root. Hub adds its own bootloader and partition table when flashing.

   Before uploading, scan that exact file for a complete Muse SDK token.
   From `esp32/`, run the following command, replacing the build directory
   with your device's:

   ```sh
   grep -aoE 'mgst_[A-Za-z0-9_-]{43}' build-reterminal-sticky/muse-gadget.bin
   ```

   The pattern matches `mgst_` followed by 43 token characters. The short
   `mgst_` prefix used by the firmware's format validation is not a match.
   **A readable file with no output and exit code 1 passes this token
   check.** Output and exit code 0 mean a full token pattern was found:
   clear the build token, rebuild and scan the new image again. Exit code
   2 or higher means the check failed; fix the path or read error and retry.
   Keep matching values local and report only whether a match was found.

   Agents use the quiet equivalent to keep token values out of tool output:

   ```sh
   grep -aqE 'mgst_[A-Za-z0-9_-]{43}' build-reterminal-sticky/muse-gadget.bin
   ```

   For this quiet command, the exit code is the result: 1 passes, 0 detects
   a token, and 2 or higher is a check error. Upload the image that passed.

### 5.2. Gather the project materials

Gather the following materials:

| Material | Contents |
|---|---|
| Project introduction | Name, purpose, supported devices and main features |
| Demonstration | Cover image, real-device photos and a video link when available |
| Usage instructions | Hardware list, installation and setup steps, operation and test results |
| Firmware | The rebuilt `muse-gadget.bin` with an empty SDK token, its target board and installation details; verify it from the Hub draft in step 6 |
| Project source link, required | A public GitHub link that shows the project directly: introduce the project at the top of your Fork's README, or link the case directly to its project branch or change comparison |

Open the GitHub link while signed out to confirm that visitors can see the
project introduction and source, or its project branch or change comparison.
Include that project-specific link in the case.

For a change comparison against Seeed's `main`, use this format:

```text
https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/compare/main...YOUR_GITHUB_USERNAME:seeedstudio-muse-gadget-sdk:YOUR_PROJECT_BRANCH
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub account and
`YOUR_PROJECT_BRANCH` with the branch containing your project. Use your
Fork's actual repository name if you chose a different one.

### 5.3. Set up SenseCraft CLI

Give your coding agent the instructions in the
[SenseCraft CLI setup guide](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/guides/getting-started/setting-up/).
It covers installation and the bundled agent skills. Complete browser
authorization with your Global account, choose **Global (International)**,
and check the active authorization with:

```sh
sensecraft-cli auth info
```

Confirm that the active site is Global and the account is the one you will
use for the challenge. Follow the CLI guide for the authorization needed to
upload project materials.

## 6. Upload and test the project draft

Ask your agent to follow the
[CLI documentation](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/)
and its bundled app-creation skill to upload the project materials and
**only the rebuilt `muse-gadget.bin`** to CodeCraft Hub as a draft, including
the required public GitHub project source link in the case. Have it return the draft's editing
link and application ID.

Test the uploaded image before publishing:

1. Open the Hub draft page and connect your own device over USB. Drafts can
   be tested on your device before publication.
2. Use the draft's built-in flash button to install its uploaded firmware
   on the matching device.
3. Enter your own Muse SDK token when the page prompts for it. The page
   writes it over serial into the device's settings after flashing.
4. Complete Muse pairing or reconnect, then verify the project's main
   functions on the device. Record the result with the application ID and
   firmware filename.

This tests the same firmware image that is uploaded to the draft. Each
firmware update repeats the rebuild, upload and draft-page device test.
Keep the application ID with the project so subsequent uploads update the
same entry.

## 7. Review, publish and submit the case link

After the draft-page device test passes, review the project information,
hardware, firmware and public GitHub project source link. Confirm that the
link opens the project's source code while signed out, then **publish the
case manually on CodeCraft Hub**. Use the published project-case link as your challenge
submission reference and follow the
[challenge page](https://codecraft.seeed.cc/hub/contest/muse-gadget-challenge)
for the submission destination and current deadlines.

The published project case must include the public GitHub project source
link that shows the submitted project. Keep your project's code in your own
GitHub repository. This repository accepts pull requests for device support,
board-neutral Muse features and fixes.
