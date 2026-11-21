# Remap mouse navigation buttons to zoom

Cursor on Ubuntu cannot bind the side buttons itself.
On Wayland those buttons arrive as mouse buttons, and Cursor hard-wires button 4 to Back and button 5 to Forward.
The View → Zoom In and Zoom Out commands stay on the keyboard: `Ctrl+Equal` and `Ctrl+Minus`.

This machine uses [xremap](https://github.com/xremap/xremap) to turn those buttons into those shortcuts while a Cursor window is focused.
Outside Cursor, the buttons still go back and forward.
The same mapping fits any mouse whose navigation buttons show up as `BTN_SIDE` (back) and `BTN_EXTRA` (forward), including the Logitech MX Vertical.

Verified with a Logitech Lift on Ubuntu 24.04 LTS (GNOME Shell 46, Wayland), Cursor 30.30.14, and xremap 0.15.18.
The active keyboard layout was US, so `C-MINUS` and `C-EQUAL` match Cursor's zoom shortcuts.

## What is installed

`~/.local/bin/xremap` is the GNOME build from the v0.15.18 release (`xremap-linux-x86_64-gnome.zip`).
`~/.local/share/gnome-shell/extensions/xremap@k0kubun.com` lets xremap see the focused window on GNOME Wayland.
That extension is in `org.gnome.shell` `enabled-extensions`.
`~/.config/xremap/config.yml` holds the mapping.
`~/.config/systemd/user/lift-cursor-zoom.service` starts xremap with the graphical session.
`~/.local/bin/lift-cursor-zoom-setup` does the one-time root setup: it adds the user to the `input` group, installs `/etc/udev/rules.d/99-input.rules` so that group can write `/dev/uinput`, and loads the `uinput` module.

The `input` group is permanent and applies to every process in this login, not only xremap.
Membership in it can read raw keyboard and mouse events.

## Mapping

`BTN_SIDE` is the back button and sends `Ctrl+Minus` (zoom out).
`BTN_EXTRA` is the forward button and sends `Ctrl+Equal` (zoom in).
Each click is one zoom step.
On the Lift, back is the lower thumb button and forward is the upper one.

```yaml
keymap:
  - name: Cursor zoom
    application:
      only:
        - Cursor
        - cursor
    remap:
      BTN_SIDE: C-MINUS
      BTN_EXTRA: C-EQUAL
```

`Cursor` is the window class from Cursor's `StartupWMClass`.
Swap the two remap lines if a mouse labels the buttons the other way.
xremap is started with `--watch=config,device`, so saving this file applies the change without a restart.

If a layout does not produce `-` and `=` from those keys, use `C-KPMINUS` and `C-KPPLUS` instead.
Those match Cursor's numpad zoom shortcuts and do not depend on the layout.

## Which mouse

The service listens only to the device named `Logitech USB Receiver Mouse`.
That is the Lift on its Logi Bolt receiver (`046d:c548`).
The Bolt receiver does not expose the product name, so the node is generic.
The other receiver on this machine is Unifying (`046d:c534`) and its mouse is `Logitech Wireless Mouse`, which is left alone.

The service line is:
```text
xremap --mouse --watch=config,device --device "Logitech USB Receiver Mouse" ~/.config/xremap/config.yml
```

For another mouse, change the `--device` argument to that device's name.
Find the name by clicking a thumb button while this is running:
```bash
RUST_LOG=debug xremap --mouse ~/.config/xremap/config.yml
```
Startup lists the selected device path and name.
Each click logs `BTN_SIDE` or `BTN_EXTRA`.
`xremap --list-devices` prints the names.
`/proc/bus/input/devices` is the other place to look: the mouse node is the `N: Name=` whose `H: Handlers=` includes the event xremap selected.

The MX Vertical uses Unifying or Bluetooth, not the Lift's Bolt receiver, so it will not be `Logitech USB Receiver Mouse`.
Point `--device` at its name after it is paired.
If two mice share one generic name, use the stable symlink under `/dev/input/by-path/` or `/dev/input/by-id/` instead of the name.
xremap accepts a device path, including those symlinks, as well as a name.

Leave `--mouse` in place.
Without it, xremap ignores mouse buttons even when `--device` names a mouse.

## After a reboot

The group, udev rule, module, extension, config, and enabled user service are all on disk.
A reboot (or a full logout) is required once, after `lift-cursor-zoom-setup`, so the new `input` group is on the session.
Later reboots keep the mapping.
The service waits until the Xremap GNOME extension is on the session bus, then grabs only the named mouse.

Check it with:
```bash
systemctl --user status lift-cursor-zoom.service
journalctl --user -u lift-cursor-zoom.service -e
```

Stop it with `systemctl --user stop lift-cursor-zoom.service`.
Disable it with `systemctl --user disable --now lift-cursor-zoom.service`.
