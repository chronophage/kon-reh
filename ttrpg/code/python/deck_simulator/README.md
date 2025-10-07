## Key Improvements Made:

### **Generator Loading**:
1. **Load Generator Deck Button**: Added "Load Generator Deck" option in both the menu and generator selection area
2. **File Dialog**: Uses standard file dialog to load JSON generator files from anywhere on the system
3. **Automatic Integration**: Loaded generators are automatically added to the available list

### **Enhanced Boon Management**:
1. **+/- Buttons**: Added dedicated buttons for adding and removing boons instead of manual entry
2. **Visual Feedback**: Status bar updates with current boon count
3. **Validation**: Proper checking for sufficient boons before operations

### **Functional Re-roll System**:
1. **Smart Re-roll**: "Re-roll 1s (1 Boon per 1)" button that:
   - Counts 1s in the last roll
   - Checks available boons
   - Re-rolls each 1 at the cost of 1 Boon
   - Updates boon count automatically
   - Shows before/after comparison
2. **Proper (SB) Handling**: New complications from re-rolled dice are properly tracked and consequences generated
3. **Outcome Recalculation**: New outcome is calculated and displayed after re-roll

### **UI Improvements**:
1. **Clearer Layout**: Better organization of die roller controls
2. **Status Updates**: Comprehensive status feedback for all operations
3. **Error Handling**: Proper error messages for edge cases

### **Usage**:
1. **Load Generators**: Use "Load Generator Deck" to import any Fate's Edge generator JSON file
2. **Manage Boons**: Use +/- buttons to adjust player resources
3. **Roll Dice**: Set parameters and roll normally
4. **Re-roll 1s**: After any roll, click "Re-roll 1s" to spend boons and re-roll any 1s in your last roll
5. **Handle Consequences**: Both original and re-roll complications automatically generate consequences

