@echo off
echo Building executable for frame.py (QR code generator)...
pyinstaller --onefile --windowed frame.py

echo Building executable for gui_qr_scanner.py (QR code scanner)...
pyinstaller --onefile --windowed gui_qr_scanner.py

echo Build complete. Executables are located in the dist folder.
pause
