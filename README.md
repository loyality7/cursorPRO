

This is a PowerShell script for resetting Cursor IDE device identifiers. The script supports Cursor 0.45.x.

## ⚠️ Disclaimer

This project is for educational and research purposes only, aimed at studying the device identification mechanism of Cursor IDE. **It is strongly recommended to purchase a [Cursor](https://cursor.sh/) license** to support the developers.

Using this script may violate Cursor's terms of service. The author assumes no responsibility for any issues arising from the use of this script, including but not limited to:

- Software license invalidation
- Account suspension
- Other unknown risks

If you value Cursor, please support the official version and pay for the developers' work.

## Usage

⚠️ To prevent the new account from being immediately invalidated, please follow these steps strictly:

### Windows

1. Sign out of your current account in Cursor IDE
2. Completely close Cursor IDE
3. Open Command Prompt or PowerShell as Administrator
4. Copy and paste the following command:

   ```batch
   powershell -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iwr -Uri 'https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.ps1' -UseBasicParsing | iex"
   ```

5. After reset is complete, open Cursor IDE and sign in with a new account (do not use the previous account)

If the script is stuck at "Waiting for Cursor process to exit...", you can force kill Cursor processes by running the following command in the terminal:

```powershell
taskkill /f /im cursor.exe
```

### macOS

1. Sign out of your current account in Cursor IDE
2. Completely close Cursor IDE
3. Open terminal and execute the following command:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.sh | bash
   ```

4. Start Cursor and sign in with a new account (do not use the previous account)

To restore to the original state, you can use the following command:

```bash
curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.sh | bash -s -- --restore
```

If the script is stuck at "Cursor is running", you can force kill Cursor processes by running the following command in the terminal:

```bash
pkill -9 Cursor
```

### Linux

1. Sign out of your current account in Cursor IDE
2. Completely close Cursor IDE
3. Open terminal and execute the following command:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/linux/bash.sh | bash -s -- --appimage /path/to/cursor.AppImage
   ```

   Replace `/path/to/cursor.AppImage` with the path to your Cursor AppImage file.

4. Start Cursor and sign in with a new account (do not use the previous account)

If the script is stuck at "Waiting for Cursor process to exit...", you can force kill Cursor processes by running the following command in the terminal:

```bash
pkill -9 Cursor
```

## ⚠️ Important Notes

### Windows

The script modifies the system registry key `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`, which may be used by other software as a device identifier. If you have purchased a license for Cursor or other software that uses this registry key for device identification, modifying it may invalidate these software licenses.

The original MachineGuid will be automatically backed up to the `%USERPROFILE%\MachineGuid_Backups` directory. If you need to restore the original MachineGuid, you can find the corresponding backup file in this directory and restore it using the registry editor.

## System Requirements

### Windows

- Windows OS
- PowerShell
- Administrator privileges
- Cursor IDE 0.45.x (tested on version 0.45.8)

### macOS

- macOS 10.13 or higher
- Cursor IDE 0.45.x

### Linux

- Linux operating system
- Cursor IDE 0.45.x (AppImage format)
- appimagetool (will be automatically downloaded if not present)
