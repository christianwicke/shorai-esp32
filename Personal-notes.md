* I use [this esp32](https://de.aliexpress.com/item/1005001838731651.html) ("Color": ESP-32 38PIN)).
* Firmware for installing with esptool is available [here](https://micropython.org/download/ESP32_GENERIC/).
* standalone esptool can be downloaded [here](https://github.com/espressif/esptool/releases) (under Assets).
 
# Decode Backtraces after core panic using Arduino
Follow the [Arduino troubleshoot instructions](https://arduino-esp8266.readthedocs.io/en/latest/faq/a02-my-esp-crashes.html):
1. Download [elf firmware](https://micropython.org/download/ESP32_GENERIC/)
2. If no done already, install the [decoder](https://github.com/me-no-dev/EspExceptionDecoder) in Arduino. 
3. Start Arduino, open a sketch, choose esp32 as target.
4. Open Exception Decoder, paste batchtrace into it.
5. If you don't see the deoced stacktrace, then the deocder uses still to old gdb. 
Decode it on the command line:
   1. Download and install the curent [gdb from espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/idf-tools.html)
   2. Copy the command from the Arduino Exception Decoder status line.
   E.g.: `C:\Users\Christian\AppData\Local\Arduino15\packages\esp32\tools\xtensa-esp32-elf-gcc\1.22.0-80-g6c4433a-5.2.0\bin\xtensa-esp32-elf-gdb.exe" "--batch" "C:\Users\Christian.Desktop\Downloads\ESP32_GENERIC-20240602-v1.23.0.elf" "-ex" "set listsize 1" "-ex" "l *0x40147ccd" "-ex" "l *0x4014faeb" "-ex" "l *0x40116a84" "-ex" "l *0x40116eef" "-ex" "l *0x400e4b51" "-ex" "l *0x400e689d" "-ex" "l *0x4008554d" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x400e6908" "-ex" "l *0x401042ad" "-ex" "l *0x40104542" "-ex" "l *0x400e69d9" "-ex" "l *0x400e73bb" "-ex" "l *0x400858e1" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x4008554d" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x4008554d" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x400e68b2" "-ex" "l *0x400f469a" "-ex" "l *0x400f4a3d" "-ex" "l *0x400d8090" "-ex" "q"`
   3. Adapt the command to your gdb location and start it from the command line, e.g.
      `C:\myFolders\programs\xtensa-esp-elf-gdb\bin\xtensa-esp32-elf-gdb.exe "--batch" "C:\Users\Christian.Desktop\Downloads\ESP32_GENERIC-20240602-v1.23.0.elf" "-ex" "set listsize 1" "-ex" "l *0x40147ccd" "-ex" "l *0x4014faeb" "-ex" "l *0x40116a84" "-ex" "l *0x40116eef" "-ex" "l *0x400e4b51" "-ex" "l *0x400e689d" "-ex" "l *0x4008554d" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x400e6908" "-ex" "l *0x401042ad" "-ex" "l *0x40104542" "-ex" "l *0x400e69d9" "-ex" "l *0x400e73bb" "-ex" "l *0x400858e1" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x4008554d" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x4008554d" "-ex" "l *0x400df390" "-ex" "l *0x400e689d" "-ex" "l *0x400e68b2" "-ex" "l *0x400f469a" "-ex" "l *0x400f4a3d" "-ex" "l *0x400d8090" "-ex" "q"`

## Exsample core panic
```
A fatal error occurred. The crash dump printed below may be used to help
determine what caused it. If you are not already running the most recent
version of MicroPython, consider upgrading. New versions often fix bugs.

To learn more about how to debug and/or report this crash visit the wiki
page at: https://github.com/micropython/micropython/wiki/ESP32-debugging

MPY version : v1.23.0 on 2024-06-02
IDF version : v5.0.4
Machine     : Generic ESP32 module with ESP32

Guru Meditation Error: Core  1 panic'ed (IllegalInstruction). Exception was unhandled.
Memory dump at 0x40147ccc: ffffffff ffffffff ffffffff
Core  1 register dump:
PC      : 0x40147cd0  PS      : 0x00060c30  A0      : 0x8014faee  A1      : 0x3ffce470  
A2      : 0x00000001  A3      : 0x00000009  A4      : 0x011a0009  A5      : 0x00000009  
A6      : 0x00000000  A7      : 0x00060c23  A8      : 0x8014ef50  A9      : 0x3ffce450  
A10     : 0x00000009  A11     : 0x00000011  A12     : 0xffff8fff  A13     : 0x3fff63a0  
A14     : 0x0000001f  A15     : 0x00060c23  SAR     : 0x00000009  EXCCAUSE: 0x00000000  
EXCVADDR: 0x00000000  LBEG    : 0x4000c46c  LEND    : 0x4000c477  LCOUNT  : 0x00000000


Backtrace: 0x40147ccd:0x3ffce470 0x4014faeb:0x3ffce490 0x40116a84:0x3ffce4c0 0x40116eef:0x3ffce540 0x400e4b51:0x3ffce590 0x400e689d:0x3ffce5b0 0x4008554d:0x3ffce5d0 0x400df390:0x3ffce670 0x400e689d:0x3ffce6a0 0x400e6908:0x3ffce6c0 0x401042ad:0x3ffce700 0x40104542:0x3ffce730 0x400e69d9:0x3ffce820 0x400e73bb:0x3ffce860 0x400858e1:0x3ffce8a0 0x400df390:0x3ffce940 0x400e689d:0x3ffce9a0 0x4008554d:0x3ffce9c0 0x400df390:0x3ffcea60 0x400e689d:0x3ffceab0 0x4008554d:0x3ffcead0 0x400df390:0x3ffceb70 0x400e689d:0x3ffcebc0 0x400e68b2:0x3ffcebe0 0x400f469a:0x3ffcec00 0x400f4a3d:0x3ffcec90 0x400d8090:0x3ffcecc0




ELF file SHA256: 9c4248e4297d02ec

Rebooting...
```