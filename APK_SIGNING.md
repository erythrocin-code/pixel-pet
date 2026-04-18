# APK 签名说明

## 关于 APK 签名

Android 要求所有 APK 在安装前必须进行签名。

### 签名类型

1. **Debug 签名**（开发用）
   - Buildozer 默认使用 debug 签名
   - 密钥位置：`~/.android/debug.keystore`
   - 仅用于测试，不能发布到应用商店

2. **Release 签名**（发布用）
   - 需要自己生成密钥
   - 用于正式发布

---

## 自动签名（Buildozer）

Buildozer 构建 debug APK 时会自动签名：

```bash
buildozer android debug
```

生成的 APK 位于 `bin/` 目录，已使用 debug 签名。

---

## 手动签名 Release APK

### 1. 生成签名密钥

```bash
keytool -genkey -v \
    -keystore pixel_pet.keystore \
    -alias pixel_pet \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000
```

按提示输入密码和信息。

### 2. 对齐 APK

```bash
zipalign -v 4 bin/pixel_pet-1.0.0-release-unsigned.apk bin/pixel_pet-aligned.apk
```

### 3. 签名 APK

```bash
apksigner sign \
    --ks pixel_pet.keystore \
    --ks-key-alias pixel_pet \
    --out bin/pixel_pet-release.apk \
    bin/pixel_pet-aligned.apk
```

### 4. 验证签名

```bash
apksigner verify --verbose bin/pixel_pet-release.apk
```

---

## Buildozer 自动签名 Release APK

在 `buildozer.spec` 中配置：

```ini
# Release 构建
android.release_artifact = aab

# 签名配置
android.keystore = %(source.dir)s/pixel_pet.keystore
android.keystore_alias = pixel_pet
android.release_artifact = apk
```

然后运行：

```bash
buildozer android release
```

---

## 常见问题

### 问题：安装时提示"未签名"

**原因**：APK 未签名或签名无效

**解决**：
1. 使用 `buildozer android debug` 构建（自动签名）
2. 或手动签名（见上方步骤）

### 问题：debug 签名的安全警告

**正常现象**：debug 签名会显示安全警告

**解决**：
1. 测试用可以忽略
2. 正式发布需要使用 release 签名

### 问题：签名密钥丢失

**注意**：如果丢失签名密钥，无法更新已发布的应用！

**建议**：
1. 备份 `pixel_pet.keystore` 文件
2. 记住密码
3. 存放在安全的地方

---

## 快速签名脚本

使用 `sign_apk.sh` 脚本：

```bash
chmod +x sign_apk.sh
./sign_apk.sh bin/pixel_pet-1.0.0-debug.apk
```

会自动生成密钥并签名。

---

## 安装说明

### 安装到手机

```bash
# 使用 ADB 安装
adb install bin/pixel_pet-1.0.0-debug.apk

# 或手动安装
# 1. 将 APK 复制到手机
# 2. 在手机上打开文件管理器
# 3. 点击 APK 文件安装
```

### 允许未知来源

首次安装需要允许"未知来源"：

1. 设置 → 安全 → 更多安全设置
2. 开启"允许安装未知来源应用"
3. 选择文件管理器

---

## 总结

- **Debug APK**：自动签名，用于测试
- **Release APK**：需要手动签名，用于发布
- 使用 `buildozer android debug` 即可获得可安装的 APK
