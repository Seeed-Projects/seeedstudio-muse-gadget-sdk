# SenseCraft × Muse Gadgets 挑战赛

[English](challenge.md)

使用 Muse 和受支持的 Seeed 设备制作项目。**项目源码必须公开在 GitHub 上**，并在 SenseCraft 的 CodeCraft Hub 发布的项目案例中附上仓库链接。可以使用自己的 GitHub 仓库或公开 Fork。向 Seeed 官方 SDK 仓库提交 PR 属于自愿贡献。

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

## 3. 安装和配置 Muse Gadget SDK

按照[入门指南](../README.zh-CN.md#第-1-步获取-sdk-token)准备 Muse 账号和 SDK token，安装固件，并在 Muse app 里完成设备配对。使用这个 Seeed SDK 仓库进行开发。

使用 AI 帮助配置时，在本仓库中启动编程助手，让它先阅读 [AGENTS.md](../AGENTS.md) 和本指南，并告诉它你的设备型号。AI 据此执行对应设备的配置步骤。账号凭据通过配置工具和设备设置在本地填写。

## 4. 开发并测试项目

向 AI 描述你想制作的项目，按 SDK 的[应用开发说明](../AGENTS.md#building-apps-and-demos)进行开发。复用已有的设备支持代码，并在真实硬件上验证项目。

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

3. Hub 的固件上传**只选择这个构建目录里新生成的 `muse-gadget.bin`**。例如 Sticky 的文件相对于仓库根目录为 `esp32/build-reterminal-sticky/muse-gadget.bin`。烧录时，Hub 会补充它自带的开机程序和分区表。

   上传前，对准备上传的这个文件检查完整 Muse SDK token。在 `esp32/` 目录运行以下命令，将构建目录替换为自己的设备对应目录：

   ```sh
   grep -aoE 'mgst_[A-Za-z0-9_-]{43}' build-reterminal-sticky/muse-gadget.bin
   ```

   规则匹配 `mgst_` 加上 43 个 token 字符。固件用于校验格式的短前缀 `mgst_` 本身不会命中。**文件可正常读取、命令没有输出且退出码为 1，才算通过这项 token 检查。** 有输出且退出码为 0，表示发现完整 token 格式的内容，应清空构建配置中的 token、重新构建，再检查新固件。退出码为 2 或更大表示检查失败，修正文件路径或读取错误后重查。匹配值保留在本地，对外只汇报是否命中。

   AI 执行时使用静默版本，将 token 内容保留在本地：

   ```sh
   grep -aqE 'mgst_[A-Za-z0-9_-]{43}' build-reterminal-sticky/muse-gadget.bin
   ```

   静默版本以退出码判断：1 为通过，0 为命中 token，2 或更大为检查失败。上传通过检查的那一份固件。

### 5.2. 整理项目材料

整理以下材料：

| 材料 | 内容 |
|---|---|
| 项目介绍 | 名称、用途、支持设备和主要功能 |
| 效果展示 | 封面、真实设备照片，以及可提供的演示视频链接 |
| 使用说明 | 硬件清单、安装和配置步骤、操作方法与实测结果 |
| 固件 | 清空 SDK token 后重新构建的 `muse-gadget.bin`，以及对应的板卡和安装说明；在第 6 步通过 Hub 草稿页验证 |
| 源码，必需 | 包含项目源码的公开 GitHub 仓库链接，可使用自己的仓库或公开 Fork |

在未登录 GitHub 的状态下打开仓库链接，确认可以直接查看项目源码，并将该链接写入项目案例。

### 5.3. 配置 SenseCraft CLI

把 [SenseCraft CLI 安装指南](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/guides/getting-started/setting-up/)里的指令交给 AI，按指南完成 CLI 和配套技能安装。使用国际站账号完成浏览器授权，站点选择 **Global（International）**，然后查看当前授权：

```sh
sensecraft-cli auth info
```

确认当前站点为 Global，账号为自己参赛时使用的账号。按 CLI 指南完成上传项目材料所需的授权。

## 6. 上传并测试项目草稿

让 AI 按照 [CLI 文档](https://sensecraft.seeed.cc/wiki/en/sensecraft-cli/)和配套的 `sensecraft-apps/create-app` 技能，将项目资料和**重新构建的 `muse-gadget.bin` 这一个固件文件**上传到 CodeCraft Hub，在案例中附上必需的公开 GitHub 源码仓库链接，保存为草稿，并返回草稿编辑链接和应用编号。

发布前，验证已经上传的这份固件：

1. 打开 Hub 草稿页，用 USB 连接自己的设备。草稿阶段即可在自己的设备上测试。
2. 使用草稿页自带的烧录按钮，把草稿中上传的固件安装到对应型号的设备。
3. 按页面提示填写自己的 Muse SDK token，由页面在烧录完成后通过串口写入设备设置。
4. 完成 Muse 配对或重新连接，在设备上验证项目的主要功能，将结果与应用编号、固件文件名一起记录。

这样验证的就是草稿中实际上传的同一份固件。每次更新固件，都重新执行构建、上传和草稿页设备验证。把应用编号保存在项目中，后续上传时更新同一作品。

## 7. 检查、发布并提交案例链接

草稿页设备验证通过后，检查项目介绍、硬件信息、固件和公开 GitHub 源码仓库链接。确认未登录 GitHub 时可以通过该链接查看项目源码，然后**在 CodeCraft Hub 上手动发布**。以发布后的项目案例链接作为参赛提交凭证，按[比赛页面](https://codecraft.seeed.cc/hub/contest/muse-gadget-challenge)说明提交到指定位置，并查看当前截止时间。

发布的项目案例必须包含公开 GitHub 源码仓库链接。希望同时改进 Seeed 官方 SDK 的开发者，可以自愿按照[贡献说明](../AGENTS.md#contributing)另行提交 PR。
