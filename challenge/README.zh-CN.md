# SenseCraft × Muse Gadgets 挑战赛

[English](README.md)

使用 Muse 和受支持的 Seeed 设备制作项目。**项目源码必须公开在 GitHub 上**，并在 SenseCraft 的 CodeCraft Hub 发布的项目案例中附上作品源码链接。参赛作品的代码保存在你自己的 GitHub 仓库里。本仓库接收设备支持、通用 Muse 功能和问题修复的 PR。

## 1. 报名并准备国际站账号

1. 填写[比赛报名表](https://forms.gle/tB2rQxda7AXeesbY8)。
2. 注册或登录**国际站（Global）账号**，确认能够登录 [CodeCraft Hub](https://codecraft.seeed.cc/hub/)。
3. 在购买硬件和开发项目之前完成这项账号检查。已有国际站账号的参赛者可直接使用；已有中国站账号的参赛者，请先确认自己能够登录国际站。

CodeCraft Hub 使用国际站账号。中国站提供 SenseCraft Data 服务。后续授权 SenseCraft CLI 时，同样选择 Global。详见 CLI 的[账号与授权说明](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/guides/getting-started/setting-up/#complete-user-authorization)。

Muse 账号用于设备连接 Muse，在第 3 步准备。

## 2. 准备硬件

选择参赛设备，准备一根能传数据的 USB 线。使用本 Seeed SDK 维护的配置文件：

| 设备 | SDK 支持状态 | 配置文件 |
|---|---|---|
| reTerminal E1001 | 已支持 | [sdkconfig.reterminal-e1001](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.reterminal-e1001) |
| reTerminal E1002 | 已支持 | [sdkconfig.reterminal-e1002](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.reterminal-e1002) |
| SenseCAP Watcher | 已支持 | [sdkconfig.muse-sensecap-watcher](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.muse-sensecap-watcher) |
| SenseCAP Indicator | 已支持 | [sdkconfig.sensecap-indicator](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.sensecap-indicator) |
| reTerminal Sticky | 实验性支持 | [sdkconfig.reterminal-sticky](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.reterminal-sticky) |
| XIAO ESP32-S3 1.47 英寸触摸屏 | 已支持 | [sdkconfig.muse-seeed-xiao-s3-147](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/blob/main/esp32/devices/sdkconfig.muse-seeed-xiao-s3-147) |

编译工具会将这些配置与 SDK 默认配置组合使用。按你的设备对应的[编译与安装步骤](../README.zh-CN.md#方法-c自己编译)操作。[设备指南](../esp32/devices/README.md)记录了各项功能及真机验证情况，包括 Sticky 实验性支持的具体范围。

## 3. Fork 并配置 Muse Gadget SDK

### 从自己的 Fork 开始

1. 在 GitHub 打开 [Seeed SDK 仓库](https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk)，点击 **Fork**，在自己的账号下创建公开副本，或打开已有的 Fork。
2. 克隆自己的 Fork，并把 Seeed 仓库添加为独立的远程仓库。将 `YOUR_GITHUB_USERNAME` 替换为自己的账号名；如果 Fork 的仓库名不同，使用其实际地址和目录名：

   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git
   cd seeedstudio-muse-gadget-sdk
   git remote add seeed https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk.git
   git remote -v
   ```

### 已经克隆过仓库

先在 GitHub 创建或复用自己的公开 Fork，再在已有的工作目录运行 `git remote -v`。以下命令均使用自己 Fork 的实际地址。如果 `origin` 指向 Seeed，且尚未配置 `seeed`，先重命名原来的远程仓库，再把自己的 Fork 添加为 `origin`：

```sh
git remote rename origin seeed
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git
git remote -v
```

如果 `seeed` 已存在，保留它，并使用 `git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git` 将 `origin` 指向自己的 Fork。如果 `origin` 已经指向自己的 Fork，核对它的拉取和推送地址即可。

如果另外配置了推送地址，使用 `git remote set-url --push origin https://github.com/YOUR_GITHUB_USERNAME/seeedstudio-muse-gadget-sdk.git` 将其指向自己的 Fork。如果已有名为 `upstream` 的远程仓库指向 Seeed，且尚未配置 `seeed`，使用 `git remote rename upstream seeed` 将其重命名。

开发过程中统一使用以下名称：

| 远程名称 | 对应仓库 |
|---|---|
| `origin` | 自己的公开 GitHub Fork 或仓库，作品分支的推送目标 |
| `seeed` | `Seeed-Projects/seeedstudio-muse-gadget-sdk`，Seeed SDK 仓库 |
| `upstream` | `facebookincubator/muse-gadget-sdk`，保留给 Meta SDK 同步使用 |

推送作品代码前，确认 `origin` 的拉取和推送地址都属于自己的账号或自己拥有的组织。作品分支推送到 `origin`。

### 使用同一仓库网络中已有的 Fork

如果点击 **Fork** 后打开了自己的已有仓库，例如 `YOUR_GITHUB_USERNAME/muse-gadget-sdk`，直接将这个公开 Fork 用作 `origin`。Seeed SDK 本身是 Meta SDK 的 Fork，GitHub 允许每个账号在同一仓库网络中拥有一个 Fork。按上面的步骤填写它的实际地址，再从 `seeed/main` 创建作品分支并推送到 `origin`：

```sh
git fetch seeed && git switch -c YOUR_PROJECT_BRANCH seeed/main
git push -u origin YOUR_PROJECT_BRANCH
```

已有 Fork 仍在同一仓库网络中，因此[第 5.2 步](#52-整理项目材料)的改动对比链接仍然适用。将 `YOUR_FORK_NAME` 填为 Fork 的实际仓库名：

```text
https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/compare/main...YOUR_GITHUB_USERNAME:YOUR_FORK_NAME:YOUR_PROJECT_BRANCH
```

也可以选择：

- 将 Seeed SDK Fork 到自己拥有的 GitHub 组织。
- 创建新的公开仓库并将 `seeed/main` 推送过去；此时无法与 Seeed 仓库直接生成改动对比链接，按第 5.2 步在案例中链接到作品分支，或链接到以作品介绍开头的 README。

### 同步 Seeed 修复

在作品分支执行以下命令，获取并合并 Seeed 的最新修复：

```sh
git fetch seeed
git merge seeed/main
```

### 配置设备

在自己的 Fork 工作目录里，按照[入门指南](../README.zh-CN.md#第-1-步获取-sdk-token)准备 Muse 账号和 SDK token，安装固件，并在 Muse app 里完成设备配对。

使用 AI 帮助配置时，在自己的 Fork 工作目录中启动编程助手，让它先阅读[根目录说明](../AGENTS.md)、[比赛执行说明](AGENTS.md)和本指南，并告诉它你的设备型号。AI 据此执行对应设备的配置步骤。账号凭据通过配置工具和设备设置在本地填写。

### 安装项目的 Muse 技能

项目的 `SKILL.md` 准备好后，在配对完成、开始测试之前，将文件全文粘贴到设备所有者的 Muse 聊天中一次，并请 Muse 记住它。技能告诉 Muse 如何使用项目命令，以及如何回应设备事件，例如提醒确认。

使用通过 USB 连接的完整界面板卡时，也可以在 `esp32/` 目录发送：

```sh
python3 tools/muse/chat.py --file path/to/SKILL.md "Please remember this skill"
```

将 `path/to/SKILL.md` 替换为项目技能文件的实际路径。每次修改技能后，再发送一次全文。

## 4. 开发并测试项目

向 AI 描述你想制作的项目，按 SDK 的[应用开发说明](../AGENTS.md#building-apps-and-demos)进行开发。复用已有的设备支持代码，并在真实硬件上验证项目。

在 1.4–2 英寸屏幕上，使用至少 16 px 的文字，以短词或图标表达信息，并在实际屏幕上检查可读性。

记录设备型号、编译配置、SDK 版本、编译结果和真机运行结果，拍摄实物照片或录制演示视频。用于分享的固件按第 5 步另行构建，并在第 6 步通过 Hub 草稿页安装到自己的设备上验证。

将项目源码公开在自己的 GitHub 仓库或公开 Fork 中，包含用于编译演示项目的源码改动，以及编译和运行说明。

## 5. 准备项目案例和 SenseCraft CLI

### 5.1. 构建用于分享的固件

**上传前，将 SDK token 清空并重新构建应用固件。** 入门指南中填入的 token 用于自己的设备构建；用于分享的固件在烧录完成后，通过串口写入使用者各自的 token。Hub 和 [Seeed 网页烧录器](../web-flasher/README.md#the-sdk-token)均采用这种配置方式。

Hub 会为所选设备提供开机程序（bootloader）和分区表。**Hub 烧录支持该设备的标准分区布局；项目自行修改过分区表的，无法通过 Hub 烧录。** 发布到 Hub 的构建应保留 SDK 为该设备提供的原有分区布局。

1. 从 `esp32/` 目录找到设备对应的[构建配置文件夹](../README.zh-CN.md#4-填入-sdk-token)，打开其中的 `sdkconfig`。例如 Sticky 对应 `build-reterminal-sticky/sdkconfig`，将 token 改为空字符串：

   ```ini
   CONFIG_GADGET_SDK_TOKEN=""
   ```

2. 保存配置，重新运行该设备的编译命令。以 reTerminal Sticky 为例：

   ```sh
   tools/board.sh reterminal-sticky build
   ```

   其他设备使用[对应的编译命令](../README.zh-CN.md#方法-c自己编译)。SDK 支持空 token 构建；构建过程中显示 `No SDK token` 提示属于预期情况。构建完成后，确认该构建目录的 `sdkconfig` 中 token 仍为空。

3. Hub 的固件上传**只使用这个构建目录里新生成的应用固件 `muse-gadget.bin`**。例如 Sticky 的文件相对于仓库根目录为 `esp32/build-reterminal-sticky/muse-gadget.bin`。烧录时，Hub 会补充它自带的开机程序和分区表。

   Hub 按账号内的文件名保存上传文件。每个项目使用独立的固件文件名：将该次构建的 `muse-gadget.bin` 在同目录复制为例如 `fridge-notes-muse-gadget.bin`，上传这个改名副本。改名后的固件可从 Hub 草稿页正常烧录并启动。

   上传前，对准备上传的这个文件检查完整 Muse SDK token。在 `esp32/` 目录运行以下命令，将目录和文件名替换为上传副本的路径：

   ```sh
   grep -aoE 'mgst_[A-Za-z0-9_-]{43}' build-reterminal-sticky/fridge-notes-muse-gadget.bin
   ```

   规则匹配 `mgst_` 加上 43 个 token 字符。固件用于校验格式的短前缀 `mgst_` 本身不会命中。**文件可正常读取、命令没有输出且退出码为 1，才算通过这项 token 检查。** 有输出且退出码为 0，表示发现完整 token 格式的内容，应清空构建配置中的 token、重新构建，再检查新固件。退出码为 2 或更大表示检查失败，修正文件路径或读取错误后重查。匹配值保留在本地，对外只汇报是否命中。

   AI 执行时使用静默版本，将 token 内容保留在本地：

   ```sh
   grep -aqE 'mgst_[A-Za-z0-9_-]{43}' build-reterminal-sticky/fridge-notes-muse-gadget.bin
   ```

   静默版本以退出码判断：1 为通过，0 为命中 token，2 或更大为检查失败。上传通过检查的那一份固件。

### 5.2. 整理项目材料

整理以下材料：

| 材料 | 内容 |
|---|---|
| 项目介绍 | 名称、用途、支持设备和主要功能 |
| 效果展示 | 封面、真实设备照片，以及可提供的演示视频链接 |
| 使用说明 | 硬件清单、安装和配置步骤、操作方法与实测结果 |
| 固件 | 清空 SDK token 后重新构建的 `muse-gadget.bin`，复制为项目独立文件名，以及对应的板卡和安装说明；在第 6 步通过 Hub 草稿页验证 |
| 作品源码链接，必需 | 能直接展示作品的公开 GitHub 链接：在自己 Fork 的 README 顶部介绍作品，或在案例中直接链接到作品分支或改动对比 |

在 Hub 页面的使用说明中链接项目的 `SKILL.md`，并列出用户操作步骤：完成 Muse 配对，将技能全文粘贴到自己的 Muse 聊天中一次（或使用上面的 USB 命令），再体验项目。说明每次修改技能后都应重新发送全文。

在未登录 GitHub 的状态下打开链接，确认访客可以直接看到作品介绍和源码，或对应的作品分支、改动对比，并将该作品链接写入项目案例。

与 Seeed `main` 分支的改动对比链接格式如下：

```text
https://github.com/Seeed-Projects/seeedstudio-muse-gadget-sdk/compare/main...YOUR_GITHUB_USERNAME:YOUR_FORK_NAME:YOUR_PROJECT_BRANCH
```

将 `YOUR_GITHUB_USERNAME` 替换为自己的 GitHub 用户名或组织名，`YOUR_FORK_NAME` 替换为 Fork 的实际仓库名，`YOUR_PROJECT_BRANCH` 替换为作品所在的分支。

### 5.3. 配置 SenseCraft CLI

把 [SenseCraft CLI 安装指南](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/guides/getting-started/setting-up/)里的指令交给 AI，按指南完成 CLI 和配套技能安装。使用国际站账号完成浏览器授权，站点选择 **Global（International）**，然后查看当前授权：

```sh
sensecraft-cli auth info
```

确认当前站点为 Global，账号为自己参赛时使用的账号。按 CLI 指南完成上传项目材料所需的授权。

## 6. 上传并测试项目草稿

让 AI 按照 [CLI 文档](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/)和 CLI 自带的应用创建技能，将项目资料和**第 5.1 步改为项目独立文件名的应用固件副本**上传到 CodeCraft Hub，在案例中附上必需的公开 GitHub 作品源码链接，保存为草稿，并返回草稿编辑链接和应用编号。

AI 通过 CLI 更新草稿时，关闭该应用的 Hub 编辑页，更新完成后再打开：打开的编辑页会保存它加载时的副本。检查每个项目草稿的固件链接各不相同。

发布前，验证已经上传的这份固件：

1. 打开 Hub 草稿页，用 USB 连接自己的设备。草稿阶段即可在自己的设备上测试。
2. 使用草稿页自带的烧录按钮，把草稿中上传的固件安装到对应型号的设备。
3. 页面完成固件写入后，先按设备复位键，或拔下并重新连接 USB 来重启设备，再按页面提示填写自己的 Muse SDK token。若未出现 token 提示，可通过 USB 串口发送 `>sdk_token=mgst_…`，设备会回复 `@sdk_token ok`，详见 [SDK token 说明](../web-flasher/README.md#the-sdk-token)。
4. 完成 Muse 配对或重新连接。
5. 按[技能安装步骤](#安装项目的-muse-技能)，将项目的 `SKILL.md` 全文安装到自己的 Muse 聊天中；每次修改技能后重新发送。
6. 在设备上验证项目的主要功能和设备事件回复，将结果与应用编号、固件文件名一起记录。

这样验证的就是草稿中实际上传的同一份固件。每次更新固件，都重新执行构建、上传和草稿页设备验证。把应用编号保存在项目中，后续上传时更新同一作品。

## 7. 检查、发布并提交案例链接

草稿页设备验证通过后，检查项目介绍、硬件信息、固件和公开 GitHub 作品源码链接。确认未登录 GitHub 时可以通过该链接查看作品源码，然后**在 CodeCraft Hub 上手动发布**。以发布后的项目案例链接作为参赛提交凭证，按[比赛页面](https://codecraft.seeed.cc/hub/contest/muse-gadget-challenge)说明提交到指定位置，并查看当前截止时间。

发布的项目案例必须包含能直接展示作品的公开 GitHub 作品源码链接。参赛作品的代码保存在你自己的 GitHub 仓库里。本仓库接收设备支持、通用 Muse 功能和问题修复的 PR。
