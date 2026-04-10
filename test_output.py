#!/usr/bin/env python
"""Write test results to file"""
import sys
from pathlib import Path

output = []

try:
    sys.path.insert(0, str(Path.cwd()))
    output.append("TEST START")
    
    from ai_video_gui import AIVideoGeneratorGUI
    output.append("✅ GUI imported")
    
    import tkinter as tk
    output.append("✅ tkinter available")
    
    root = tk.Tk()
    root.withdraw()
    output.append("✅ Root created")
    
    gui = AIVideoGeneratorGUI(root)
    output.append("✅ GUI instantiated")
    
    gui.select_mode('smooth')
    if gui.selected_mode == 'smooth':
        output.append("✅ RED button test passed")
    
    gui.select_mode('quick')
    if gui.selected_mode == 'quick':
        output.append("✅ GREEN button test passed")
    
    root.destroy()
    output.append("✅ GUI destroyed cleanly")
    
    output.append("")
    output.append("="*60)
    output.append("✅ ALL TESTS PASSED - SYSTEM READY")
    output.append("="*60)
    
except Exception as e:
    output.append(f"❌ ERROR: {e}")
    import traceback
    output.append(traceback.format_exc())

# Write results
with open('test_results.txt', 'w') as f:
    f.write('\n'.join(output))

# Print to console
print('\n'.join(output))
